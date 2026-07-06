# FastAPI + PostgreSQL Docker Compose Project

Учебный проект: FastAPI-приложение и PostgreSQL запускаются через Docker Compose.

## Стек

- FastAPI
- PostgreSQL 15
- Docker
- Docker Compose
- psycopg

## Структура проекта

```text
.
├── app/
│   └── main.py
├── compose.yaml
├── Dockerfile
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Переменные окружения

Перед запуском нужно создать файл `.env` на основе `.env.example`:

```bash
cp .env.example .env
```

Пример содержимого `.env.example`:

```env
POSTGRES_USER=admin
POSTGRES_PASSWORD=secret
POSTGRES_DB=appdb
DATABASE_URL=postgresql://admin:secret@db:5432/appdb
```

> В реальных проектах `.env` не должен попадать в GitHub, потому что там могут быть пароли и другие секреты.

## Запуск проекта

Проверить конфигурацию Docker Compose:

```bash
docker compose config
```

Запустить проект в фоне с пересборкой образа приложения:

```bash
docker compose up -d --build
```

## Проверка статуса контейнеров

```bash
docker compose ps
```

Ожидается, что сервисы `app` и `db` будут в состоянии `Up (healthy)`.

## Проверка FastAPI

```bash
curl localhost:8000
```

Ожидаемый ответ:

```json
{"message":"FastAPI app is running"}
```

## Проверка подключения к PostgreSQL через FastAPI

```bash
curl localhost:8000/db-check
```

Ожидаемый ответ содержит статус `ok` и версию PostgreSQL:

```json
{
  "status": "ok",
  "postgres_version": "PostgreSQL ..."
}
```

Цепочка проверки:

```text
Mac
→ localhost:8000
→ ports "8000:8000"
→ app container
→ FastAPI /db-check
→ DATABASE_URL
→ db:5432
→ PostgreSQL
→ SELECT version()
→ JSON response
```

## Healthcheck

В проекте настроены healthcheck-и для двух сервисов.

### db healthcheck

Проверяет готовность PostgreSQL внутри `db` container через `pg_isready`.

Смысл:

```text
db healthy = PostgreSQL готов принимать подключения
```

### app healthcheck

Проверяет, что FastAPI отвечает на HTTP-запрос внутри `app` container.

Смысл:

```text
app healthy = FastAPI запущен и отвечает
```

### depends_on condition: service_healthy

`app` запускается только после того, как `db` станет `healthy`.

```text
depends_on = порядок запуска
healthcheck = проверка готовности service
condition: service_healthy = ждать successful healthcheck
```

## Остановка проекта

Остановить проект, удалить containers и network, но сохранить volume с данными PostgreSQL:

```bash
docker compose down
```

Остановить проект и удалить containers, network и volume с данными PostgreSQL:

```bash
docker compose down -v
```

## Основная архитектурная формула

```text
Mac → app = через ports
app → db = через Docker network
```

- `ports "8000:8000"` нужен, чтобы Mac мог обратиться к FastAPI в `app` container.
- `backend network` нужен, чтобы `app` container мог обратиться к `db` container по hostname `db`.
- `pgdata` — Docker volume для хранения данных PostgreSQL.
