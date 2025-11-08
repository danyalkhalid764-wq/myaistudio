web: python init_alembic_version.py; python run_migrations.py || echo "Migrations failed, continuing..."; uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}

