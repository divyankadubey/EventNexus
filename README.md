# Event Nexus - Complete Event Management System

A comprehensive, professional Event Management System with separate admin/user portals, role-based authentication, QR code generation, mobile OTP, SMS integration, and email notifications.

## 🎯 Features

### **Core Event Management**
- **Event Creation & Management**: Complete CRUD operations with detailed information
- **Guest Registration**: Real-time guest registration with QR code generation
- **Booking Management**: Venue, catering, and service booking management
- **Budget Tracking**: Monitor event budgets and expenses

### **Advanced Features**
- **Separate Portals**: Dedicated admin and user dashboards with role-based access
- **Role-Based Authentication**: Secure user management with Admin/User roles
- **QR Code Generation**: Automatic QR codes for guest check-in and event access
- **Mobile OTP Authentication**: Secure mobile-based user authentication
- **SMS Notifications**: Twilio integration for real-time SMS alerts
- **Email Notifications**: Beautiful HTML email templates with Event Nexus branding
- **Real-time Features**: Instant notifications and updates

### **User Experience**
- **Admin Dashboard**: Comprehensive management tools and analytics
- **User Dashboard**: Event discovery and registration interface
- **Mobile Responsive**: Works perfectly on all devices
- **Professional UI**: Modern, clean interface with Bootstrap 5

## 🛠️ Tech Stack

### **Backend**
- **Framework**: Flask (Python)
- **Database**: MySQL with SQLAlchemy ORM
- **Authentication**: Session-based with role management
- **Email**: Flask-Mail with Gmail SMTP
- **SMS**: Twilio API integration
- **QR Codes**: qrcode library

### **Frontend**
- **UI Framework**: Bootstrap 5
- **Icons**: Bootstrap Icons
- **Templates**: Jinja2 templating
- **Responsive**: Mobile-first design

### **Services**
- **Environment**: Python-dotenv for configuration
- **Security**: CSRF protection, secure sessions
- **Real-time**: Instant notifications and updates

## 🚀 Installation

### Prerequisites
- Python 3.8+
- MySQL Server
- pip (Python package manager)
- Gmail account (for email notifications)
- Twilio account (for SMS notifications)

### Quick Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/event-nexus.git
   cd event-nexus
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Database**
   ```bash
   # For MySQL
   mysql -u root -p < database.sql
   
   # Or for SQLite (default)
   python setup_database_sqlite.py
   ```

5. **Configure Environment Variables**
   ```bash
   cp .env.example .env
   # Edit .env with your credentials
   ```

6. **Run the Application**
   ```bash
   python app.py
   ```

7. **Access the Application**
   - **URL**: `http://127.0.0.1:5001`
   - **Admin Login**: `admin/admin123`
   - **User Registration**: Mobile OTP available

## 📁 Project Structure

```
event-nexus/
├── app.py                      # Main Flask application
├── models.py                   # Database models with role-based authentication
├── config.py                   # Configuration settings
├── database.sql                # Database schema and sample data
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
├── .gitignore                  # Git ignore rules
├── README.md                   # Project documentation
├── HOW_TO_RUN.md              # Detailed setup guide
├── SYSTEM_ARCHITECTURE.md      # Technical documentation
├── 
├── 📧 Email Services/
│   ├── email_service.py        # Basic email functionality
│   ├── enhanced_email_service.py # Advanced email templates
│   └── gmail_troubleshoot.py   # Email troubleshooting tools
├── 
├── 📱 Communication Services/
│   ├── twilio_service.py       # SMS integration
│   └── qr_service.py           # QR code generation
├── 
├── 🗄️ Database & Migration/
│   ├── setup_database_sqlite.py # SQLite setup
│   ├── setup_database_mysql.py  # MySQL setup
│   ├── migrate_user_roles.py    # Role migration
│   └── migrations/             # Database migrations
├── 
├── 🎨 Templates/
│   ├── base.html               # Base template
│   ├── auth/                   # Authentication templates
│   │   ├── login.html
│   │   ├── register.html
│   │   ├── mobile_login.html
│   │   └── mobile_register.html
│   ├── admin/                  # Admin portal templates
│   │   └── dashboard.html
│   ├── user/                   # User portal templates
│   │   └── dashboard.html
│   ├── events/                 # Event management templates
│   ├── guests/                 # Guest management templates
│   ├── bookings/               # Booking management templates
│   └── check_in/               # Check-in templates
├── 
└── 🧪 Testing & Utilities/
    ├── test_email.py           # Email testing
    ├── test_email_demo.py      # Email preview
    ├── test_twilio.py          # SMS testing
    └── verify_gmail.py         # Gmail verification
```

## 🎯 Usage

### **Admin Portal** (`/admin/dashboard`)
- **Event Management**: Create, edit, and manage events
- **Guest Management**: Add guests, track RSVP status
- **User Management**: Manage user roles and permissions
- **Analytics**: View comprehensive event statistics
- **QR Generation**: Generate QR codes for guest check-in

### **User Portal** (`/user/dashboard`)
- **Event Discovery**: Browse and discover events
- **Event Registration**: Register for events with mobile OTP
- **Guest Registration**: Add guests to events
- **Personal Dashboard**: View registered events and status

### **Authentication System**
- **Role-Based Access**: Admin and User roles with different permissions
- **Mobile OTP**: Secure mobile-based authentication
- **Session Management**: Secure session handling
- **Password Security**: Hashed passwords with secure storage

### **Communication Features**
- **Email Notifications**: Beautiful HTML invitations with Event Nexus branding
- **SMS Alerts**: Real-time SMS notifications via Twilio
- **QR Check-in**: QR code generation for event access
- **Real-time Updates**: Instant status updates

## 🗄️ Database Schema

### **Core Tables**
- **users**: User authentication with roles (Admin/User)
- **events**: Event information with location, budget, and details
- **guests**: Guest details with QR codes and RSVP status
- **bookings**: Service bookings linked to events

### **Advanced Features**
- **Role-based permissions**: Secure access control
- **QR code generation**: Unique codes for each guest
- **Real-time tracking**: Live status updates
- **Mobile integration**: OTP-based authentication

## 🚀 Deployment

### **Development**
```bash
python app.py
# Runs on http://127.0.0.1:5001
```

### **Production**
- **Environment Variables**: Configure production settings
- **Database**: Use MySQL for production
- **Security**: Enable HTTPS and secure cookies
- **Scaling**: Deploy with Gunicorn or similar WSGI server

## 🔧 Configuration

### **Environment Variables**
```env
# Database
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=event_management

# Security
SECRET_KEY=your_secret_key_here

# Email Configuration
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=your_gmail@gmail.com
MAIL_PASSWORD=your_app_password
MAIL_ENABLED=True

# SMS Configuration
TWILIO_ACCOUNT_SID=your_twilio_sid
TWILIO_AUTH_TOKEN=your_twilio_token
TWILIO_PHONE_NUMBER=your_twilio_number
TWILIO_ENABLED=True
```

## 🎯 Current Status

### ✅ **Implemented Features**
- Complete event management system
- Separate admin/user portals with role-based access
- QR code generation for guest check-in
- Mobile OTP authentication system
- Twilio SMS integration
- Email notification system with beautiful templates
- Real-time notifications and updates
- Mobile-responsive design
- Professional UI/UX

### 🚀 **Ready for Production**
- All core features implemented and tested
- Security measures in place
- Professional documentation
- Complete deployment guides

## 📞 Support

For setup assistance or questions:
- Check `HOW_TO_RUN.md` for detailed setup instructions
- Review `SYSTEM_ARCHITECTURE.md` for technical details
- Use the provided troubleshooting scripts for email/SMS issues

## 📄 License

This project is created for educational and demonstration purposes. Feel free to use, modify, and distribute according to your needs.
