# PANDUAN DEPLOY KE RAILWAY DENGAN MYSQL

## Prasyarat
- Akun Railway (https://railway.app)
- Git installed
- Repository di GitHub

## Langkah-Langkah Deploy

### 1. Persiapan Lokal
```powershell
# Pastikan dependencies terinstall
pip install -r requirements.txt

# Copy .env.example ke .env (untuk development lokal)
Copy-Item .env.example .env

# Sesuaikan .env dengan config MySQL lokal Anda
# Edit .env:
# DB_USER=root
# DB_PASS=your_password
# DB_HOST=localhost
# DB_NAME=chatbot_db
```

### 2. Push ke GitHub
```powershell
git add .
git commit -m "Persiapan migration ke Railway dengan MySQL"
git push origin main
```

### 3. Setup di Railway Dashboard
1. Kunjungi https://railway.app/dashboard
2. Klik **"New Project"**
3. Pilih **"Deploy from GitHub"** dan connect dengan akun GitHub Anda
4. Pilih repository `Chatbot-Bimbingan-Akademik`
5. Klik **"Deploy"** untuk membuat service Flask

### 4. Tambahkan MySQL Plugin
1. Di Railway dashboard, klik **"Add Service"**
2. Pilih **"MySQL"**
3. Railway otomatis akan membuat database dan set `DATABASE_URL` env variable

### 5. Konfigurasi Service Flask
Setelah MySQL plugin ditambah, Railway otomatis set `DATABASE_URL`. Pastikan:

1. Di tab "Variables", cek apakah `DATABASE_URL` sudah ada:
   - Jika ada → OK, tidak perlu perubahan
   - Jika tidak → set manual (copy dari MySQL plugin details)

2. Set variable lainnya (opsional):
   ```
   FLASK_ENV=production
   SECRET_KEY=your-strong-secret-key-here
   ```

3. Klik **"Deploy"** untuk deploy ulang dengan env vars baru

### 6. Jalankan Database Initialization (Jika Perlu)
Jika tabel belum terbuat, buka Railway console dan jalankan:
```bash
python -c "from app import app; from config import db; app.app_context().push(); db.create_all(); print('✅ Database initialized')"
```

Atau set Railway environment `INIT_DB=true` dan modifikasi `app.py`:
```python
if __name__ == "__main__":
    with app.app_context():
        if os.getenv('INIT_DB'):
            db.create_all()
            print("✅ Database initialized")
        db.create_all()  # Always create tables
    app.run(debug=True, port=5000)
```

### 7. Cek Deployment
1. Di Railway, klik service Flask
2. Lihat "Deployments" tab untuk status build
3. Jika Build Status = **Success** → OK
4. Klik "Public URL" untuk akses aplikasi

### 8. Troubleshoot

**Error: "Module 'app' has no attribute 'app'"**
- Pastikan di `Procfile` benar: `web: gunicorn app:app`
- Pastikan `app.py` export `app` object

**Error: "Database connection failed"**
- Cek apakah `DATABASE_URL` sudah set di Railway variables
- Pastikan MySQL plugin sudah added
- Test koneksi lokal dulu dengan `.env`

**Error: "Table tidak ada"**
- Jalankan command initialization di step 6

## Struktur File untuk Railway

```
.
├── app.py                    # Entry point Flask
├── config.py                 # Baca DATABASE_URL dari env (SUDAH DIUPDATE)
├── requirements.txt          # Dependencies (SUDAH DITAMBAHKAN: gunicorn, pymysql, python-dotenv)
├── Procfile                  # Entry point untuk Railway (SUDAH DIBUAT)
├── .env.example              # Template env vars (SUDAH DIBUAT)
├── .env                       # Lokal env config (SUDAH DIBUAT - jangan push!)
├── .gitignore                # Pastikan ada entry: .env
├── backend/
│   ├── db/
│   │   ├── init_db.py        # Database initialization
│   │   ├── models.py         # SQLAlchemy models
│   │   └── __pycache__/
│   ├── routes/
│   │   ├── admin_routes.py
│   │   ├── chatbot_routes.py
│   │   ├── user_routes.py
│   │   └── __pycache__/
│   ├── utils/
│   │   ├── load_data.py
│   │   ├── pdf_parser.py
│   │   ├── retrain_model.py
│   │   └── __pycache__/
│   ├── model/
│   │   └── main_model.h5
│   ├── static/
│   └── uploads/
├── frontend/                 # HTML files (Railway akan serve via Flask)
└── README.md

PENTING: Tambahkan ke `.gitignore`:
```
.env
__pycache__/
*.pyc
.DS_Store
node_modules/
```

## Catatan Penting

1. **DATABASE_URL Format**: 
   - Railway MySQL menghasilkan: `mysql+pymysql://user:pass@host:port/db`
   - Aplikasi Anda sudah dikonfigurasi untuk parse ini

2. **Password di URL**: 
   - Railway auto-handle URL encoding
   - Pastikan `config.py` gunakan `quote_plus()` jika password ada karakter spesial

3. **Backup Data**:
   - Sebelum migrasi, backup data MySQL lokal:
     ```powershell
     mysqldump -u root chatbot_db > backup.sql
     ```
   - Setelah Railway running, import data jika perlu

4. **Skala & Cost**:
   - Railway free tier: cukup untuk development
   - Untuk production: monitor usage di Railway dashboard

## Testing Lokal Sebelum Deploy

```powershell
# Install dependencies
pip install -r requirements.txt

# Pastikan MySQL lokal running
# Edit .env dengan config lokal Anda

# Jalankan Flask dev server
python app.py

# Buka: http://localhost:5000
```

Jika semua OK di lokal → siap deploy ke Railway!

## Contoh Railway Deployment Flow

```
GitHub Repo
    ↓
Railway Auto-Deploy (trigger push)
    ↓
Build Stage (install requirements)
    ↓
MySQL Plugin Connected (DATABASE_URL set)
    ↓
Start Flask with gunicorn
    ↓
App Running di Railway!
```

## Link Referensi
- Railway Docs: https://docs.railway.app
- Railway MySQL Plugin: https://docs.railway.app/databases/mysql
- Python Flask on Railway: https://docs.railway.app/guides/flask

---

Pertanyaan? Hubungi Railway support atau update documentation.
