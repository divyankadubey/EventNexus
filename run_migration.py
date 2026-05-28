"""
Run database migration to add check-in fields
"""

import os
from dotenv import load_dotenv
import pymysql

# Load environment variables
load_dotenv()

# Database connection
conn = pymysql.connect(
    host='localhost',
    user='root',
    password='',  # Your MySQL password
    database='event_management'
)

cursor = conn.cursor()

print("🔧 Running Database Migration...")
print("=" * 50)

try:
    # Check if columns already exist
    cursor.execute("SHOW COLUMNS FROM guests LIKE 'qr_token'")
    if cursor.fetchone():
        print("✅ Migration already applied!")
    else:
        # Add check-in columns
        print("📝 Adding qr_token column...")
        cursor.execute("""
            ALTER TABLE guests 
            ADD COLUMN qr_token VARCHAR(100) AFTER dietary_requirements
        """)
        
        print("📝 Adding checked_in column...")
        cursor.execute("""
            ALTER TABLE guests 
            ADD COLUMN checked_in BOOLEAN DEFAULT FALSE AFTER qr_token
        """)
        
        print("📝 Adding check_in_time column...")
        cursor.execute("""
            ALTER TABLE guests 
            ADD COLUMN check_in_time DATETIME AFTER checked_in
        """)
        
        print("📝 Creating indexes...")
        cursor.execute("CREATE INDEX idx_qr_token ON guests(qr_token)")
        cursor.execute("CREATE INDEX idx_checked_in ON guests(checked_in)")
        
        conn.commit()
        print("\n✅ Migration completed successfully!")
        
except Exception as e:
    print(f"❌ Error: {str(e)}")
    conn.rollback()
finally:
    cursor.close()
    conn.close()

print("\n🎉 Database is ready for QR code check-in system!")
