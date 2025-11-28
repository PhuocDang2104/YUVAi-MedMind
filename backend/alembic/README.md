# Alembic

Tạo migration mới (autogenerate):
```bash
cd backend
$env:PYTHONPATH="."
alembic revision --autogenerate -m "init schema"
alembic upgrade head
```

Config URL lấy từ `.env` (settings.database_url).
