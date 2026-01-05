#!/usr/bin/env python3
"""
Setup script to create the first admin user.
This script can be run to bootstrap an admin user in the database.

Usage:
    python setup_admin.py
    python setup_admin.py --email admin@example.com --password admin123 --name "Admin User"
"""

import argparse
import sys
from app import create_app
from app.extensions import db
from app.models.user import User
from app.repositories.user_repository import UserRepository

def create_admin_user(email: str, password: str, name: str = "Admin User"):
    """Create an admin user in the database"""
    app = create_app()
    
    with app.app_context():
        # Ensure tables exist
        db.create_all()
        
        user_repo = UserRepository()
        
        # Check if admin user already exists
        existing_user = user_repo.get_by_email(email)
        if existing_user:
            if existing_user.is_admin():
                print(f"❌ Admin user with email '{email}' already exists!")
                return False
            else:
                # Upgrade existing user to admin
                print(f"⚠️  User '{email}' exists but is not an admin. Upgrading to admin...")
                existing_user.role = "admin"
                db.session.commit()
                print(f"✅ User '{email}' has been upgraded to admin!")
                return True
        
        # Create new admin user
        try:
            user = User(name=name, email=email, role="admin")
            user.set_password(password)
            user = user_repo.add(user)
            print(f"✅ Admin user created successfully!")
            print(f"   Email: {user.email}")
            print(f"   Name: {user.name}")
            print(f"   Role: {user.role}")
            print(f"   ID: {user.id}")
            return True
        except Exception as e:
            print(f"❌ Error creating admin user: {e}")
            return False

def main():
    parser = argparse.ArgumentParser(description='Create the first admin user')
    parser.add_argument('--email', type=str, default='admin@example.com',
                       help='Admin user email (default: admin@example.com)')
    parser.add_argument('--password', type=str, default='admin123',
                       help='Admin user password (default: admin123)')
    parser.add_argument('--name', type=str, default='Admin User',
                       help='Admin user name (default: Admin User)')
    
    args = parser.parse_args()
    
    print("=" * 50)
    print("Admin User Setup Script")
    print("=" * 50)
    print(f"Email: {args.email}")
    print(f"Name: {args.name}")
    print("=" * 50)
    print()
    
    success = create_admin_user(args.email, args.password, args.name)
    
    if success:
        print()
        print("=" * 50)
        print("✅ Setup complete! You can now login with:")
        print(f"   Email: {args.email}")
        print(f"   Password: {args.password}")
        print("=" * 50)
        sys.exit(0)
    else:
        print()
        print("=" * 50)
        print("❌ Setup failed!")
        print("=" * 50)
        sys.exit(1)

if __name__ == "__main__":
    main()

