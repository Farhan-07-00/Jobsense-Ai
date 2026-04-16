import os

class Config:
    # Disable database temporarily
    MYSQL_HOST = "localhost"
    MYSQL_USER = "root"
    MYSQL_PASSWORD = "2312"
    MYSQL_DATABASE = "resume_analyser"
    MYSQL_PORT = 3306
    
    UPLOAD_FOLDER = "data/resumes"
    SECRET_KEY = "resume-app-123"