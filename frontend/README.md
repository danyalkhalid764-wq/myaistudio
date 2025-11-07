# MyAIStudio Frontend

React.js frontend for the MyAIStudio text-to-speech application.

## 🚀 Quick Start

### Prerequisites
- Node.js 18+
- npm or yarn

### Installation

1. **Install dependencies**
```bash
npm install
```

2. **Start development server**
```bash
npm run dev
```

3. **Build for production**
```bash
npm run build
```

## 🎨 Features

- **Modern UI**: Built with React.js and Tailwind CSS
- **Responsive Design**: Mobile-first approach
- **Authentication**: JWT-based login system
- **Voice Generation**: Real-time TTS with audio playback
- **Payment Integration**: Seamless plan upgrades
- **Trial System**: Free trial with restrictions

## 🏗️ Project Structure

```
src/
├── components/          # Reusable components
│   ├── Navbar.jsx      # Navigation component
│   ├── VoiceGenerator.jsx # Voice generation UI
│   └── ProtectedRoute.jsx # Route protection
├── pages/              # Page components
│   ├── Landing.jsx    # Home page
│   ├── Login.jsx      # Login page
│   ├── Register.jsx   # Registration page
│   ├── Dashboard.jsx  # User dashboard
│   └── Pricing.jsx     # Pricing plans
├── contexts/          # React contexts
│   └── AuthContext.jsx # Authentication context
├── api/               # API service functions
│   ├── auth.js        # Authentication API
│   ├── tts.js         # Text-to-speech API
│   └── payment.js     # Payment API
└── App.jsx           # Main application component
```

## 🎯 Key Components

### VoiceGenerator
- Text input for voice generation
- Real-time audio playback
- Trial/paid user restrictions
- Download functionality for paid users

### Dashboard
- User plan information
- Voice generation interface
- Generation history
- Upgrade prompts for trial users

### Pricing
- Plan comparison
- Payment integration
- Feature lists
- FAQ section

## 🔧 Configuration

### Environment Variables
```env
REACT_APP_API_URL=http://localhost:8000
```

### API Integration
The frontend communicates with the FastAPI backend through:
- Authentication endpoints
- TTS generation endpoints
- Payment processing endpoints

## 🎨 Styling

- **Tailwind CSS**: Utility-first CSS framework
- **Custom Components**: Reusable UI components
- **Responsive Design**: Mobile-friendly layouts
- **Dark Mode**: Optional dark theme support

## 🧪 Testing

```bash
# Run tests
npm test

# Run with coverage
npm run test:coverage
```

## 🐳 Docker

```bash
# Build image
docker build -t myaistudio-frontend .

# Run container
docker run -p 3000:80 myaistudio-frontend
```

## 📱 Mobile Support

- Responsive design for all screen sizes
- Touch-friendly interface
- Mobile-optimized audio controls
- Progressive Web App features

## 🔒 Security

- JWT token management
- Secure API communication
- Input validation
- XSS protection

## 🚀 Deployment

### Production Build
```bash
npm run build
```

### Environment Setup
- Configure API endpoints
- Set up authentication
- Configure payment integration

## 📊 Performance

- Code splitting for faster loading
- Lazy loading of components
- Optimized bundle size
- Caching strategies

## 🎯 User Experience

- Intuitive interface design
- Real-time feedback
- Error handling and notifications
- Accessibility features





















