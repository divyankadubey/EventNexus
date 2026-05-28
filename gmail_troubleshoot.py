#!/usr/bin/env python3
"""
Gmail authentication troubleshooting script
"""

import smtplib
import os
from dotenv import load_dotenv

def troubleshoot_gmail():
    """Troubleshoot Gmail authentication issues"""
    
    load_dotenv()
    
    print("🔧 Gmail Authentication Troubleshooting")
    print("=" * 50)
    
    # Get current configuration
    username = os.getenv('MAIL_USERNAME')
    password = os.getenv('MAIL_PASSWORD')
    server = os.getenv('MAIL_SERVER')
    port = os.getenv('MAIL_PORT')
    
    print(f"📧 Username: {username}")
    print(f"🔐 Password: {'*' * len(password)}")
    print(f"🌐 Server: {server}:{port}")
    print("=" * 50)
    
    # Test 1: Basic SMTP connection
    print("\n1️⃣ Testing basic SMTP connection...")
    try:
        test_server = smtplib.SMTP(server, int(port))
        print("✅ SMTP connection successful")
        test_server.quit()
    except Exception as e:
        print(f"❌ SMTP connection failed: {e}")
        return False
    
    # Test 2: Authentication with current password
    print("\n2️⃣ Testing authentication with current password...")
    try:
        test_server = smtplib.SMTP(server, int(port))
        test_server.starttls()
        test_server.login(username, password)
        print("✅ Authentication successful!")
        test_server.quit()
        return True
    except smtplib.SMTPAuthenticationError as e:
        print(f"❌ Authentication failed: {e}")
        print("\n🔍 Possible causes:")
        print("   • 2FA not enabled")
        print("   • App password incorrect")
        print("   • Account locked")
        print("   • Less secure app access blocked")
        return False
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return False
    
    # Test 3: Manual email sending
    print("\n3️⃣ Testing manual email sending...")
    try:
        test_server = smtplib.SMTP(server, int(port))
        test_server.starttls()
        test_server.login(username, password)
        
        # Send test email
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart
        
        msg = MIMEMultipart()
        msg['From'] = username
        msg['To'] = 'samarthchoudhary26sept@gmail.com'
        msg['Subject'] = 'Test from Event Nexus System'
        body = "This is a test email from Event Nexus to verify Gmail authentication is working."
        msg.attach(MIMEText(body, 'plain'))
        
        test_server.send_message(username, 'samarthchoudhary26sept@gmail.com', msg.as_string())
        test_server.quit()
        
        print("✅ Test email sent successfully!")
        return True
    except Exception as e:
        print(f"❌ Email sending failed: {e}")
        return False

if __name__ == '__main__':
    troubleshoot_gmail()
