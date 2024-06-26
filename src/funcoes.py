from passlib.context import CryptContext 

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Funcoes(object):
    
    @staticmethod
    def verify_password(plain_password, password):
        return pwd_context.verify(plain_password, password)
    
    @staticmethod
    def get_password_hash(password):
        return pwd_context.hash(password)