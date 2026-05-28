#!/usr/bin/env python3
"""
Script to migrate database schema for user roles
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db
import sqlite3

def migrate_database():
    """Add role and is_active columns to users table"""
    with app.app_context():
        # Get database path from app config
        db_path = app.config.get('SQLALCHEMY_DATABASE_URI', '').replace('sqlite:///', '')
        if not db_path.startswith('/'):
            # Relative path - add instance directory
            db_path = os.path.join(os.path.dirname(__file__), 'instance', db_path)
        
        if not db_path:
            print("❌ Could not determine database path")
            return
        
        print(f"📁 Database path: {db_path}")
        
        # Connect to SQLite database directly
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        try:
            # Check if role column exists
            cursor.execute("PRAGMA table_info(users)")
            columns = [column[1] for column in cursor.fetchall()]
            
            if 'role' not in columns:
                print("➕ Adding 'role' column to users table...")
                cursor.execute("ALTER TABLE users ADD COLUMN role TEXT DEFAULT 'User'")
                print("✅ Added 'role' column")
            else:
                print("ℹ️ 'role' column already exists")
            
            if 'is_active' not in columns:
                print("➕ Adding 'is_active' column to users table...")
                cursor.execute("ALTER TABLE users ADD COLUMN is_active BOOLEAN DEFAULT 1")
                print("✅ Added 'is_active' column")
            else:
                print("ℹ️ 'is_active' column already exists")
            
            # Commit the changes
            conn.commit()
            print("✅ Database migration completed successfully!")
            
        except Exception as e:
            print(f"❌ Migration error: {e}")
            conn.rollback()
        finally:
            conn.close()

def create_admin_user():
    """Create admin user after migration"""
    from app import User
    
    with app.app_context():
        # Check if admin user exists
        admin_user = User.query.filter_by(username='admin').first()
        
        if not admin_user:
            # Create admin user
            admin_user = User(
                username='admin',
                email='admin@eventmanagement.com',
                full_name='System Administrator',
                role='Admin',
                is_active=True
            )
            admin_user.set_password('admin123')
            db.session.add(admin_user)
            print("✅ Created admin user (username: admin, password: admin123)")
        else:
            # Update existing admin user to have Admin role
            admin_user.role = 'Admin'
            admin_user.is_active = True
            print("✅ Updated admin user role")
        
        # Update any existing users without roles to be 'User'
        try:
            users_without_role = User.query.filter(User.role.is_(None)).all()
            for user in users_without_role:
                user.role = 'User'
                user.is_active = True
            
            if users_without_role:
                print(f"✅ Updated {len(users_without_role)} users to 'User' role")
        except:
            print("ℹ️ No users without roles found")
        
        # Commit all changes
        db.session.commit()
        print("✅ User roles updated successfully!")

if __name__ == '__main__':
    print("🚀 Starting database migration...")
    migrate_database()
    print("\n👤 Creating admin user...")
    create_admin_user()
    print("\n🎉 Migration completed!")
