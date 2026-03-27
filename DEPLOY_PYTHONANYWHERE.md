# Deploy Django Portfolio on PythonAnywhere

This guide is specific to this project layout and settings.

## 1. Create account and web app

1. Sign in to PythonAnywhere.
2. Go to **Web** tab.
3. Click **Add a new web app**.
4. Choose:
   - Domain: `<your-username>.pythonanywhere.com`
   - Framework: **Manual configuration**
   - Python version: 3.11 (recommended for this project)

## 2. Open a Bash console and clone your project

In PythonAnywhere, open **Consoles -> Bash** and run:

```bash
git clone <your-repo-url> Portfolio
cd Portfolio
python3.11 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

If your repo is private, use a personal access token or upload files manually.

## 3. Set environment variables

In the same Bash console:

```bash
cd ~/Portfolio
cat > .env << 'EOF'
DJANGO_DEBUG=False
DJANGO_SECRET_KEY=<paste-a-strong-secret-key>
DJANGO_ALLOWED_HOSTS=<your-username>.pythonanywhere.com
DJANGO_CSRF_TRUSTED_ORIGINS=https://<your-username>.pythonanywhere.com
DJANGO_SECURE_SSL_REDIRECT=True
DJANGO_SESSION_COOKIE_SECURE=True
DJANGO_CSRF_COOKIE_SECURE=True
EOF
```

Generate a secret key quickly:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

## 4. Load .env from WSGI file

PythonAnywhere does not load `.env` automatically. Edit WSGI file from **Web -> WSGI configuration file** and use this content:

```python
import os
import sys
from pathlib import Path

project_home = '/home/<your-username>/Portfolio'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

env_file = Path(project_home) / '.env'
if env_file.exists():
    for raw in env_file.read_text().splitlines():
        line = raw.strip()
        if not line or line.startswith('#') or '=' not in line:
            continue
        key, value = line.split('=', 1)
        os.environ.setdefault(key.strip(), value.strip())

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

## 5. Configure static files mapping

In **Web -> Static files**, add:

- URL: `/static/`
- Directory: `/home/<your-username>/Portfolio/staticfiles`

## 6. Run migrations and collect static

Back in Bash:

```bash
cd ~/Portfolio
source .venv/bin/activate
python manage.py migrate
python manage.py collectstatic --noinput
```

(Optional admin user):

```bash
python manage.py createsuperuser
```

## 7. Set virtualenv and source path in Web tab

In **Web** tab set:

- Source code: `/home/<your-username>/Portfolio`
- Working directory: `/home/<your-username>/Portfolio`
- Virtualenv: `/home/<your-username>/Portfolio/.venv`

## 8. Reload and verify

1. Click **Reload** in Web tab.
2. Open `https://<your-username>.pythonanywhere.com`.
3. If errors appear, check:
   - **Web -> Error log**
   - **Web -> Server log**

## 9. Update workflow after new commits

Whenever you push changes:

```bash
cd ~/Portfolio
source .venv/bin/activate
git pull
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
```

Then click **Reload** in Web tab.
