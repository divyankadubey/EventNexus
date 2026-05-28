#!/usr/bin/env python3
"""
Quick Gmail authentication verification
"""

import smtplib
import os
from dotenv import load_dotenv

load_dotenv()

def test_gmail_auth():
    """Test Gmail SMTP authentication directly"""
    
    # Get credentials from .env
    username = os.getenv('MAIL_USERNAME')
    password = os.getenv('MAIL_PASSWORD')
    
    print("🔧 Testing Gmail Authentication")
    print("=" * 40)
    print(f"📧 Username: {username}")
    print(f"🔐 Password: {'*' * len(password)}")
    print("=" * 40)
    
    try:
        # Test SMTP connection
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()  # Enable TLS
        server.login(username, password)
        
        print("✅ Gmail authentication successful!")
        print("🎉 Email system is ready to send!")
        
        # Test sending a simple email
        msg = "Subject: Test from Event Nexus\n\nThis is a test email from Event Nexus system."
        server.sendmail(username, "samarthchoudhary26sept@gmail.com", msg)
        print("✅ Test email sent to samarthchoudhary26sept@gmail.com!")
        
        server.quit()
        return True
        
    except smtplib.SMTPAuthenticationError as e:
        print(f"❌ Authentication failed: {e}")
        print("\n🔍 Possible causes:")
        print("1. 2-Step Verification not enabled")
        print("2. Using regular password instead of app password")
        print("3. App password format incorrect")
        print("4. Account locked due to failed attempts")
        return False
        
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return False

if __name__ == '__main__':
    test_gmail_auth()
