#!/bin/bash

# Проверяем, что имя домена передано
if [ -z "$1" ]; then
  echo "Ошибка: Имя домена не указано. Использование: $0 example.com [email@example.com]"
  exit 1
fi

DOMAIN=$1
EMAIL=$2

# Преобразуем домен в Punycode, если он содержит кириллические символы
if command -v idn2 &> /dev/null; then
  echo "Проверяем, нужно ли преобразовывать домен в Punycode..."
  PUNYCODE_DOMAIN=$(echo "$DOMAIN" | idn2) || PUNYCODE_DOMAIN="$DOMAIN"
  
  # Если домен был преобразован, выводим информацию
  if [ "$PUNYCODE_DOMAIN" != "$DOMAIN" ]; then
    echo "Домен преобразован в Punycode: $PUNYCODE_DOMAIN"
    DOMAIN="$PUNYCODE_DOMAIN"
  else
    echo "Домен не требует преобразования в Punycode"
  fi
else
  echo "Утилита idn2 не установлена, используем домен как есть"
fi

# Если email не указан, используем non-interactive режим с --register-unsafely-without-email
if [ -z "$EMAIL" ]; then
  EMAIL_ARG="--register-unsafely-without-email"
else
  EMAIL_ARG="--email $EMAIL"
fi

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

# Создаем директории для certbot
mkdir -p ./certbot/conf
mkdir -p ./certbot/www

# Останавливаем существующие контейнеры, если они запущены
echo "Останавливаем контейнеры..."
$DOCKER_COMPOSE_CMD down || echo "Предупреждение: Не удалось остановить контейнеры, возможно они не были запущены."

# Запускаем только nginx и certbot для получения сертификата
echo "Запускаем nginx и certbot..."
$DOCKER_COMPOSE_CMD up -d nginx certbot

# Ждем, чтобы nginx успел запуститься
echo "Ожидаем запуск nginx..."
sleep 5

# Запрашиваем сертификат
echo "Запрос сертификата для домена $DOMAIN..."
$DOCKER_COMPOSE_CMD run --rm certbot certbot certonly --webroot \
  --webroot-path=/var/www/certbot \
  --agree-tos \
  $EMAIL_ARG \
  -d $DOMAIN -d www.$DOMAIN

# Проверяем, успешно ли получен сертификат
if [ $? -ne 0 ]; then
  echo "ОШИБКА: Не удалось получить сертификат. Проверьте логи certbot для дополнительной информации."
  echo "Останавливаем контейнеры..."
  $DOCKER_COMPOSE_CMD down
  exit 1
fi

# Перезапускаем nginx для применения сертификата
echo "Перезапускаем nginx для применения сертификата..."
$DOCKER_COMPOSE_CMD restart nginx

echo "Процесс получения сертификата завершен."
echo "Проверьте наличие сертификата в ./certbot/conf/live/$DOMAIN/"

# Запускаем все сервисы
echo "Запуск всех сервисов..."
$DOCKER_COMPOSE_CMD up -d

echo "Настройка SSL сертификата завершена. Ваш сайт должен быть доступен по HTTPS." 