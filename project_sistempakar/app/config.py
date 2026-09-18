import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'kunci_rahasia_super_aman'
    DB_HOST = 'localhost'
    DB_USER = 'root'
    DB_PASSWORD = ''
    DB_NAME = 'db_pakar_kulit'

