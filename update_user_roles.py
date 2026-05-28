#!/usr/bin/env python3
"""
Script to update user roles in the database
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db, User
from werkzeug.security import generate_password_hash

def update_user_roles():
    """Update existing users and create admin account if needed"""
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
        users_without_role = User.query.filter(User.role.is_(None)).all()
        for user in users_without_role:
            user.role = 'User'
            user.is_active = True
        
        if users_without_role:
            print(f"✅ Updated {len(users_without_role)} users to 'User' role")
        
        # Commit all changes
        db.session.commit()
        print("✅ Database roles updated successfully!")

if __name__ == '__main__':
    update_user_roles()
