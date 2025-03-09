#!/bin/bash

# Создаем директорию для бэкапов, если её нет
BACKUP_DIR="./backups"
mkdir -p $BACKUP_DIR

# Создаем имя файла бэкапа с текущей датой
DATE=$(date +"%Y-%m-%d_%H-%M-%S")
BACKUP_FILE="$BACKUP_DIR/history_db_backup_$DATE.db"

# Останавливаем контейнер backend, чтобы избежать изменений в БД во время копирования
echo "Останавливаю контейнер backend для создания бэкапа..."
docker-compose stop backend

# Копируем файл базы данных
echo "Создаю бэкап базы данных..."
cp ./backend/history.db "$BACKUP_FILE"

# Запускаем контейнер backend обратно
echo "Запускаю контейнер backend..."
docker-compose start backend

# Проверяем, что бэкап успешно создан
if [ -f "$BACKUP_FILE" ]; then
  echo "Бэкап успешно создан: $BACKUP_FILE"
  
  # Удаляем старые бэкапы (оставляем только 5 последних)
  echo "Удаляю старые бэкапы..."
  ls -t $BACKUP_DIR/history_db_backup_*.db | tail -n +6 | xargs -r rm
  
  echo "Количество сохраненных бэкапов: $(ls $BACKUP_DIR/history_db_backup_*.db | wc -l)"
else
  echo "Ошибка: Бэкап не был создан!"
  exit 1
fi 