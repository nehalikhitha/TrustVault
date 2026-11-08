# 🔐 TrustVault – Secure Document Sharing & Audit Management

TrustVault is a Django-based web application designed to securely upload, manage, share, and access documents using role-based permissions and audit logging.

The application helps document owners control who can access their documents and what actions they are allowed to perform.

## 🚀 Features

- User registration and authentication.
- Role-based access control.
- Secure document upload and management.
- Document sharing with READ and EDIT permissions.
- Grant and revoke document permissions.
- Server-side authorization checks.
- Document download with access verification.
- Audit logging for important document activities.
- Notifications for document sharing and permission changes.
- Document search functionality.
- REST API support using Django REST Framework.

## 👥 User Roles

| Role | Description |
|---|---|
| ADMIN | Administrative management |
| OWNER | Uploads, manages, and shares documents |
| VIEWER | Accesses documents shared according to permissions |

## 🛠️ Technology Stack

- **Backend:** Python, Django
- **API:** Django REST Framework
- **Database:** SQLite (development)
- **Database Driver:** Psycopg
- **Environment Management:** Python dotenv
- **Frontend:** Django Templates, HTML, CSS

## 📁 Project Structure

```text
TrustVault/
│
├── accounts/
├── analytics/
├── audit/
├── config/
├── core/
├── documents/
├── notifications/
├── permissions/
├── search/
├── security/
│
├── media/
├── private_media/
├── manage.py
├── requirements.txt
├── README.md
├── THREATS.md
├── PROMPTS.md
└── .gitignore
```

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/nehalikhitha/TrustVault.git
cd TrustVault
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the virtual environment

**Windows PowerShell:**

```powershell
.\.venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure environment variables

Create a `.env` file in the project root directory.

```env
SECRET_KEY=your-generated-secret-key
DEBUG=True
```

Generate your own Django secret key. Never upload `.env` to GitHub.

### 6. Apply database migrations

```bash
python manage.py migrate
```

### 7. Start the development server

```bash
python manage.py runserver
