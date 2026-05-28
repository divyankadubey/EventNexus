# 🚀 Twilio OTP - Quick Start Guide

Your Event Management System is now ready to send **real-time OTP** via Twilio SMS!

---

## ✅ What's Already Done

✅ **MSG91 completely removed** - No traces left  
✅ **Twilio package installed** - `twilio==8.10.0`  
✅ **Service created** - `twilio_service.py`  
✅ **Routes added** - 3 new API endpoints  
✅ **Configuration ready** - Just need your credentials  

---

## 🎯 Next: Get Your Twilio Account (5 Minutes)

### Step 1: Sign Up for Twilio
👉 **Go to:** https://www.twilio.com/try-twilio

1. Sign up with your email
2. Verify your phone number
3. **Get $15 FREE credit** (~500 SMS messages)

### Step 2: Get Your Credentials

Once logged in:

1. Go to **Dashboard**: https://console.twilio.com/
2. Find these 3 values:
   - **Account SID** (looks like: `ACxxxxxxxxxxxxxxxx`)
   - **Auth Token** (click "show" to reveal)
   - **Phone Number** (buy a number if you don't have one)

### Step 3: Buy a Phone Number (FREE with trial)

1. In Twilio Console → **Phone Numbers** → **Buy a Number**
2. Select **United States** (for trial account)
3. Click **Search** → Choose any number
4. Click **Buy**
5. Copy your number (format: `+15551234567`)

### Step 4: Update Your `.env` File

Open your `.env` file and replace these lines:

```bash
# Twilio SMS Configuration
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your_auth_token_here
TWILIO_PHONE_NUMBER=+1234567890
TWILIO_ENABLED=True
```

**With your actual values:**

```bash
# Twilio SMS Configuration
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your_auth_token_here
TWILIO_PHONE_NUMBER=+1234567890
TWILIO_ENABLED=True
```

---

## 🏃 Run Your App

### Option 1: Using Virtual Environment (Recommended)

```bash
cd "WEBD"
source venv/bin/activate
python app.py
```

### Option 2: Using Python 3 Directly

```bash
cd "WEBD"
python3 app.py
```

You should see:
```
✅ Twilio service initialized successfully
 * Running on http://127.0.0.1:5001
```

---

## 📱 Test Real-Time OTP

### Method 1: Via Guest Management

1. Open your app: http://localhost:5001
2. Login to your account
3. Go to **Guests** section
4. Create or edit a guest with a phone number
5. Click **"Send OTP"** button
6. **Guest receives SMS instantly!** 📲
7. Enter OTP to verify

### Method 2: Via API (for developers)

**Send OTP:**
```bash
curl -X POST http://localhost:5001/guests/1/send-otp
```

**Verify OTP:**
```bash
curl -X POST http://localhost:5001/guests/1/verify-otp \
  -H "Content-Type: application/json" \
  -d '{"otp": "123456"}'
```

**Send Reminder:**
```bash
curl -X POST http://localhost:5001/guests/1/send-reminder
```

---

## 📋 Available Features

### 1. **Send OTP** 
Route: `POST /guests/<id>/send-otp`
- Generates 6-digit OTP
- Sends via SMS instantly
- Valid for 10 minutes

**SMS Example:**
```
Your OTP for Birthday Party is: 123456. 
Valid for 10 minutes. - Nexus Event Management
```

### 2. **Verify OTP**
Route: `POST /guests/<id>/verify-otp`
- Verifies user-entered OTP
- Marks phone as verified
- Updates RSVP status to "Accepted"

### 3. **Send Event Reminder**
Route: `POST /guests/<id>/send-reminder`
- Sends event details via SMS
- Includes date, time, location
- Professional formatting

**SMS Example:**
```
Hi John Doe!

Reminder: You're invited to Birthday Party

📅 Date: 25 Dec 2024
⏰ Time: 06:00 PM

We look forward to seeing you!
- Nexus Event Management
```

---

## 🔧 Troubleshooting

### ❌ "Twilio service is not enabled"
**Solution:** Check your `.env` file has correct credentials and `TWILIO_ENABLED=True`

### ❌ "The 'To' number is not a valid phone number"
**Solution:** 
- Phone must be exactly 10 digits
- Example: `9876543210` (correct)
- Don't use: `+91 98765 43210` or `(987) 654-3210`

### ❌ "Permission to send an SMS has not been enabled"
**Solution:** 
- **Trial accounts** can only send to **verified numbers**
- Go to: https://console.twilio.com/us1/develop/phone-numbers/manage/verified
- Add and verify the recipient's phone number
- OR upgrade to a paid account to send to any number

### ❌ ModuleNotFoundError: No module named 'twilio'
**Solution:**
```bash
cd "WEBD"
source venv/bin/activate
pip install -r requirements.txt
```

---

## 💰 Pricing

### Trial Account (Current)
- ✅ **$15 FREE credit**
- ✅ ~**500 SMS** in India
- ⚠️ Can only send to **verified phone numbers**
- ✅ Perfect for **development & testing**

### After Free Credit Runs Out
- Upgrade to **Pay-As-You-Go**
- **₹0.70 per SMS** in India (~$0.008)
- Send to **any number**
- No monthly fees

---

## 📊 Monitor Your SMS

View all sent messages:
👉 https://console.twilio.com/us1/monitor/logs/sms

See:
- ✅ Delivery status
- 📅 Timestamp
- 💰 Cost per message
- ⚠️ Error messages (if any)

---

## 🎨 Add UI Components (Optional)

Want to add OTP verification buttons to your guest pages?

Check the full guide: `TWILIO_SETUP_GUIDE.md` (Section: Frontend Integration)

---

## 📞 Support Links

- **Twilio Dashboard**: https://console.twilio.com/
- **Get Free Trial**: https://www.twilio.com/try-twilio
- **SMS Logs**: https://console.twilio.com/us1/monitor/logs/sms
- **Verify Phone Numbers**: https://console.twilio.com/us1/develop/phone-numbers/manage/verified
- **Pricing**: https://www.twilio.com/sms/pricing/in
- **Documentation**: https://www.twilio.com/docs/sms/quickstart/python

---

## ✨ What You Can Do Now

1. ✅ Send **real-time OTP** via SMS to guests
2. ✅ Verify **phone numbers** automatically
3. ✅ Send **event reminders** via SMS
4. ✅ Send **RSVP confirmations** automatically
5. ✅ Send **custom messages** to guests

---

## 🎉 You're All Set!

**MSG91 is completely gone. Twilio is ready to use!**

Just add your credentials to `.env` and start sending SMS! 🚀

Need help? Check `TWILIO_SETUP_GUIDE.md` for detailed documentation.
