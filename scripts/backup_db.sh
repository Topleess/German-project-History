#!/bin/bash

# Определяем, какую команду использовать для Docker Compose
DOCKER_COMPOSE_CMD="docker-compose"
if ! command -v docker-compose &> /dev/null; then
  echo "docker-compose не найден, проверяем наличие 'docker compose'..."
  if command -v docker &> /dev/null && docker compose version &> /dev/null; then
    echo "Используем 'docker compose' вместо 'docker-compose'"
    DOCKER_COMPOSE_CMD="docker compose"
  else
    echo "ПРЕДУПРЕЖДЕНИЕ: Docker Compose не найден, но продолжаем выполнение..."
  fi
fi

# Создаем директорию для бэкапов, если её нет
BACKUP_DIR="./backups"
mkdir -p $BACKUP_DIR

# Создаем имя файла бэкапа с текущей датой
DATE=$(date +"%Y-%m-%d_%H-%M-%S")
BACKUP_FILE="$BACKUP_DIR/history_db_backup_$DATE.db"

# Останавливаем контейнер backend, чтобы избежать изменений в БД во время копирования
echo "Останавливаю контейнер backend для создания бэкапа..."
$DOCKER_COMPOSE_CMD stop backend || {
  echo "Не удалось остановить контейнер. Проверяем существование базы данных без остановки..."
  if [ ! -f "./backend/history.db" ]; then
    echo "Ошибка: файл базы данных не найден!"
    exit 1
  fi
  echo "Файл базы данных найден, продолжаем без остановки контейнера (возможны проблемы с целостностью бэкапа)"
}

# Копируем файл базы данных
echo "Создаю бэкап базы данных..."
cp ./backend/history.db "$BACKUP_FILE" || {
  echo "Ошибка при копировании базы данных!"
  # Пытаемся запустить контейнер обратно
  $DOCKER_COMPOSE_CMD start backend || echo "Не удалось запустить контейнер backend!"
  exit 1
}

# Запускаем контейнер backend обратно
echo "Запускаю контейнер backend..."
$DOCKER_COMPOSE_CMD start backend || echo "Не удалось запустить контейнер backend!"

# Проверяем, что бэкап успешно создан
if [ -f "$BACKUP_FILE" ]; then
  echo "Бэкап успешно создан: $BACKUP_FILE"
  
  # Удаляем старые бэкапы (оставляем только 5 последних)
  echo "Удаляю старые бэкапы..."
  ls -t $BACKUP_DIR/history_db_backup_*.db 2>/dev/null | tail -n +6 | xargs -r rm || echo "Нет старых бэкапов для удаления"
  
  # Считаем количество бэкапов, но не выдаем ошибку, если их нет
  BACKUP_COUNT=$(ls $BACKUP_DIR/history_db_backup_*.db 2>/dev/null | wc -l || echo 0)
  echo "Количество сохраненных бэкапов: $BACKUP_COUNT"
else
  echo "Ошибка: Бэкап не был создан!"
  exit 1
fi 