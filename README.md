# 📋 Attendance Management System

A comprehensive Django REST API for managing employee attendance using NFC cards and QR code scanners. Built with clean architecture, optimized queries, and role-based access control.

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- pip

### Installation

```bash
# Clone repository
git clone https://github.com/yourusername/attendance-management-system.git
cd attendance-management-system

#1️⃣ Docker Support (Optional)

docker-compose up -d --build


# 2️⃣Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations (optional - db.sqlite3 included)
python manage.py migrate

# Start development server
python manage.py runserver
```


**🔥 For Testing Convenience:** 
- `db.sqlite3` is included with pre-populated test data
- CORS is disabled (development mode only)
- Ready to test immediately after cloning

---

## 📚 API Documentation

Base URL: `http://206.162.244.143:7773/api/v1`

Postman Link : https://documenter.getpostman.com/view/40097709/2sB3dVPoCD

### 🔐 Authentication

**Register (Employee)**
```http
POST /api/auth/register/
Content-Type: application/json

{
  "role": "Employee",
  "full_name": "John Doe",
  "email": "john@example.com",
  "password": "SecurePass123",
  "company_uid": "uuid-here"
}
```

**Register (Administrator)**
```http
POST /api/auth/register/
Content-Type: application/json

{
  "role": "Administrator",
  "full_name": "Admin User",
  "email": "admin@example.com",
  "password": "AdminPass123",
  "company_name": "Tech Corp",
  "location": "Dhaka, Bangladesh"
}
```

**Login**
```http
POST /api/auth/login/
Content-Type: application/json

{
  "email": "john@example.com",
  "password": "SecurePass123"
}

Response:
{
  "status": "success",
  "data": {
    "token": "eyJ0eXAiOiJKV1...",
    "user": {...}
  }
}
```

**Logout**
```http
POST /api/auth/logout/
Authorization: Bearer <token>
```

---

### 📊 Attendance Management

**Create Attendance**
```http
POST /api/attendance/
Authorization: Bearer <token>
Content-Type: application/json

{
  "is_nfc": true,
  "is_qr": false,
  "date": "2025-12-19"
}
```

**List My Attendance (Employee)**
```http
GET /api/attendance/?date=2025-12-19
Authorization: Bearer <token>

Response:
{
  "count": 15,
  "next": "...",
  "previous": null,
  "results": [
    {
      "uid": "uuid-here",
      "is_nfc": true,
      "is_qr": false,
      "code": "NFC",
      "date": "2025-12-19"
    }
  ]
}
```

**List All Attendance (Admin)**
```http
GET /api/attendance/all/?date=2025-12-19
Authorization: Bearer <token>

Response:
{
  "count": 50,
  "results": [
    {
      "uid": "uuid-here",
      "is_nfc": true,
      "is_qr": false,
      "code": "NFC",
      "date": "2025-12-19",
      "employee": {
        "uid": "user-uuid",
        "full_name": "John Doe"
      }
    }
  ]
}
```

---

### 👥 User Management (Admin Only)

**List Users**
```http
GET /api/users/
Authorization: Bearer <token>

Response:
{
  "count": 25,
  "results": [
    {
      "uid": "uuid-here",
      "full_name": "John Doe",
      "email": "john@example.com",
      "company": {
        "uid": "company-uuid",
        "company_name": "Tech Corp",
        "location": "Dhaka"
      }
    }
  ]
}
```

**User Details**
```http
GET /api/users/{uid}/
Authorization: Bearer <token>
```

---

### 🏢 Company Management (Admin Only)

**List Companies**
```http
GET /api/companies/
Authorization: Bearer <token>

Response:
{
  "count": 10,
  "results": [
    {
      "uid": "uuid-here",
      "company_name": "Tech Corp",
      "location": "Dhaka",
      "employees": [
        {
          "uid": "user-uuid",
          "full_name": "John Doe"
        }
      ]
    }
  ]
}
```

**Update Company**
```http
PUT /api/companies/{uid}/
Authorization: Bearer <token>
Content-Type: application/json

{
  "company_name": "Updated Corp Name",
  "location": "Chittagong"
}
```

---

### 📄 PDF Reports

**My Attendance Report**
```http
GET /api/reports/pdf/my/?start_date=2025-12-01&end_date=2025-12-31
Authorization: Bearer <token>

Returns: PDF file
```

**Single Employee Report (Admin)**
```http
GET /api/reports/pdf/employee/{employee_uid}/?start_date=2025-12-01&end_date=2025-12-31
Authorization: Bearer <token>

Returns: PDF file
```

**Company-wide Report (Admin)**
```http
GET /api/reports/pdf/company/?start_date=2025-12-01&end_date=2025-12-31
Authorization: Bearer <token>

Returns: PDF file with all employees
```

---

## 🎯 Key Features

### ✅ Authentication & Authorization
- JWT-based authentication (1-week validity)
- Role-based permissions: `IsEmployee`, `IsAdministrator`
- Secure password hashing

### ✅ Attendance System
- Dual method support: NFC card & QR code
- One attendance per user per day constraint
- Date-based filtering
- Optimized queries with `select_related` and `prefetch_related`

### ✅ Report Generation
- HTML to PDF conversion using `weasyprint` and backup `xhtml2pdf`
- Date range filtering
- Role-specific reports
- Company-wide analytics

### ✅ Data Management
- Custom pagination (10 items/page)
- Total count in responses
- Proper serialization with nested data
- Clean model relationships

---

## 🏗️ System Architecture
<img width="auto" height="370" alt="image" src="https://github.com/user-attachments/assets/19868b6c-4cee-453e-9344-21c97bd58486" />



### Models
```
User (AbstractUser)
├── Role (FK)
├── Company (FK)
└── Attendance (One-to-Many)

Company
└── Users (One-to-Many)

Attendance
├── User (FK)
└── Unique constraint: (user, date)
```

### Permissions
- `IsAuthenticated` (Default)
- `IsEmployee` (Employee-only endpoints)
- `IsAdministrator` (Admin-only endpoints)

---

## 🧪 Testing

### Run Tests
```bash
# All tests
python manage.py test

# Specific app
python manage.py test apps.auths.tests.test_auth
python manage.py test apps.attendance.tests.test_attendance
python manage.py test apps.companies.tests.test_company

# Verbose output
python manage.py test --verbosity=2
```

### Test Coverage
- Authentication (Register/Login/Logout)
- Attendance CRUD operations
- Company management
- User management
- Permission checks
- Model constraints

---

## 📦 Tech Stack

- **Framework:** Django 5.0+ / Django REST Framework
- **Database:** SQLite3 (Development)
- **Authentication:** JWT (djangorestframework-simplejwt)
- **PDF Generation:** WeasyPrint
- **Testing:** Django TestCase

---

## ⚙️ Environment Setup

### Development Mode (Current)
- ✅ `db.sqlite3` included for quick testing
- ✅ CORS disabled
- ✅ Debug mode enabled
- ✅ Pre-populated test data

### Production Recommendations
- Switch to PostgreSQL
- Enable CORS with whitelist
- Configure environment variables
- Use Docker for deployment
- Set `DEBUG=False`

---

## 📝 Database Schema

### Pre-loaded Test Data
- **Roles:** Employee, Administrator
- **Companies:** 5+ sample companies
- **Users:** 10+ test users (employees & admins)
- **Attendance:** 30+ sample records

**Test Credentials:**
```
Employee:
{
    "email": "rahman@example.com",
    "password": "TestPass123"
}

Administrator:
{
    "email": "adminddd@example.com",
    "password": "TestPass123"
}

Admin (super user):
{
    "email": "admin@gmail.com",
    "password": "admin1234"
}
```

---

## 🔍 Query Optimization

### Techniques Used
1. **Select Related:** For ForeignKey relationships
2. **Prefetch Related:** For reverse ForeignKey (Many-to-One)
3. **Database Indexing:** On email, date fields
4. **Unique Constraints:** Prevent duplicate attendance
5. **Pagination:** Limit query results

---


## PDF Style :

<img width="791" height="851" alt="image" src="https://github.com/user-attachments/assets/5daca897-5edc-41eb-9d3c-5ed89b86d7f4" />




**⚡ Ready to Test:** Just clone, activate venv, and start the server. All test data is already in `db.sqlite3`!
