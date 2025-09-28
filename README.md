# Restaurant SaaS Backend

A comprehensive Django-based backend for a multi-tenant restaurant management system with real-time features, order management, and reporting capabilities.

## 🏗️ Architecture

### Tech Stack
- **Framework**: Django 5.2 + Django REST Framework
- **Database**: PostgreSQL
- **Authentication**: JWT (Simple JWT)
- **Real-time**: Django Channels + Redis
- **Background Tasks**: Celery + Redis
- **File Storage**: Local filesystem (AWS S3 optional)
- **ASGI Server**: Daphne

### App Structure
```
backend/
├── api/                 # Core domain (organizations, shops, users)
├── accounts/            # Authentication & user management
├── menu/               # Menu & categories management
├── orders/             # Order processing & kitchen display
├── chat/               # Real-time messaging
├── reports/            # Report generation
├── restaurant/         # Project configuration
└── utils/              # Shared utilities
```

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- PostgreSQL
- Redis
- Virtual environment

### Installation

1. **Clone and setup**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. **Environment Configuration**
Create `.env` file in project root:
```env
SECRET_KEY=your-secret-key
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
AWS_ACCESS_KEY_ID=your-aws-key
AWS_SECRET_ACCESS_KEY=your-aws-secret
AWS_STORAGE_BUCKET_NAME=your-bucket-name
```

3. **Database Setup**
```bash
# Create PostgreSQL database
createdb restaurant

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

4. **Start Services**
```bash
# Terminal 1: Django server
python manage.py runserver

# Terminal 2: Celery worker
celery -A restaurant worker -l info

# Terminal 3: ASGI server (for WebSockets)
daphne restaurant.asgi:application
```

## 📚 API Documentation

### Authentication
- **Login**: `POST /api/token/`
- **Register**: `POST /api/auth/register/`
- **Profile**: `GET /api/auth/me/`
- **Update Profile**: `PATCH /api/auth/update-profile/<id>/`
- **Change Password**: `PATCH /api/auth/change-password/`
- **Password Reset**: `POST /api/auth/password-reset/`

### Core Management

#### Organizations
- `GET/POST /api/organizations/` - List/create organizations
- `GET/PATCH/DELETE /api/organizations/<id>/` - Organization details

#### Shops
- `GET/POST /api/shops/` - List/create shops
- `GET/PATCH/DELETE /api/shops/<id>/` - Shop details
- `GET /api/client/shops/` - Public shop listing

#### Users
- `GET /api/auth/users/` - List users (filtered by role/organization)
- `GET /api/dashboard/count/` - Global statistics

### Menu Management

#### Categories
- `GET/POST /api/menu/categories/` - List/create categories
- `GET/PATCH/DELETE /api/menu/categories/<id>/` - Category details
- `GET /api/menu/client/categories/<shop_id>/` - Public categories

#### Menu Items
- `GET/POST /api/menu/menu/` - List/create menu items
- `GET/PATCH/DELETE /api/menu/menu/<id>/` - Menu item details
- `GET /api/menu/client/menus/<shop_id>/` - Public menu listing

### Orders & Kitchen

#### Orders
- `GET/POST /api/orders/` - List/create orders
- `GET/PATCH/DELETE /api/orders/<id>/` - Order management
- `GET /api/orders/kitchen-display/` - Kitchen display view

#### Order Items
- `GET/POST /api/orders/items/` - Order items management
- `GET/PATCH/DELETE /api/orders/items/<id>/` - Item details

#### Ratings
- `GET/POST /api/orders/ratings/` - Menu ratings
- `GET/PATCH/DELETE /api/orders/ratings/<id>/` - Rating details

### Real-time Features

#### Chat
- `GET/POST /api/chat/rooms/` - Chat rooms
- `GET /api/chat/messages/?room_id=<id>` - Messages
- **WebSocket**: `ws://localhost:8000/ws/chat/<room_id>/`

#### Kitchen Display
- **WebSocket**: `ws://localhost:8000/ws/orders/<shop_id>/`

### Reports
- `PATCH /api/reports/users/` - Generate user reports
- `PATCH /api/reports/organizations/` - Generate organization reports
- `PATCH /api/reports/shops/` - Generate shop reports
- `PATCH /api/reports/menu/` - Generate menu reports
- `PATCH /api/reports/orders/` - Generate order reports

## 🔐 User Roles & Permissions

### Role Hierarchy
1. **Admin** - Full system access
2. **Organization Admin** - Manages organization and shops
3. **Shop Admin** - Manages specific shop
4. **User** - Customer access

### Permission Matrix
| Feature | Admin | Org Admin | Shop Admin | User |
|---------|-------|-----------|------------|------|
| Organizations | ✅ | ❌ | ❌ | ❌ |
| Shops | ✅ | ✅ | ❌ | 👁️ |
| Menu | ✅ | ✅ | ✅ | 👁️ |
| Orders | ✅ | ✅ | ✅ | ✅ |
| Reports | ✅ | ✅ | ✅ | ❌ |
| Chat | ✅ | ✅ | ✅ | ✅ |

## 🗄️ Database Schema

### Core Models
- **CustomUser** - Extended user with roles
- **Organization** - Multi-tenant organizations
- **Shop** - Restaurant locations
- **MenuCategory** - Menu groupings
- **Menu** - Food items
- **Order** - Customer orders
- **OrderItem** - Order line items
- **ChatRoom** - Customer-shop messaging
- **Message** - Chat messages

### Key Relationships
```
Organization → Shop → MenuCategory → Menu
User → Order → OrderItem
Shop → ChatRoom → Message
```

## 🔄 Real-time Features

### WebSocket Endpoints
- **Chat**: `/ws/chat/<room_id>/` - Customer-shop messaging
- **Kitchen**: `/ws/orders/<shop_id>/` - Kitchen display updates
- **Reports**: `/ws/reports/` - Report generation notifications

### Message Types
```json
// Chat message
{
  "text": "Hello, I'd like to order",
  "sender": "user"
}

// Order update
{
  "method": "processing",
  "order_id": 123
}
```

## 📊 Reporting System

### Report Types
- **User Reports** - User lists with filtering
- **Organization Reports** - Organization data
- **Shop Reports** - Shop performance
- **Menu Reports** - Menu analytics
- **Order Reports** - Order summaries

### Report Generation
Reports are generated asynchronously using Celery and delivered via WebSocket notifications as PDF files.

## 🛠️ Development

### Code Structure
```
api/           # Core business logic
├── models.py      # Domain models
├── views.py       # REST endpoints
├── serializers.py # Data serialization
└── urls.py        # URL routing

accounts/      # Authentication
menu/          # Menu management
orders/        # Order processing
chat/          # Real-time messaging
reports/       # Report generation
```

### Key Features
- **Multi-tenancy** - Organization-based data isolation
- **Role-based Access** - Granular permissions
- **Real-time Updates** - WebSocket integration
- **Async Processing** - Celery background tasks
- **File Management** - Upload handling
- **Report Generation** - PDF export system

## 🚀 Deployment

### Production Checklist
- [ ] Set `DEBUG = False`
- [ ] Configure production database
- [ ] Set up Redis for Celery/Channels
- [ ] Configure email settings
- [ ] Set up file storage (AWS S3)
- [ ] Configure CORS origins
- [ ] Set up SSL certificates
- [ ] Configure static file serving

### Environment Variables
```env
SECRET_KEY=production-secret-key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com
DATABASE_URL=postgresql://user:pass@host:port/db
REDIS_URL=redis://localhost:6379/0
```

## 📝 API Examples

### Authentication Flow
```bash
# Register
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"username": "user", "email": "user@example.com", "password": "pass123"}'

# Login
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "user", "password": "pass123"}'

# Use token
curl -H "Authorization: Bearer <token>" http://localhost:8000/api/auth/me/
```

### Order Creation
```bash
curl -X POST http://localhost:8000/api/orders/ \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "shop": 1,
    "table_number": 1,
    "total_price": "25.50",
    "items": [
      {"id": 1, "price": "12.50", "quantity": 1},
      {"id": 2, "price": "13.00", "quantity": 1}
    ]
  }'
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Contact the development team
- Check the documentation

---

**Built with ❤️ for modern restaurant management**
