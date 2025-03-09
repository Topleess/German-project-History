#!/bin/bash

echo "Запуск миграций базы данных..."

# Определяем, какую команду использовать для Docker Compose
DOCKER_COMPOSE_CMD="docker-compose"
if ! command -v docker-compose &> /dev/null; then
  echo "docker-compose не найден, проверяем наличие 'docker compose'..."
  if command -v docker &> /dev/null && docker compose version &> /dev/null; then
    echo "Используем 'docker compose' вместо 'docker-compose'"
    DOCKER_COMPOSE_CMD="docker compose"
  else
    echo "ОШИБКА: Docker Compose не найден! Установите Docker Compose для продолжения."
    echo "Например: sudo apt-get update && sudo apt-get install -y docker-compose-plugin"
    exit 1
  fi
fi

# Проверяем, запущен ли контейнер backend
if ! $DOCKER_COMPOSE_CMD ps | grep -q "backend.*running"; then
  echo "Контейнер backend не запущен! Пытаемся запустить..."
  $DOCKER_COMPOSE_CMD up -d backend || {
    echo "Не удалось запустить контейнер backend. Миграции не могут быть выполнены."
    exit 1
  }
  # Даем контейнеру время на запуск
  echo "Ожидаем запуск контейнера backend..."
  sleep 5
fi

# Выполняем миграции внутри контейнера backend
echo "Запускаем скрипт миграций в контейнере..."
$DOCKER_COMPOSE_CMD exec -T backend python -c "
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