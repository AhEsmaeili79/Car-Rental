# 🚗 Car Rental System (سواربینو)

A comprehensive Django-based car rental platform that connects car owners (renters) with customers (passengers) in a peer-to-peer marketplace. The application supports Persian/Farsi language and includes features for car listing, booking, reviews, and administrative management.

## 🌟 Features

### For Passengers (Customers)
- **Browse Cars**: View available cars with detailed information
- **Advanced Search & Filtering**: Filter by price, location, capacity, and driver availability
- **Car Details**: View multiple images, specifications, and reviews
- **Booking System**: Reserve cars with date selection and passenger count
- **Review System**: Rate and review cars after rental
- **Order Management**: View booking history and cancel reservations
- **User Profile**: Manage personal information and view rental history

### For Car Owners (Renters)
- **Car Management**: Add, edit, and manage car listings
- **Booking Requests**: Receive and manage rental requests
- **Order Confirmation**: Approve or reject booking requests
- **Earnings Tracking**: Monitor rental income and booking status
- **Car Status**: Activate/deactivate car listings

### For Administrators
- **Dashboard**: Overview of users, cars, and orders
- **User Management**: Manage user accounts and roles
- **Car Moderation**: Review and approve car listings
- **Order Monitoring**: Track all rental transactions
- **Renter Approval**: Approve car owner applications
- **System Analytics**: View platform statistics and recent activities

## 🛠️ Technology Stack

- **Backend**: Django 4.x
- **Database**: SQLite (development) / PostgreSQL (production ready)
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Image Processing**: Pillow (PIL)
- **Date Handling**: django-jalali, jdatetime (Persian calendar support)
- **Forms**: django-crispy-forms
- **Authentication**: Django's built-in authentication system

## 📁 Project Structure

```
Car-Rental/
├── admin_app/          # Admin panel and management
├── car/               # Car listing and management
├── core/              # Django settings and configuration
├── reservations/      # Booking and order management
├── users/             # User authentication and profiles
├── static/            # CSS, JS, images, and fonts
├── templates/         # HTML templates
├── media/             # User-uploaded files
└── requirements.txt   # Python dependencies
```

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Step 1: Clone the Repository
```bash
git clone <repository-url>
cd Car-Rental
```

### Step 2: Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Database Setup
```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 5: Create Superuser
```bash
python manage.py createsuperuser
```

### Step 6: Run Development Server
```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`

## 👥 User Roles

### 1. Passenger (Default Role)
- Browse and search cars
- Make reservations
- Write reviews
- Manage profile

### 2. Renter (Car Owner)
- List cars for rent
- Manage bookings
- Approve/reject requests
- Track earnings

### 3. Admin
- Full system access
- User management
- Content moderation
- System analytics

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the project root:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
```

### Database Configuration
The application uses SQLite by default. For production, update `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_db_name',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## 📱 Key Features Explained

### Car Listing System
- **Multiple Images**: Up to 5 images per car with automatic resizing
- **Detailed Information**: Name, city, capacity, price per day, driver availability
- **Status Management**: Active/inactive car listings
- **Owner Association**: Each car is linked to its owner

### Booking System
- **Date Validation**: Prevents double bookings
- **Capacity Check**: Ensures passenger count doesn't exceed car capacity
- **Price Calculation**: Automatic calculation based on days and driver option
- **Status Tracking**: Pending, confirmed, cancelled, completed

### Review System
- **Rating System**: 1-5 star ratings
- **Comment Support**: Text reviews for detailed feedback
- **One Review Per User**: Prevents spam and duplicate reviews
- **Average Rating Display**: Shows overall car rating

### Admin Panel
- **Dashboard**: Real-time statistics and recent activities
- **User Management**: View, edit, and manage user accounts
- **Content Moderation**: Approve/reject cars and manage listings
- **Order Monitoring**: Track all rental transactions

## 🌐 API Endpoints

### Authentication
- `GET /` - Home page with login/signup
- `POST /login/` - User login
- `POST /signup/` - User registration
- `GET /logout/` - User logout

### Cars
- `GET /cars/` - List all cars with filters
- `GET /cars/<id>/` - Car detail page
- `POST /cars/<id>/review/` - Add/edit review
- `GET /cars/add/` - Add new car (renters only)
- `POST /cars/add/` - Create new car listing

### Reservations
- `GET /reservations/` - User's order history
- `POST /reservations/<car_id>/` - Create new reservation
- `POST /reservations/cancel/<order_id>/` - Cancel reservation
- `GET /reservations/host/` - Host's booking requests

### Admin
- `GET /admin-panel/` - Admin dashboard
- `POST /admin-panel/` - Admin actions (user management, etc.)

## 🎨 UI/UX Features

### Persian Language Support
- Right-to-left (RTL) layout
- Persian date picker (Jalali calendar)
- Arabic numerals support
- Persian text throughout the interface

### Responsive Design
- Mobile-first approach
- Bootstrap 5 framework
- Cross-browser compatibility
- Touch-friendly interface

### User Experience
- Preloader animations
- Toast notifications
- Modal dialogs
- Image galleries
- Form validation

## 🔒 Security Features

- CSRF protection
- SQL injection prevention
- XSS protection
- Secure file uploads
- Authentication required for sensitive operations
- Role-based access control

## 📊 Database Schema

### User Model
- Username, email, password
- Role (Admin/Renter/Passenger)
- Phone number, address
- Role change requests

### Car Model
- Name, images, city, capacity
- Price per day, driver availability
- Owner reference, active status

### Order Model
- Car and user references
- Pickup/return dates
- Passenger count, total price
- Status tracking

### Review Model
- Car and user references
- Rating (1-5), comment
- Creation timestamp

## 🚀 Deployment

### Production Checklist
1. Set `DEBUG = False` in settings
2. Configure production database
3. Set up static file serving
4. Configure media file storage
5. Set up HTTPS
6. Configure logging
7. Set up backup system

### Recommended Hosting
- **Heroku**: Easy deployment with PostgreSQL
- **DigitalOcean**: VPS with Django deployment
- **AWS**: Scalable cloud hosting
- **PythonAnywhere**: Django-specific hosting

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Contact the development team
- Check the documentation

## 🔄 Version History

- **v1.0.0**: Initial release with core features
- Basic car rental functionality
- User authentication and roles
- Booking system
- Admin panel

---

**Note**: This application is designed for the Persian market with full RTL support and Persian language integration. The system supports both English and Persian interfaces.

