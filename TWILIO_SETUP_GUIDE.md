# 📱 Twilio SMS Integration Guide

Complete setup guide for using **Twilio SMS** in your Event Management System (replacing MSG91).

---

## 🎯 What's Implemented

✅ **Twilio SMS Service** (`twilio_service.py`)  
✅ **OTP Generation & Verification**  
✅ **Guest Phone Verification**  
✅ **Event Reminder SMS**  
✅ **RSVP Confirmation SMS**  
✅ **3 New API Routes** in `app.py`

---

## 🚀 SETUP INSTRUCTIONS

### Step 1: Sign Up for Twilio (FREE $15 Credit)

1. Go to: **https://www.twilio.com/try-twilio**
2. Sign up with your email
3. Verify your phone number
4. You'll get **$15 FREE credit** (~500 SMS in India)

### Step 2: Get Your Twilio Credentials

1. **Login to Twilio Console**: https://console.twilio.com/
2. Go to **Dashboard**
3. Copy the following:
   - **Account SID** (starts with `AC...`)
   - **Auth Token** (click to reveal)

### Step 3: Get a Twilio Phone Number

1. In Twilio Console, go to: **Phone Numbers** → **Manage** → **Buy a number**
2. Select **Country: United States** (for trial)
3. Click **Search**
4. Choose a number and click **Buy**
5. Copy your Twilio phone number (format: `+1234567890`)

### Step 4: Configure Environment Variables

Open your `.env` file and update the Twilio credentials:

```bash
# Twilio SMS Configuration
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your_auth_token_here
TWILIO_PHONE_NUMBER=+1234567890
TWILIO_ENABLED=True
```

**Example:**
```bash
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your_auth_token_here
TWILIO_PHONE_NUMBER=+1234567890
TWILIO_ENABLED=True
```

### Optional: Use Multiple Twilio Numbers (Round-Robin)

If you have multiple Twilio numbers and want to rotate between them or provide fallback on failures, set:

```bash
# Comma-separated list of numbers
TWILIO_PHONE_NUMBERS=+15551234567, +15557654321, +15017122661
```

Notes:
- The app will pick the next number each time it sends an SMS (round‑robin).
- If sending fails from one number, it automatically tries the next number.
- If `TWILIO_PHONE_NUMBERS` isn't set, the app uses `TWILIO_PHONE_NUMBER`.

### Step 5: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- `twilio==8.10.0` (added to requirements.txt)
- All other existing dependencies

### Step 6: Test Twilio Service

Run the test script:

```bash
python twilio_service.py
```

You should see:
```
✅ Twilio service initialized successfully
Generated OTP: 123456
Account Info: {...}
```

### Step 7: Start Your Application

```bash
python app.py
```

---

## 📡 AVAILABLE FEATURES

### 1. **Send OTP to Guest**
Sends a 6-digit OTP via SMS for phone verification.

**Route:** `POST /guests/<id>/send-otp`

**Example Request:**
```javascript
fetch('/guests/1/send-otp', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'}
})
.then(response => response.json())
.then(data => {
    console.log(data);
    // {success: true, message: "OTP sent to 9876543210", message_sid: "SM..."}
});
```

**SMS Format:**
```
Your OTP for Birthday Party is: 123456. Valid for 10 minutes. - Nexus Event Management
```

---

### 2. **Verify Guest OTP**
Verifies the OTP entered by the guest.

**Route:** `POST /guests/<id>/verify-otp`

**Example Request:**
```javascript
fetch('/guests/1/verify-otp', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({otp: '123456'})
})
.then(response => response.json())
.then(data => {
    console.log(data);
    // {success: true, message: "OTP verified successfully!"}
});
```

---

### 3. **Send Event Reminder**
Sends an event reminder SMS to guests.

**Route:** `POST /guests/<id>/send-reminder`

**Example Request:**
```javascript
fetch('/guests/1/send-reminder', {
    method: 'POST'
})
.then(response => response.json())
.then(data => {
    console.log(data);
});
```

**SMS Format:**
```
Hi John Doe!

Reminder: You're invited to Birthday Party

📅 Date: 25 Dec 2024
⏰ Time: 06:00 PM

We look forward to seeing you!
- Nexus Event Management
```

---

## 🎨 FRONTEND INTEGRATION

### Add OTP Verification to Guest Templates

#### Update `templates/guests/detail.html` or `edit.html`:

```html
<!-- OTP Verification Section -->
<div class="card mt-4">
    <div class="card-header bg-primary text-white">
        <h5 class="mb-0">📱 Phone Verification</h5>
    </div>
    <div class="card-body">
        {% if guest.phone %}
            {% if not guest.otp_verified %}
                <div class="alert alert-warning">
                    ⚠️ Phone number not verified
                </div>
                <button onclick="sendOTP({{ guest.id }})" 
                        class="btn btn-primary" id="sendOtpBtn-{{ guest.id }}">
                    📨 Send OTP
                </button>
                
                <!-- OTP Input (hidden initially) -->
                <div id="otp-section-{{ guest.id }}" style="display: none;" class="mt-3">
                    <label class="form-label">Enter OTP</label>
                    <div class="input-group">
                        <input type="text" 
                               id="otp-input-{{ guest.id }}" 
                               class="form-control" 
                               placeholder="Enter 6-digit OTP" 
                               maxlength="6"
                               pattern="[0-9]{6}">
                        <button onclick="verifyOTP({{ guest.id }})" 
                                class="btn btn-success">
                            ✅ Verify
                        </button>
                    </div>
                    <small class="text-muted">OTP valid for 10 minutes</small>
                </div>
            {% else %}
                <div class="alert alert-success">
                    ✅ Phone number verified!
                </div>
            {% endif %}
            
            <!-- Send Reminder Button -->
            <button onclick="sendReminder({{ guest.id }})" 
                    class="btn btn-info mt-2">
                🔔 Send Event Reminder
            </button>
        {% else %}
            <div class="alert alert-secondary">
                No phone number provided
            </div>
        {% endif %}
    </div>
</div>

<script>
function sendOTP(guestId) {
    const btn = document.getElementById(`sendOtpBtn-${guestId}`);
    btn.disabled = true;
    btn.innerHTML = '<span class="spinner-border spinner-border-sm"></span> Sending...';
    
    fetch(`/guests/${guestId}/send-otp`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'}
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('✅ OTP sent successfully! Check your phone.');
            document.getElementById(`otp-section-${guestId}`).style.display = 'block';
            btn.innerHTML = '📨 Resend OTP';
        } else {
            alert('❌ Error: ' + data.message);
            btn.innerHTML = '📨 Send OTP';
        }
        btn.disabled = false;
    })
    .catch(error => {
        alert('❌ Error sending OTP');
        btn.disabled = false;
        btn.innerHTML = '📨 Send OTP';
    });
}

function verifyOTP(guestId) {
    const otp = document.getElementById(`otp-input-${guestId}`).value;
    
    if (!otp || otp.length !== 6) {
        alert('Please enter a valid 6-digit OTP');
        return;
    }
    
    fetch(`/guests/${guestId}/verify-otp`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({otp: otp})
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('✅ Phone verified successfully!');
            location.reload();
        } else {
            alert('❌ ' + data.message);
        }
    })
    .catch(error => {
        alert('❌ Error verifying OTP');
    });
}

function sendReminder(guestId) {
    if (!confirm('Send event reminder to this guest?')) return;
    
    fetch(`/guests/${guestId}/send-reminder`, {
        method: 'POST'
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('✅ Reminder sent successfully!');
        } else {
            alert('❌ ' + data.message);
        }
    })
    .catch(error => {
        alert('❌ Error sending reminder');
    });
}
</script>
```

---

## 💻 PYTHON API USAGE

### Send OTP Programmatically

```python
from twilio_service import twilio_service

# Generate OTP
otp = twilio_service.generate_otp()

# Send OTP via SMS
success, message, message_sid = twilio_service.send_otp(
    phone='9876543210',
    otp=otp,
    event_name='Birthday Party'
)

if success:
    print(f"OTP sent! Message SID: {message_sid}")
else:
    print(f"Failed: {message}")
```

### Send Custom SMS

```python
success, message, message_sid = twilio_service.send_sms(
    phone='9876543210',
    message='Your custom message here'
)
```

### Send Event Reminder

```python
success, message, message_sid = twilio_service.send_event_reminder(
    phone='9876543210',
    guest_name='John Doe',
    event_name='Birthday Party',
    event_date='25 Dec 2024',
    event_time='06:00 PM'
)
```

### Send RSVP Confirmation

```python
success, message, message_sid = twilio_service.send_rsvp_confirmation(
    phone='9876543210',
    guest_name='John Doe',
    event_name='Birthday Party',
    rsvp_status='Accepted'
)
```

### Verify OTP

```python
from datetime import datetime

is_valid, message = twilio_service.verify_otp(
    stored_otp='123456',
    user_otp='123456',
    created_at=datetime.utcnow(),
    expiry_minutes=10
)

if is_valid:
    print("OTP verified!")
else:
    print(f"Verification failed: {message}")
```

---

## 🔧 TROUBLESHOOTING

### Issue 1: "Twilio service is not enabled or configured"

**Solution:**
- Check your `.env` file has correct credentials
- Make sure `TWILIO_ENABLED=True`
- Restart your Flask application

### Issue 2: "The 'To' number is not a valid phone number"

**Solution:**
- Make sure phone number is exactly 10 digits
- No spaces or special characters
- Example: `9876543210` (correct) vs `+91 98765 43210` (wrong)

### Issue 3: "Permission to send an SMS has not been enabled"

**Solution:**
- **Trial Account Limitation**: You can only send SMS to verified phone numbers
- To send to unverified numbers, upgrade to a paid account
- Or, verify the recipient's phone in Twilio Console: **Phone Numbers** → **Verified Caller IDs**

### Issue 4: "Authenticate" error

**Solution:**
- Double-check your `TWILIO_ACCOUNT_SID` and `TWILIO_AUTH_TOKEN`
- Make sure there are no extra spaces
- Generate a new Auth Token if needed

---

## 💰 PRICING

### Trial Account (Current)
- **$15 FREE credit**
- ~500 SMS in India (₹3 per SMS ≈ $0.03)
- Can only send to verified numbers
- Perfect for development and testing

### Pay-As-You-Go (When you upgrade)
- No monthly fees
- **₹0.70 per SMS in India** (~$0.008)
- Send to any number
- Pricing: https://www.twilio.com/sms/pricing/in

### Recommendation
- Use **trial credit for development**
- Upgrade when you launch to production
- With $15, you can test with ~500 messages

---

## 📊 MONITORING & LOGS

### View SMS Logs in Twilio Console

1. Go to: https://console.twilio.com/us1/monitor/logs/sms
2. See all sent messages with:
   - Status (delivered, sent, failed)
   - Timestamp
   - Cost
   - Error messages (if any)

### Check Account Balance

```python
info = twilio_service.get_account_info()
print(info)
```

---

## 🌍 INTERNATIONAL SMS

To send SMS to other countries, modify `_format_phone_number()` in `twilio_service.py`:

```python
def _format_phone_number(self, phone, country_code='+91'):
    """Format phone number with country code"""
    phone = ''.join(filter(str.isdigit, phone))
    
    if not phone.startswith('+'):
        if len(phone) == 10:
            phone = f'{country_code}{phone}'
    
    return phone
```

**Examples:**
- India: `+919876543210`
- USA: `+15551234567`
- UK: `+447911123456`

---

## 🎯 TESTING CHECKLIST

- [ ] Twilio credentials configured in `.env`
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Test service: `python twilio_service.py`
- [ ] Application starts without errors
- [ ] Send OTP to verified number works
- [ ] OTP verification works
- [ ] Event reminder SMS works
- [ ] Check Twilio logs for delivery status

---

## 🔗 USEFUL LINKS

- **Twilio Console**: https://console.twilio.com/
- **Get Free Credit**: https://www.twilio.com/try-twilio
- **SMS Logs**: https://console.twilio.com/us1/monitor/logs/sms
- **Pricing**: https://www.twilio.com/sms/pricing
- **Documentation**: https://www.twilio.com/docs/sms/quickstart/python
- **Verify Phone**: https://console.twilio.com/us1/develop/phone-numbers/manage/verified

---

## ✅ SUMMARY

You've successfully replaced MSG91 with Twilio! 🎉

**What's working:**
- ✅ OTP generation and sending via SMS
- ✅ OTP verification
- ✅ Event reminders
- ✅ RSVP confirmations
- ✅ Custom SMS messages

**Next steps:**
1. Get Twilio account and credentials
2. Update `.env` with your credentials
3. Test with verified phone numbers
4. Upgrade account when ready for production

**Free tier gives you:**
- $15 credit
- ~500 SMS messages
- Perfect for development

---

Need help? Check the troubleshooting section or Twilio documentation! 🚀
