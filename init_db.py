from backend.app.models import Base, User
from backend.app.models.database import engine, SessionLocal
from backend.app.config import settings

def init_database():
    # Initializing database with tables and users from settings
    print("Initializing database...")
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    print("Database tables created!")
    
    # Load users from settings
    default_users = settings.parsed_default_users
    
    if not default_users:
        print("No users found in configuration (DEFAULT_USERS)")
        return
    
    db = SessionLocal()
    try:
        users_created = 0
        users_skipped = 0
        
        for user_data in default_users:
            username = user_data.get('username') or user_data.get('name')
            if not username:
                continue
                
            existing_user = db.query(User).filter(
                User.username == username
            ).first()
            
            if existing_user:
                print(f"User '{username}' already exists - skipping")
                users_skipped += 1
                continue
            
            new_user = User(
                username=username,
                email=user_data.get('email', f"{username}@example.com"),
                full_name=user_data.get('full_name', username),
                role=user_data.get('role', 'hr')
            )
            # Assuming User model has set_password or hashed_password
            if hasattr(new_user, 'set_password'):
                new_user.set_password(user_data.get('password', 'changeme'))
            elif hasattr(new_user, 'hashed_password'):
                from backend.app.services.auth_service import get_password_hash
                new_user.hashed_password = get_password_hash(user_data.get('password', 'changeme'))
            
            db.add(new_user)
            users_created += 1
            print(f"Created user: {username} ({user_data.get('role', 'hr')})")
        
        db.commit()
        
        print(f"\nSummary:")
        print(f"   • Users created: {users_created}")
        print(f"   • Users skipped: {users_skipped}")
        print(f"   • Total users processed: {len(default_users)}")
        
    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    init_database()
