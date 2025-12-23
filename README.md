# Distributed Event Logging System

Небольшой учебный сервис для приёма и хранения событий (логов) в MongoDB Replica Set с REST API на FastAPI.

## Что умеет
- Поднимает 3‑нодовый MongoDB Replica Set (`rs0`) через Docker Compose.
- Автоматически инициализирует Replica Set при старте (идемпотентно).
- Предоставляет REST API для записи/чтения событий и простую статистику по `level`.
- Имеет Swagger UI для ручного тестирования.

## Быстрый старт (Docker)
1) Установите Docker Desktop (или Colima) и Docker Compose v2.
2) В корне проекта запустите:
```bash
docker compose up -d --build
```
3) Откройте Swagger UI: `http://localhost:8000/docs`

Остановка и удаление данных (томов):
```bash
docker compose down -v
```

## Проверка, что Replica Set поднялся
Статус репликации:
```bash
docker compose exec mongo1 mongosh --eval 'rs.status().members.map(m=>({name:m.name,stateStr:m.stateStr}))'
```
Ожидаемое состояние: один `PRIMARY`, два `SECONDARY`.

## REST API
Базовый URL: `http://localhost:8000`

### Swagger
- Swagger UI: `http://localhost:8000/docs`
- Web UI: `http://localhost:8000/`
- В `POST /events` в поле **Request body** нужно вставлять JSON (не `curl`).

### Endpoints
#### `POST /events`
Создаёт событие.

Пример:
```bash
curl -X POST http://localhost:8000/events \
  -H "Content-Type: application/json" \
  -d '{"service":"auth","level":"info","message":"user login","host":"node1","metadata":{"user":"bob"}}'
```

#### `GET /events`
Возвращает до 100 событий. Можно фильтровать по `service` и/или `level`:
```bash
curl "http://localhost:8000/events?service=auth&level=info"
```

#### `GET /events/stats`
Статистика по уровням логов (`level`):
```bash
curl http://localhost:8000/events/stats
```

#### `GET /health`
Health-check:
```bash
curl http://localhost:8000/health
```

## Как это устроено
- `mongo1`, `mongo2`, `mongo3` — три `mongod` с `--replSet rs0`.
- `mongo-setup` — одноразовый контейнер, который ждёт доступности `mongo1` и запускает `mongo-init.js` через `mongosh`.
- `api` — FastAPI приложение, подключается к MongoDB по строке вида:
  `mongodb://mongo1:27017,mongo2:27017,mongo3:27017/?replicaSet=rs0`

## Структура проекта
- `docker-compose.yml` — сервисы MongoDB, инициализация Replica Set, API.
- `Dockerfile` — образ для API с предустановленными Python-зависимостями.
- `mongo-init.js` — конфигурация Replica Set.
- `app/` — код FastAPI (`main.py`, `routes.py`, `models.py`, `db.py`).

## Troubleshooting
- Если видите `ReadConcernMajorityNotAvailableYet` в логах MongoDB — это нормально при старте до инициализации Replica Set.
- Если контейнеры MongoDB падают с `Exited (137)` — обычно это OOM. В `docker-compose.yml` уже задан небольшой `--wiredTigerCacheSizeGB` для снижения потребления памяти.
