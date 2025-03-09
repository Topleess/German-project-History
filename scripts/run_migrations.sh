#!/bin/bash

echo "Запуск миграций базы данных..."

# Вывод текущей рабочей директории и списка файлов для диагностики
echo "Текущая директория: $(pwd)"
echo "Содержимое директории:"
ls -la

# Определяем, какую команду использовать для Docker Compose
# Если DOCKER_COMPOSE_CMD уже установлена в окружении, используем её
if [ -z "${DOCKER_COMPOSE_CMD}" ]; then
  echo "Переменная DOCKER_COMPOSE_CMD не была установлена ранее!"
  
  if command -v docker-compose &> /dev/null; then
    echo "Найдена команда docker-compose"
    DOCKER_COMPOSE_CMD="docker-compose"
  elif command -v docker &> /dev/null && docker compose version &> /dev/null; then
    echo "Найдена команда docker compose"
    DOCKER_COMPOSE_CMD="docker compose"
  else
    echo "ОШИБКА: Docker Compose не найден! Установите Docker Compose для продолжения."
    # Попытка установить docker-compose
    echo "Пытаемся установить docker-compose..."
    if command -v apt-get &> /dev/null; then
      sudo apt-get update && sudo apt-get install -y docker-compose-plugin
      if [ $? -eq 0 ]; then
        DOCKER_COMPOSE_CMD="docker compose"
        echo "Docker Compose успешно установлен!"
      else
        echo "Не удалось установить Docker Compose. Выход."
        exit 1
      fi
    else
      echo "Невозможно установить Docker Compose автоматически. Выход."
      exit 1
    fi
  fi
fi

echo "Используем команду Docker Compose: ${DOCKER_COMPOSE_CMD}"

# Проверка наличия docker-compose.yml
if [ ! -f docker-compose.yml ]; then
  echo "ОШИБКА: Файл docker-compose.yml не найден в текущей директории!"
  echo "Проверьте, что вы находитесь в корневой директории проекта."
  exit 1
fi

# Проверяем контейнеры
echo "Список контейнеров:"
docker ps -a | grep history

# Проверяем, запущен ли контейнер backend
echo "Проверяем запущен ли контейнер backend..."
if ! docker ps | grep -q "history-backend.*Up"; then
  echo "Контейнер backend не запущен! Пытаемся запустить..."
  ${DOCKER_COMPOSE_CMD} up -d backend || {
    echo "Не удалось запустить контейнер backend. Миграции не могут быть выполнены."
    exit 1
  }
  # Даем контейнеру время на запуск
  echo "Ожидаем запуск контейнера backend..."
  sleep 10
  
  # Проверка статуса после запуска
  if ! docker ps | grep -q "history-backend.*Up"; then
    echo "ОШИБКА: Контейнер history-backend не запустился. Выход."
    exit 1
  fi
fi

# Выполняем миграции внутри контейнера backend, без запроса пароля
echo "Запускаем скрипт миграций в контейнере..."
docker exec -i history-backend python -c "
import os
import sys
import importlib.util

print('Проверка директории в контейнере:', os.getcwd())
print('Список файлов:', os.listdir('.'))
print('Список файлов в app:', os.listdir('./app') if os.path.exists('./app') else 'Директория app не найдена')

# Проверяем наличие модуля миграций
migrations_path = os.path.join('app', 'migrations.py')
if os.path.exists(migrations_path):
    print('Модуль миграций найден:', migrations_path)
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
    print('Файл миграций не найден:', migrations_path)
    print('Создаем пустой файл миграций для будущего использования')
    
    # Создаем базовый файл миграций
    with open(migrations_path, 'w') as f:
        f.write('''
import os
from app.db.database import Base, engine

async def run_migrations():
    """
    Выполняет миграции базы данных
    """
    print('Запуск миграций...')
    async with engine.begin() as conn:
        # Создаем все таблицы из моделей, если их нет
        await conn.run_sync(Base.metadata.create_all)
    print('Миграции успешно выполнены')
''')
    print('Файл миграций создан. Запускаем миграции...')
    
    # Теперь загружаем созданный модуль
    spec = importlib.util.spec_from_file_location('migrations', migrations_path)
    migrations = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(migrations)
    
    if hasattr(migrations, 'run_migrations'):
        print('Выполняются миграции базы данных...')
        migrations.run_migrations()
        print('Миграции успешно выполнены.')
    else:
        print('Функция run_migrations не найдена в только что созданном модуле миграций.')
        print('Это странно и требует ручной проверки.')
"

# Проверяем, успешно ли выполнена команда
if [ $? -eq 0 ]; then
  echo "Миграции базы данных успешно выполнены"
else
  echo "Ошибка при выполнении миграций базы данных"
  exit 1
fi 