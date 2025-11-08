web: python init_alembic_version.py; echo "About to start server..."; python start_server.py || echo "Server script failed, trying direct uvicorn..."; python -c "import uvicorn; from main import app; uvicorn.run(app, host='0.0.0.0', port=int(__import__('os').getenv('PORT', '8000')))"

