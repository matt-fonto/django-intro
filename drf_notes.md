## Setup

### 1. Setup a virtual environment

```bash
mkdir drf_project && cd drf_project
python3 -m venv venv
source venv/bin/activate
```

### 2. Create `requirements.txt` + installation

```txt
django
djangorestframework
```

```bash
pip3 install -r requirements.txt
```

### 3. Create django project and an app

```bash
django-admin startproject [django-project] .
python manage.py startapp api
```
