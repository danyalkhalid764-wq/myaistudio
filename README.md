# MyAIStudio - AI Voice Generation Platform

A complete web application for text-to-speech generation using ElevenLabs API with Easypaisa payment integration.

## 🌟 Features

### Frontend (React.js)
- **Modern UI**: Built with React.js, Vite, and Tailwind CSS
- **Responsive Design**: Mobile-friendly interface
- **Authentication**: JWT-based login/register system
- **Dashboard**: User-friendly voice generation interface
- **Trial System**: Free trial with 3 daily generations and watermarks
- **Payment Integration**: Seamless Easypaisa payment processing

### Backend (FastAPI)
- **RESTful API**: FastAPI with automatic documentation
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Authentication**: JWT-based security
- **TTS Integration**: ElevenLabs API for voice generation
- **Image Generation**: Claid API for text-to-image generation
- **Payment Processing**: Easypaisa API integration
- **Trial Restrictions**: Daily limits and watermarking for free users

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose
- ElevenLabs API key
- Claid API key
- Easypaisa API credentials

### 1. Clone the Repository
```bash
git clone <repository-url>
cd pakistaniproject
```

### 2. Environment Setup
Create a `.env` file in the root directory:

```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/myaistudio

# ElevenLabs API
ELEVENLABS_API_KEY=your_elevenlabs_api_key_here

# Claid API
CLAID_API_KEY=your_claid_api_key_here

# Easypaisa Payment API
EASYPAY_API_KEY=your_easypay_api_key_here
EASYPAY_MERCHANT_ID=your_merchant_id_here
EASYPAY_STORE_ID=your_store_id_here

# JWT Configuration
JWT_SECRET=your_jwt_secret_key_here
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 3. Run with Docker Compose
```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### 4. Access the Application
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## 🏗️ Development Setup

### Backend Development
```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run database migrations
alembic upgrade head

# Start development server
uvicorn main:app --reload
```

### Frontend Development
```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

## 📊 Database Schema

### Users Table
- `id`: Primary key
- `name`: User's full name
- `email`: Unique email address
- `password_hash`: Bcrypt hashed password
- `plan`: Trial, Starter, or Pro
- `daily_count`: Daily generation count (for trial users)
- `created_at`: Registration timestamp

### Voice History Table
- `id`: Primary key
- `user_id`: Foreign key to users
- `text`: Input text for generation
- `audio_url`: URL to generated audio (paid users only)
- `created_at`: Generation timestamp

### Generated Images Table
- `id`: Primary key
- `user_id`: Foreign key to users
- `prompt`: Input text for generation
- `image_url`: URL to generated image
- `width`: Image width in pixels
- `height`: Image height in pixels
- `created_at`: Generation timestamp

### Payments Table
- `id`: Primary key
- `user_id`: Foreign key to users
- `amount`: Payment amount
- `status`: pending, completed, failed
- `transaction_id`: Unique transaction identifier
- `created_at`: Payment timestamp

## 🔧 API Endpoints

### Authentication
- `POST /auth/register` - User registration
- `POST /auth/login` - User login
- `GET /auth/me` - Get current user info

### Text-to-Speech
- `POST /api/generate-voice` - Generate voice from text
- `GET /api/history` - Get user's voice history
- `GET /api/plan` - Get user's plan information

### Text-to-Image
- `POST /api/generate-image` - Generate image from text prompt
- `GET /api/image-history` - Get user's image generation history

### Payments
- `POST /api/payment/create` - Create payment request
- `POST /api/payment/callback` - Handle payment callback
- `GET /api/payment/history` - Get payment history
- `POST /api/payment/upgrade` - Trigger plan upgrade

## 💳 Payment Plans

### Free Trial
- 3 voice generations per day
- Watermarked audio
- No download option
- Basic quality

### Starter Plan (₨500/month)
- Unlimited generations
- High-quality audio
- Download enabled
- No watermarks

### Pro Plan (₨1000/month)
- Everything in Starter
- Premium quality voices
- Priority processing
- Advanced features

## 🔒 Security Features

- **JWT Authentication**: Secure token-based auth
- **Password Hashing**: Bcrypt for password security
- **CORS Protection**: Configured for specific origins
- **Input Validation**: Pydantic schemas for data validation
- **Environment Variables**: Secure configuration management

## 🐳 Docker Configuration

The application includes:
- **Multi-stage builds**: Optimized Docker images
- **Health checks**: Service monitoring
- **Volume persistence**: Database data persistence
- **Network isolation**: Secure service communication

## 📝 Environment Variables

### Backend (.env)
```env
DATABASE_URL=postgresql://user:password@localhost:5432/myaistudio
ELEVENLABS_API_KEY=your_elevenlabs_api_key
EASYPAY_API_KEY=your_easypay_api_key
EASYPAY_MERCHANT_ID=your_merchant_id
EASYPAY_STORE_ID=your_store_id
JWT_SECRET=your_jwt_secret
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Frontend (.env)
```env
REACT_APP_API_URL=http://localhost:8000
```

## 🚀 Deployment

### Production Deployment
1. Set up production environment variables
2. Configure domain and SSL certificates
3. Update CORS settings for production domain
4. Set up monitoring and logging
5. Configure backup strategies for database

### Scaling Considerations
- Use Redis for session management
- Implement database connection pooling
- Add load balancing for multiple instances
- Set up CDN for static assets

## 🧪 Testing

### Backend Testing
```bash
cd backend
pytest tests/
```

### Frontend Testing
```bash
cd frontend
npm test
```

## 📚 API Documentation

Once the backend is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Check the API documentation
- Review the logs for debugging

## 🔄 Updates and Maintenance

- Regular dependency updates
- Security patches
- Feature enhancements
- Performance optimizations

---

**MyAIStudio** - Transform text into natural speech with AI-powered voice generation.






