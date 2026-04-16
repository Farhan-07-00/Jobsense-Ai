import mysql.connector
from mysql.connector import Error
from datetime import datetime
import config

class Database:
    def __init__(self):
        self.connection = None
    
    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=config.Config.MYSQL_HOST,
                user=config.Config.MYSQL_USER,
                password=config.Config.MYSQL_PASSWORD,
                database=config.Config.MYSQL_DATABASE,
                port=config.Config.MYSQL_PORT
            )
            return True
        except Error as e:
            print(f"Database connection error: {e}")
            return False
    
    def create_tables(self):
        cursor = self.connection.cursor()
        
        # Users table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100),
            email VARCHAR(100),
            resume_score INT,
            skills TEXT,
            predicted_jobs TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """)
        
        # Admin table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS admin (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) UNIQUE,
            password VARCHAR(255)
        )
        """)
        
        # Insert default admin (username: admin, password: admin123)
        cursor.execute("""
        INSERT IGNORE INTO admin (username, password) 
        VALUES ('admin', 'admin123')
        """)
        
        self.connection.commit()
        cursor.close()
    
    def save_resume_analysis(self, name, email, score, skills, jobs):
        cursor = self.connection.cursor()
        cursor.execute("""
        INSERT INTO users (name, email, resume_score, skills, predicted_jobs)
        VALUES (%s, %s, %s, %s, %s)
        """, (name, email, score, ','.join(skills), ','.join(jobs)))
        self.connection.commit()
        cursor.close()
    
    def get_all_analyses(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users ORDER BY timestamp DESC")
        results = cursor.fetchall()
        cursor.close()
        return results
    
    def get_admin_credentials(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT username, password FROM admin")
        result = cursor.fetchone()
        cursor.close()
        return result