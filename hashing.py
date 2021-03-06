import uuid
import hashlib
 
def hash_password(password):
    salt = uuid.uuid4().hex
    return hashlib.sha512(password.encode() + salt.encode()).hexdigest() + ':' + salt


def check_password(hashed_password, user_password):
    password, salt = hashed_password.split(':')
    return password == hashlib.sha512(user_password.encode() + salt.encode()).hexdigest()
