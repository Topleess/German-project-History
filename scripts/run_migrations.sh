#!/bin/bash

echo "Запуск миграций базы данных..."

# Выполняем миграции внутри контейнера backend
# Если у вас есть специальная команда для миграций, замените её здесь
docker-compose exec -T backend python -c "
import os
import sys
import importlib.util

# Проверяем наличие модуля миграций
migrations_path = os.path.join('app', 'migrations.py')
if os.path.exists(migrations_path):
    spec = importlib.util.spec_from_file_location('migrations', migrations_path)
    migrations = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(migrations)
    
    # Запускаем функцию миграций, если она существует
    if hasattr(migrations, 'run_migrations'):
        print('Выполняются миграции базы данных...')
        migrations.run_migrations()
        print('Миграции успешно выполнены.')
    else:
        print('Функция run_migrations не найдена в модуле миграций.')
else:
    print('Файл миграций не найден. Миграции не выполнены.')
"

# Проверяем, успешно ли выполнена команда
if [ $? -eq 0 ]; then
  echo "Миграции базы данных успешно выполнены"
else
  echo "Ошибка при выполнении миграций базы данных"
  exit 1
fi 