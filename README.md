# 🔗 URL Shortener (Full Stack)

A production-style URL shortener built with FastAPI, Redis, and a custom frontend.

## 🚀 Features

- 🔐 JWT Authentication
- ✂️ URL Shortening (custom + auto-generated)
- 📊 Click Analytics (async worker)
- ⚡ Redis Caching
- 👤 User-specific URLs
- ⏳ Expiring Links
- 🚫 Rate Limiting
- 🖥️ Interactive Frontend UI

---

## 🧠 Architecture

Client → FastAPI → Redis (cache)
                   ↓
                Queue → Worker → SQLite DB

---

## 🛠 Tech Stack

- Backend: FastAPI
- Database: SQLite
- Cache & Queue: Redis
- Auth: JWT (python-jose)
- Frontend: HTML + JavaScript

---

## ⚙️ How to Run

### 1. Clone repo
```bash
git clone https://github.com/YOUR_USERNAME/url-shortener.git
cd url-shortener

```
### Setup virtual environment
```bash
python -m venv venv
source venv/Scripts/activate   # Windows


```
### Install dependencies
```bash
pip install -r requirements.txt

```
### Start Redis
```bash
redis-server.exe

```
### Run backend
```bash
uvicorn app.main:app --reload

```
### Run worker
```bash
python -m app.worker

```
### Open frontend
```
Open frontend/index.html in browser

```
### Environment Variables

- SECRET_KEY=your_secret_key
- REDIS_HOST=localhost
- REDIS_PORT=your_port


### API Endpoints

- POST /login
- POST /shorten
- GET /{code}
- GET /stats/{code}
- GET /my-urls


### Demo Flow

- Login
- Shorten URL
- Open short link
- View analytics

### Future Improvements

- Docker support
- PostgreSQL migration
- UI dashboard (React)
- Rate limiting per user

### What I Learned

- Building scalable backend systems
- Designing async processing pipelines
- Implementing caching strategies
- Structuring production-ready APIs

