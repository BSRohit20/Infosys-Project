import json
import secrets
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import logging
from app.models.user import User, UserLogin, UserSession, CustomerProfile

logger = logging.getLogger(__name__)

class AuthService:
    def __init__(self):
        self.users_data = self._load_users()
        self.active_sessions: Dict[str, UserSession] = {}
    
    def _load_users(self) -> list:
        """Load users from JSON file"""
        try:
            # Try comprehensive users first, fall back to original
            try:
                with open('app/data/comprehensive_users.json', 'r') as f:
                    return json.load(f)
            except FileNotFoundError:
                with open('app/data/users.json', 'r') as f:
                    return json.load(f)
        except FileNotFoundError:
            return []
    
    def authenticate_user(self, username: str, password: str) -> Optional[User]:
        """Authenticate user with username and password"""
        for user_data in self.users_data:
            if (user_data['username'] == username and 
                user_data.get('password_hash') == password):  # In real app, use proper password hashing
                
                user = User(**{k: v for k, v in user_data.items() if k != 'password_hash'})
                return user
        return None
    
    def create_session(self, user: User) -> UserSession:
        """Create a new user session"""
        session_token = secrets.token_urlsafe(32)
        expires_at = datetime.utcnow() + timedelta(hours=24)
        
        session = UserSession(
            user_id=user.user_id,
            username=user.username,
            role=user.role,
            session_token=session_token,
            expires_at=expires_at
        )
        
        self.active_sessions[session_token] = session
        return session
    
    def get_user_from_session(self, session_token: str) -> Optional[User]:
        """Get user from session token"""
        logger.info(f"🔍 Looking for session: {session_token}")
        logger.info(f"🔍 Active sessions: {list(self.active_sessions.keys())}")
        
        if session_token in self.active_sessions:
            session = self.active_sessions[session_token]
            logger.info(f"🔍 Found session for user: {session.user_id}")
            if datetime.utcnow() < session.expires_at:
                # Find user data
                for user_data in self.users_data:
                    if user_data['user_id'] == session.user_id:
                        user = User(**{k: v for k, v in user_data.items() if k != 'password_hash'})
                        logger.info(f"✅ Session valid for user: {user.username}")
                        return user
                logger.warning(f"⚠️ User data not found for session user_id: {session.user_id}")
            else:
                # Session expired
                logger.info(f"⏰ Session expired for user: {session.user_id}")
                del self.active_sessions[session_token]
        else:
            logger.info(f"❌ Session not found: {session_token}")
        return None
    
    def logout_user(self, session_token: str) -> bool:
        """Logout user by removing session"""
        if session_token in self.active_sessions:
            del self.active_sessions[session_token]
            return True
        return False
    
    def create_user(self, user_data: dict) -> Optional[User]:
        """Create a new user and save to users.json"""
        try:
            # Generate a new user ID
            if user_data.get('role') == 'customer':
                # Count existing guest users to generate next ID
                guest_count = sum(1 for user in self.users_data if user.get('role') == 'customer')
                user_id = f"guest_{guest_count + 1:03d}"
                
                # Create complete user data
                new_user = {
                    "user_id": user_id,
                    "username": user_data.get('username').lower(),  # Ensure lowercase
                    "email": user_data.get('email'),
                    "role": "customer",
                    "first_name": user_data.get('first_name'),
                    "last_name": user_data.get('last_name'),
                    "created_at": datetime.utcnow().isoformat(),
                    "last_login": None,
                    "is_active": True,
                    "password_hash": user_data.get('password'),
                    "guest_id": user_id,
                    "loyalty_tier": user_data.get('loyalty_tier', 'Standard')
                }
                
                # Add to in-memory data
                self.users_data.append(new_user)
                
                # Save to file
                try:
                    import os
                    # Use environment-aware path handling
                    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                    users_file = os.path.join(base_dir, 'data', 'users.json')
                    
                    # Ensure directory exists
                    data_dir = os.path.dirname(users_file)
                    if not os.path.exists(data_dir):
                        os.makedirs(data_dir)
                        
                    logger.info(f"Saving user data to {users_file}")
                    
                    with open(users_file, 'w') as f:
                        json.dump(self.users_data, f, indent=2)
                    logger.info(f"User data saved successfully")
                except Exception as e:
                    logger.error(f"Failed to write to users.json: {str(e)}")
                    logger.error(f"Current directory: {os.getcwd()}")
                    logger.error(f"Directory listing: {os.listdir(base_dir)}")
                    raise
                    
                # Return the created user (without password)
                return User(**{k: v for k, v in new_user.items() if k != 'password_hash'})
            
            return None
        except Exception as e:
            import traceback
            logger.error(f"Error creating user: {str(e)}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            return None
    
    def get_customer_profile(self, user_id: str) -> Optional[CustomerProfile]:
        """Get customer profile for customer users"""
        for user_data in self.users_data:
            if user_data['user_id'] == user_id and user_data['role'] == 'customer':
                return CustomerProfile(
                    user_id=user_id,
                    guest_id=user_data.get('guest_id'),
                    loyalty_number=user_data.get('loyalty_number'),
                    preferences=user_data.get('preferences', {}),
                    contact_info={
                        'email': user_data.get('email'),
                        'first_name': user_data.get('first_name'),
                        'last_name': user_data.get('last_name')
                    }
                )
        return None
    
    def is_admin(self, user: User) -> bool:
        """Check if user is admin"""
        return user.role == 'admin'
    
    def is_staff(self, user: User) -> bool:
        """Check if user is staff or admin"""
        return user.role in ['admin', 'staff']
    
    def is_customer(self, user: User) -> bool:
        """Check if user is customer"""
        return user.role == 'customer'

# Global auth service instance
auth_service = AuthService()
