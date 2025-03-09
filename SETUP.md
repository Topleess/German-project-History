# Настройка проекта для хостинга с доменным именем

## Предварительные требования

- Ubuntu/Debian сервер с доступом по SSH
- Зарегистрированное доменное имя с настроенными A/AAAA записями, указывающими на IP-адрес вашего сервера
- Docker и Docker Compose установлены на сервере
- Git установлен на сервере

## Шаг 1: Клонирование репозитория на сервер

```bash
# Подключение к серверу
ssh user@your-server-ip

# Создание директории для проекта
mkdir -p /path/to/project
cd /path/to/project

# Клонирование репозитория
git clone https://github.com/your-username/your-repo.git .
```

## Шаг 2: Настройка GitHub Actions Secrets

В вашем GitHub репозитории добавьте следующие секреты (Settings -> Secrets and variables -> Actions -> New repository secret):

- `SSH_HOST`: IP-адрес вашего сервера
- `SSH_USER`: Имя пользователя для SSH-подключения
- `SSH_PRIVATE_KEY`: Содержимое приватного SSH-ключа для подключения к серверу
- `DEPLOY_PATH`: Путь к папке проекта на сервере (например, `/path/to/project`)
- `DOMAIN_NAME`: Ваше доменное имя (например, `example.com`)

## Шаг 3: Первоначальная настройка на сервере

### 3.1. Создание директорий для certbot

```bash
mkdir -p certbot/conf
mkdir -p certbot/www
```

### 3.2. Получение SSL-сертификата для домена

```bash
# Запуск скрипта инициализации SSL с указанием домена и email для уведомлений
bash scripts/init_ssl.sh your-domain.com your-email@example.com
```

## Шаг 4: Настройка nginx (происходит автоматически)

Конфигурация nginx уже включена в проект. При деплое через GitHub Actions происходит следующее:

1. Создаётся конфигурация для вашего домена
2. Настраивается SSL
3. Настраивается перенаправление с HTTP на HTTPS
4. Настраивается проксирование для frontend и backend

## Шаг 5: Запуск проекта

```bash
# Сборка и запуск контейнеров
docker-compose up -d --build
```

## Шаг 6: Проверка работоспособности

Откройте ваш домен в браузере: `https://your-domain.com`

## Дополнительная информация

### Обновление проекта через GitHub Actions

При пуше в ветку `main` или `master` автоматически запускается GitHub Actions workflow, который:

1. Собирает и тестирует приложения
2. Деплоит приложения на сервер
3. Создает резервную копию базы данных перед обновлением
4. Запускает миграции базы данных
5. Перезапускает nginx с обновленной конфигурацией

### Ручное обновление проекта на сервере

```bash
cd /path/to/project
git pull
docker-compose down
docker-compose up -d --build
```

### Резервное копирование базы данных

```bash
# Автоматическое резервное копирование выполняется при деплое
# Для ручного бэкапа:
bash scripts/backup_db.sh
```

### Обновление SSL-сертификата

SSL-сертификаты Let's Encrypt действительны в течение 90 дней. Автоматическое обновление настроено через certbot контейнер.

## Устранение неполадок

### Проблемы с nginx

```bash
# Проверка конфигурации nginx
docker-compose exec nginx nginx -t

# Просмотр логов nginx
docker-compose logs nginx
```

### Проблемы с контейнерами

```bash
# Просмотр статуса контейнеров
docker-compose ps

# Просмотр логов всех контейнеров
docker-compose logs

# Просмотр логов конкретного контейнера
docker-compose logs frontend
docker-compose logs backend
``` 