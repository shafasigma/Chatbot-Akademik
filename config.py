import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote_plus

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)

# ===== DATABASE CONFIGURATION =====
# Coba baca DATABASE_URL dari env (Railway menyediakan ini)
# Jika tidak ada, gunakan variabel lokal atau fallback default
DATABASE_URL = os.getenv('DATABASE_URL')

if not DATABASE_URL:
    # Fallback ke MySQL lokal (env vars atau hardcoded default)
    DB_USER = os.getenv('DB_USER', 'root')
    DB_PASS = os.getenv('DB_PASS', '')  # Kosong jika tidak ada password
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = os.getenv('DB_PORT', '3306')
    DB_NAME = os.getenv('DB_NAME', 'chatbot_db')
    
    # URL-encode password jika ada karakter spesial
    if DB_PASS:
        DB_PASS = quote_plus(DB_PASS)
    
    # Gunakan pymysql (kompatibel dengan Railway)
    DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = os.getenv('SECRET_KEY', 'change_this_secret')

db = SQLAlchemy(app)
MODEL_DIR = os.path.join(BASE_DIR, "model")
UPLOADS_DIR = os.path.join(BASE_DIR, "uploads")
os.makedirs(MODEL_DIR, exist_ok=True)
os.makedirs(os.path.join(UPLOADS_DIR, "datasets"), exist_ok=True)
os.makedirs(os.path.join(UPLOADS_DIR, "pdfs"), exist_ok=True)
