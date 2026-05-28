# 📧 Gmail Setup for Event Nexus - Samarth's Configuration

## 🎯 Your Email Configuration

**From:** eventnexus@gmail.com  
**To:** samarthchoudhary26sept@gmail.com (and all user emails)

## 🔧 Step 1: Setup eventnexus@gmail.com

### 1.1 Create/Access eventnexus@gmail.com
1. Go to [Gmail](https://gmail.com)
2. Login to `eventnexus@gmail.com` (or create this account)
3. Enable **2-Step Verification**:
   - Go to Google Account Settings → Security
   - Click "2-Step Verification" → Turn on

### 1.2 Generate App Password
1. In Google Security settings, click **"App passwords"**
2. Select:
   - App: "Mail"
   - Device: "Other (Custom name)"
3. Enter: "Event Nexus System"
4. Click **"Generate"**
5. **Copy the 16-character password** (this is your `MAIL_PASSWORD`)

## ⚙️ Step 2: Update .env File

Replace the current email configuration with your credentials:

```env
# Gmail SMTP Configuration
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USE_SSL=False
MAIL_USERNAME=eventnexus@gmail.com
MAIL_PASSWORD=your_16_character_app_password_here
MAIL_DEFAULT_SENDER=eventnexus@gmail.com
MAIL_ENABLED=True
```

**Important:**
- `MAIL_USERNAME` = `eventnexus@gmail.com`
- `MAIL_PASSWORD` = The 16-character app password (NOT your regular password)

## 🚀 Step 3: Test Email System

### 3.1 Run the Test Script
```bash
cd "/Users/samarthchoudhary/Desktop/WEBD"
source venv/bin/activate
python test_email.py
```

### 3.2 Test Real Registration
1. **Admin Test:**
   - Login as admin (`admin/admin123`)
   - Go to "Manage Guests" → "Create Guest"
   - Enter: samarthchoudhary26sept@gmail.com
   - Check your email for the invitation!

2. **User Dashboard Test:**
   - Register as a user or use mobile OTP
   - Browse events and click "Register"
   - Enter your email: samarthchoudhary26sept@gmail.com
   - Check your email immediately!

## 📨 What You'll Receive

### Email from: eventnexus@gmail.com
### Subject: 🎉 Event Nexus Invitation: [Event Name]

**Email includes:**
- ✅ **Personal greeting:** "Dear Samarth Choudhary,"
- ✅ **Event details:** Name, date, time, location
- ✅ **Registration confirmation:** "Congratulations! You have been successfully registered"
- ✅ **Event description:** Full event information
- ✅ **What to expect:** Networking, activities, food
- ✅ **Important info:** Arrival time, dress code, parking
- ✅ **Professional design:** Beautiful HTML layout
- ✅ **Event Nexus branding:** Professional appearance

## 🔍 Real-Time Email Features

### Instant Delivery:
- ⚡ **Immediate sending** when guest registers
- 📧 **Real-time notifications** to your inbox
- 🎯 **Personalized content** for each guest
- 📱 **Mobile-friendly** design

### Email Contents:
```
🎉 Event Nexus Invitation: [Event Name]

Dear Samarth Choudhary,

Congratulations! You have been successfully registered for [Event Name].

📅 Event Details:
Event: [Event Name]
Date: [Event Date]
Time: [Event Time]
Location: [Event Location]

We look forward to welcoming you!

Best regards,
The Event Management Team
🎊

From: eventnexus@gmail.com | Powered by: Event Nexus Platform
```

## 🛠️ Troubleshooting

### If emails don't arrive:
1. **Check spam folder** in Gmail
2. **Verify app password** is correct (16 characters)
3. **Ensure 2FA is enabled** on eventnexus@gmail.com
4. **Check network connectivity**

### Common errors:
- **"Authentication failed"** → Use app password, not regular password
- **"Connection refused"** → Check firewall/network settings
- **"Email service disabled"** → Verify .env configuration

## 🎯 Next Steps

1. **Setup eventnexus@gmail.com** with 2FA and app password
2. **Update .env file** with the app password
3. **Run test script** to verify configuration
4. **Test real registration** to see instant email delivery
5. **Check samarthchoudhary26sept@gmail.com** for beautiful invitations!

## 📊 Success Indicators

✅ **Console shows:** "✅ Enhanced email service initialized successfully"  
✅ **Test script shows:** "✅ Test email sent successfully!"  
✅ **Registration shows:** "Invitation email sent to samarthchoudhary26sept@gmail.com"  
✅ **Email arrives:** Professional Event Nexus invitation in your inbox  

---

**🎉 Your Event Nexus system will send beautiful, real-time email invitations from eventnexus@gmail.com to all registered guests!**
