#!/usr/bin/env python3
"""
Test Twilio Configuration and Account Status
"""

from twilio_service import twilio_service
import os
from dotenv import load_dotenv

load_dotenv()

def test_twilio_config():
    print("🔧 Testing Twilio Configuration")
    print("=" * 50)
    
    # Check environment variables
    account_sid = os.getenv('TWILIO_ACCOUNT_SID')
    auth_token = os.getenv('TWILIO_AUTH_TOKEN')
    phone_number = os.getenv('TWILIO_PHONE_NUMBER')
    enabled = os.getenv('TWILIO_ENABLED')
    
    print(f"Account SID: {account_sid[:10]}...")
    print(f"Auth Token: {auth_token[:10]}...")
    print(f"Phone Number: {phone_number}")
    print(f"Enabled: {enabled}")
    print()
    
    # Check service initialization
    if twilio_service.client:
        print("✅ Twilio client initialized successfully")
        
        # Get account info
        account_info = twilio_service.get_account_info()
        print(f"Account Info: {account_info}")
        
        # Test OTP generation
        otp = twilio_service.generate_otp()
        print(f"Generated OTP: {otp}")
        
        print("\n⚠️  TRIAL ACCOUNT LIMITATION:")
        print("Trial accounts can only send messages to verified phone numbers.")
        print("To fix this issue:")
        print("1. Go to: https://console.twilio.com/us1/develop/phone-numbers/manage/verified")
        print("2. Add and verify your phone number")  
        print("3. Or upgrade to a paid account")
        
    else:
        print("❌ Twilio client failed to initialize")
        print("Check your credentials in .env file")

if __name__ == '__main__':
    test_twilio_config()
