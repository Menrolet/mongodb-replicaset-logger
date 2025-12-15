# Distributed Event Logging System

Сервис для приёма и хранения событий (логов) в MongoDB Replica Set с REST API на FastAPI.

## Запуск
1) Установите Docker и Docker Compose.
2) Запустите кластер и API:
```
docker compose up
```
Запустятся три узла MongoDB, сервис инициализации репликации и контейнер с API на `http://localhost:8000`.

## Проверка репликации
- Посмотреть статус Replica Set:
```
docker compose exec mongo1 mongosh --eval "rs.status()"
```

## REST API (основное)
- Swagger UI: `http://localhost:8000/docs`
- Добавить событие:
```
curl -X POST http://localhost:8000/events \
  -H "Content-Type: application/json" \
  -d '{"service":"auth","level":"info","message":"user login","host":"node1","metadata":{"user":"bob"}}'
```
- Получить события (фильтры `service`, `level` опциональны):
```
curl "http://localhost:8000/events?service=auth&level=info"
```
- Статистика по уровням:
```
curl http://localhost:8000/events/stats
```
- Health-check:
```
curl http://localhost:8000/health
```

## Структура проекта
- `docker-compose.yml` — сервисы MongoDB, инициализация Replica Set, API.
- `mongo-init.js` — конфигурация Replica Set.
- `app/` — код FastAPI (`main.py`, `routes.py`, `models.py`, `db.py`).
