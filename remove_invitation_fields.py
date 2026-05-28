"""
Remove invitation fields from database
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
    password='',
    database='event_management'
)

cursor = conn.cursor()

print("🔧 Removing Invitation Fields...")
print("=" * 50)

try:
    # Check if columns exist
    cursor.execute("SHOW COLUMNS FROM guests LIKE 'invitation_sent'")
    if cursor.fetchone():
        print("📝 Dropping invitation_sent column...")
        cursor.execute("ALTER TABLE guests DROP COLUMN invitation_sent")
        
        print("📝 Dropping invitation_sent_at column...")
        cursor.execute("ALTER TABLE guests DROP COLUMN invitation_sent_at")
        
        print("📝 Dropping rsvp_responded_at column...")
        cursor.execute("ALTER TABLE guests DROP COLUMN rsvp_responded_at")
        
        print("📝 Dropping index...")
        try:
            cursor.execute("DROP INDEX idx_invitation_sent ON guests")
        except:
            pass  # Index might not exist
        
        conn.commit()
        print("\n✅ Invitation fields removed successfully!")
    else:
        print("✅ Invitation fields already removed!")
        
except Exception as e:
    print(f"❌ Error: {str(e)}")
    conn.rollback()
finally:
    cursor.close()
    conn.close()

print("\n🎉 Feature #2 completely removed from database!")
