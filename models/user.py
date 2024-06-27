"""
user object model
"""
from models.base import Base
import models

class User(Base):
    name = "user"
    def __init__(self, name,email,  password):
        self.keys = ["id", "name", "created_at", "email", "password"]
        super().__init__()
        self.name = name
        self.email = email
        self.password = password
