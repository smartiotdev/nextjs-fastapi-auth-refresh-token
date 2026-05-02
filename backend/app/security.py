# app/security.py
import hashlib
import bcrypt

def hash_password(pwd: str) -> str:
    # Pre-hash with SHA256 to normalize length
    password_hash = hashlib.sha256(pwd.encode('utf-8')).hexdigest()
    
    # Generate salt and hash with bcrypt
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_hash.encode('utf-8'), salt)
    
    # Return as string for database storage
    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_pwd: str) -> bool:
    # Apply same SHA256 pre-hash as during registration
    password_hash = hashlib.sha256(plain_password.encode('utf-8')).hexdigest()
    
    # Verify with bcrypt (includes salt extraction automatically)
    return bcrypt.checkpw(
        password_hash.encode('utf-8'), 
        hashed_pwd.encode('utf-8')
    )