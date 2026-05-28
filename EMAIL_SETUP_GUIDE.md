# 📧 Email Setup Guide - Gmail SMTP Configuration

## 🔧 Step 1: Enable Gmail App Password

### 1.1 Enable 2-Factor Authentication (2FA)
1. Go to [Google Account Settings](https://myaccount.google.com/)
2. Click on "Security"
3. Enable "2-Step Verification"

### 1.2 Generate App Password
1. In Google Security settings, click "App passwords"
2. Select "Mail" for the app
3. Select "Other (Custom name)" and enter "Event Management System"
4. Click "Generate"
5. **Copy the 16-character password** (this is your `MAIL_PASSWORD`)

## ⚙️ Step 2: Update .env File

Replace the email configuration in your `.env` file:

```env
# Gmail SMTP Configuration
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USE_SSL=False
MAIL_USERNAME=your_gmail_address@gmail.com
MAIL_PASSWORD=your_16_character_app_password
MAIL_DEFAULT_SENDER=your_gmail_address@gmail.com
MAIL_ENABLED=True
```

**Important:**
- `MAIL_USERNAME` = Your Gmail address
- `MAIL_PASSWORD` = The 16-character app password (NOT your regular Gmail password)

## 🚀 Step 3: Test Email Functionality

### 3.1 Admin Guest Creation
1. Login as admin (`admin/admin123`)
2. Go to "Manage Guests" → "Create Guest"
3. Enter guest details with a valid email
4. Check the guest's email for the invitation

### 3.2 User Dashboard Registration
1. Register as a user or login with mobile OTP
2. Browse events and click "Register"
3. Fill in the registration form
4. Check your email for the event invitation

## 📨 What the Email Contains

### Event Invitation Email Includes:
- ✅ **Personalized greeting** with guest name
- ✅ **Event details** (name, date, time, location)
- ✅ **Event description** and what to expect
- ✅ **Registration confirmation**
- ✅ **Important information** (arrival time, dress code, etc.)
- ✅ **Dietary requirements acknowledgment**
- ✅ **Professional HTML design**
- ✅ **Contact information**

### Email Features:
- 🎨 **Beautiful HTML template** with responsive design
- 📱 **Mobile-friendly** layout
- 🎉 **Celebratory tone** congratulating the guest
- 📅 **Event details** clearly displayed
- 📍 **Location and timing** information
- 🎊 **Professional branding**

## 🔍 Troubleshooting

### Common Issues:

#### "Email service disabled or not configured"
- **Cause:** Gmail credentials not set correctly
- **Fix:** Update `.env` file with correct Gmail address and app password

#### "Authentication failed"
- **Cause:** Using regular Gmail password instead of app password
- **Fix:** Generate a new app password from Google Account settings

#### "Connection refused"
- **Cause:** Firewall or network blocking SMTP
- **Fix:** Check network settings and firewall rules

#### "Invalid email format"
- **Cause:** Email address format validation failed
- **Fix:** Use proper email format (user@domain.com)

### Test Email Command:
```python
# Test email sending
from enhanced_email_service import enhanced_email_service
from app import app, Guest, Event

with app.app_context():
    # Create test guest and event
    guest = Guest(name="Test User", email="test@example.com")
    event = Event(name="Test Event", event_date=datetime.now().date())
    
    # Send test email
    result = enhanced_email_service.send_event_invitation(guest, event)
    print(f"Email sent: {result}")
```

## 📊 Email Status Messages

### Success Messages:
- `"Guest added successfully! Invitation email sent to user@gmail.com"`
- `"Registration successful! Invitation email sent to user@gmail.com"`

### Warning Messages:
- `"Guest added successfully! (Email notification failed)"`
- `"Guest added successfully! (Email error: [specific error])"`

## 🎯 Next Steps

Once email is working:
1. **Test with real email addresses**
2. **Check spam folders** if emails don't arrive
3. **Monitor email delivery** in the application logs
4. **Customize email templates** if needed

## 📞 Support

If you encounter issues:
1. Verify Gmail 2FA is enabled
2. Generate a fresh app password
3. Check network connectivity
4. Review application logs for specific error messages

---

**🎉 Your Event Management System now sends beautiful, professional event invitations automatically!**
