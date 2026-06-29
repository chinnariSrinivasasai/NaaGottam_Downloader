# Naa Gottam Downloader

A robust, full-stack Django web application designed to fetch and analyze YouTube video metadata and download streams. By utilizing advanced `yt-dlp` configurations, this application seamlessly integrates with local browser authentication contexts to safely bypass modern bot-detection walls (such as PO Tokens) using a residential network footprint. It features an interactive UI, comprehensive download configuration options, database historical tracking, and a secure configuration path for local internet tunneling.

---

## 🚀 Features

* **Advanced Extraction Engine:** Powered by `yt-dlp` with automated native browser cookie database mapping (`cookiesfrombrowser`) to execute authenticated network handshakes.
* **Persistent Tracking:** Built-in history logger using Django ORM to systematically record query metadata, requested stream qualities, and optional asset parameters (thumbnails/subtitles).
* **Production-Ready Architecture:** Equipped with `WhiteNoise` middleware for high-performance, self-contained static asset delivery.
* **Tunneling Deployment Matrix:** Pre-configured security policies supporting instantaneous remote exposure via secure tunnels like `ngrok` without compromising CSRF or host integrity header validations.

---

## 🛠️ System Requirements & Architecture

* **Framework:** Django 5.x / 6.x
* **Core Engine:** `yt-dlp` (Python-native library wrapper)
* **Database:** SQLite3 (Default development configuration)
* **Authentication Context:** An active browser session (Microsoft Edge, Google Chrome, Brave, or Firefox) logged into a valid YouTube account on the host machine.

---

## ⚙️ Installation & Local Setup

Follow these steps to deploy the application inside a localized virtual environment:

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/naagottam-downloader.git
cd naagottam-downloader

```

### 2. Configure Virtual Environment

Create and activate an isolated Python environment:

```bash
# Initialize the virtual environment
python -m venv venv

# Activate on Windows:
.\venv\Scripts\activate

# Activate on macOS/Linux:
source venv/bin/activate

```

### 3. Install Required Dependencies

Ensure your local dependencies are updated to avoid parsing exceptions:

```bash
pip install -r requirements.txt

```

### 4. Apply Database Migrations & Assets

Run schema initializations and consolidate static structural files:

```bash
python manage.py migrate
python manage.py collectstatic --no-input

```

### 5. Launch the Application Server

```bash
python manage.py runserver

```

The application will boot up at `http://127.0.0.1:8000/`.

---

## 🌐 Setting Up Remote Access (via ngrok)

To securely expose this local service to external endpoints or include it as a functional component in portfolios, leverage the integrated tunnel configurations.

1. Launch a separate terminal window and instantiate a standard HTTP tunnel targeting the active Django portal port:
```bash
ngrok http 8000

```


2. Copy the secure public address provided by the output forwarding registry (e.g., `https://xxxx-xx-xx.ngrok-free.app`).
3. The application will dynamically interface with the host restrictions defined inside `settings.py` to process requests globally:
```python
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '.ngrok-free.app']
CSRF_TRUSTED_ORIGINS = ['https://*.ngrok-free.app']

```



---

## 🗂️ Core Architecture & Code Review

The core controller handling stream resolution abstracts extraction complexity by executing an un-isolated extraction sweep matching local browser instances:

```python
ydl_opts = {
    "format": "best[ext=mp4]/best",
    "quiet": True,
    "noplaylist": True,
    # Pulls session authentication directly from active local processes
    "cookiesfrombrowser": ("edge",), 
}

```

> ⚠️ **Development Note:** For uninterrupted file access operations, ensure your selected target browser (e.g., Microsoft Edge or Google Chrome) is completely closed or has released its SQLite user database lock immediately prior to running queries.
