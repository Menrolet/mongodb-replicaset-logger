# Примеры запросов и команд

## Запуск и остановка
```bash
docker compose up -d --build
```

```bash
docker compose down -v
```

## Проверка Replica Set
```bash
docker compose exec mongo1 mongosh --eval 'rs.status().members.map(m=>({name:m.name,stateStr:m.stateStr}))'
```

## Базовый URL
```
http://localhost:8000
```

## Web UI
```
http://localhost:8000/
```

## Swagger UI
```
http://localhost:8000/docs
```

## REST API
### POST /events — создать событие
```bash
curl -X POST http://localhost:8000/events \
  -H "Content-Type: application/json" \
  -d '{"service":"auth","level":"info","message":"user login","host":"node1","metadata":{"user":"bob","ip":"10.0.0.1"}}'
```

### GET /events — получить список
```bash
curl http://localhost:8000/events
```

### GET /events с фильтрами
```bash
curl "http://localhost:8000/events?service=auth&level=info"
```

### GET /events/stats — статистика по уровням
```bash
curl http://localhost:8000/events/stats
```

### GET /health — проверка API
```bash
curl http://localhost:8000/health
```
