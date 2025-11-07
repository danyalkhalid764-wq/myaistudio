# MyAIStudio Backend

FastAPI backend for the MyAIStudio text-to-speech application.

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- PostgreSQL
- ElevenLabs API key
- Easypaisa API credentials

### Installation

1. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables**
```bash
cp env.example .env
# Edit .env with your actual values
```

4. **Run database migrations**
```bash
alembic upgrade head
```

5. **Start the server**
```bash
uvicorn main:app --reload
```

## 🔧 Configuration

### Environment Variables
- `DATABASE_URL`: PostgreSQL connection string
- `ELEVENLABS_API_KEY`: Your ElevenLabs API key
- `EASYPAY_API_KEY`: Easypaisa API key
- `EASYPAY_MERCHANT_ID`: Your merchant ID
- `EASYPAY_STORE_ID`: Your store ID
- `JWT_SECRET`: Secret key for JWT tokens
- `JWT_ALGORITHM`: JWT algorithm (default: HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiration time

### Database Setup
```bash
# Create database
createdb myaistudio

# Run migrations
alembic upgrade head
```

## 📊 API Documentation

Once running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🧪 Testing

```bash
# Run tests
pytest

# Run with coverage
pytest --cov=.
```

## 🐳 Docker

```bash
# Build image
docker build -t myaistudio-backend .

# Run container
docker run -p 8000:8000 myaistudio-backend
```

## 📝 API Endpoints

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - User login
- `GET /auth/me` - Get current user

### Text-to-Speech
- `POST /api/generate-voice` - Generate voice
- `GET /api/history` - Voice history
- `GET /api/plan` - Plan information

### Payments
- `POST /api/payment/create` - Create payment
- `POST /api/payment/callback` - Payment callback
- `GET /api/payment/history` - Payment history

## 🔒 Security

- JWT-based authentication
- Password hashing with bcrypt
- CORS protection
- Input validation with Pydantic
- Environment variable security

## 📈 Monitoring

- Health check endpoint: `/health`
- Structured logging
- Error handling and reporting





















