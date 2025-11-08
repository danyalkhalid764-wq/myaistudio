@echo off
echo Activating MyAIStudio Backend Virtual Environment...
call venv\Scripts\activate.bat
echo Virtual environment activated!
echo.
echo Next steps:
echo 1. Copy env.example to .env: copy env.example .env
echo 2. Edit .env with your API keys
echo 3. Run migrations: alembic upgrade head
echo 4. Start server: uvicorn main:app --reload
echo.
echo Server will be available at: http://localhost:8000
echo API Documentation: http://localhost:8000/docs
cmd /k
























