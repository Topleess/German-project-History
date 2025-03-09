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

# Создаем директории для certbot
mkdir -p ./certbot/conf
mkdir -p ./certbot/www

# Останавливаем существующие контейнеры, если они запущены
docker-compose down

# Запускаем только nginx и certbot для получения сертификата
docker-compose up -d nginx certbot

# Ждем, чтобы nginx успел запуститься
echo "Ожидаем запуск nginx..."
sleep 5

# Запрашиваем сертификат
echo "Запрос сертификата для домена $DOMAIN..."
docker-compose run --rm certbot certbot certonly --webroot \
  --webroot-path=/var/www/certbot \
  --agree-tos \
  $EMAIL_ARG \
  -d $DOMAIN -d www.$DOMAIN

# Перезапускаем nginx для применения сертификата
docker-compose restart nginx

echo "Процесс получения сертификата завершен."
echo "Проверьте наличие сертификата в ./certbot/conf/live/$DOMAIN/"

# Запускаем все сервисы
echo "Запуск всех сервисов..."
docker-compose up -d

echo "Настройка SSL сертификата завершена. Ваш сайт должен быть доступен по HTTPS." 