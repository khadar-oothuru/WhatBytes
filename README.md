# Healthcare Backend API

A comprehensive healthcare management system API built with Django REST Framework, featuring patient and doctor management with secure JWT authentication.

## 🚀 Features

- **User Authentication**: JWT-based authentication system
- **Patient Management**: Complete CRUD operations for patient records
- **Doctor Management**: Complete CRUD operations for doctor profiles
- **Patient-Doctor Mapping**: Assign and manage doctor-patient relationships
- **Swagger Documentation**: Interactive API documentation
- **PostgreSQL Support**: Production-ready database configuration
- **Admin Interface**: Django admin for easy data management

## 📋 Requirements

- Python 3.8+
- Django 4.2.7
- Django REST Framework
- PostgreSQL (optional, SQLite for development)

## 🛠️ Installation

### 1. Clone and Setup

```bash
# Navigate to your project directory
cd d:\whatbytes

# The virtual environment is already created as 'healthcare_env'
# Activate it (Windows)
healthcare_env\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Environment Configuration

Copy `.env.example` to `.env` and update the configuration:

```bash
cp .env.example .env
```

Update the following variables in `.env`:
- `SECRET_KEY`: Your Django secret key
- `DEBUG`: Set to `False` in production
- `DB_*`: Database configuration (PostgreSQL settings)

### 3. Database Setup

#### For Development (SQLite - Current Setup)
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

#### For Production (PostgreSQL)
1. Install PostgreSQL
2. Create database: `healthcare_db`
3. Update settings.py to use PostgreSQL configuration
4. Run migrations

### 4. Run the Server

```bash
python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/`

## 📖 API Documentation

### Interactive Documentation
- **Swagger UI**: `http://127.0.0.1:8000/swagger/`
- **ReDoc**: `http://127.0.0.1:8000/redoc/`

### Authentication Endpoints

### To test use the details below:
POST /api/auth/login/
{
    "username": "testuser",
    "password": "testpass123"
}



#### Register User
```
POST /api/auth/register/
Content-Type: application/json

{
    "username": "john_doe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "password": "securePassword123",
    "password_confirm": "securePassword123"
}
```

#### Login User
```
POST /api/auth/login/
Content-Type: application/json

{
    "username": "john_doe",
    "password": "securePassword123"
}
```

### Patient Management Endpoints

#### Create Patient
```
POST /api/patients/
Authorization: Bearer <access_token>
Content-Type: application/json

{
    "first_name": "Jane",
    "last_name": "Smith",
    "email": "jane.smith@email.com",
    "phone_number": "+1234567890",
    "date_of_birth": "1990-05-15",
    "gender": "F",
    "blood_group": "A+",
    "address": "123 Main St",
    "city": "New York",
    "state": "NY",
    "zip_code": "10001",
    "emergency_contact_name": "John Smith",
    "emergency_contact_phone": "+1234567891"
}
```

#### Get All Patients
```
GET /api/patients/
Authorization: Bearer <access_token>
```

#### Get Patient Details
```
GET /api/patients/<id>/
Authorization: Bearer <access_token>
```

#### Update Patient
```
PUT /api/patients/<id>/
Authorization: Bearer <access_token>
Content-Type: application/json

{
    "first_name": "Jane Updated",
    ...
}
```

#### Delete Patient
```
DELETE /api/patients/<id>/
Authorization: Bearer <access_token>
```

### Doctor Management Endpoints

#### Create Doctor
```
POST /api/doctors/
Authorization: Bearer <access_token>
Content-Type: application/json

{
    "first_name": "Dr. Michael",
    "last_name": "Johnson",
    "email": "dr.johnson@hospital.com",
    "phone_number": "+1234567892",
    "specialization": "CARDIOLOGY",
    "license_number": "MD123456",
    "years_of_experience": 10,
    "qualification": "MD, MBBS",
    "hospital_affiliation": "City General Hospital",
    "office_address": "456 Medical Center Dr",
    "city": "New York",
    "state": "NY",
    "zip_code": "10002",
    "consultation_fee": "200.00"
}
```

#### Get All Doctors
```
GET /api/doctors/
Authorization: Bearer <access_token>
```

#### Get Doctor Details
```
GET /api/doctors/<id>/
Authorization: Bearer <access_token>
```

#### Update Doctor
```
PUT /api/doctors/<id>/
Authorization: Bearer <access_token>
```

#### Delete Doctor
```
DELETE /api/doctors/<id>/
Authorization: Bearer <access_token>
```

### Patient-Doctor Mapping Endpoints

#### Assign Doctor to Patient
```
POST /api/mappings/
Authorization: Bearer <access_token>
Content-Type: application/json

{
    "patient": 1,
    "doctor": 1,
    "status": "ACTIVE",
    "notes": "Regular checkup assignment"
}
```

#### Get All Mappings
```
GET /api/mappings/
Authorization: Bearer <access_token>
```

#### Get Patient's Doctors
```
GET /api/mappings/<patient_id>/
Authorization: Bearer <access_token>
```

#### Remove Doctor from Patient
```
DELETE /api/mappings/detail/<mapping_id>/
Authorization: Bearer <access_token>
```

## 🔧 Models

### Patient Model
- Personal information (name, email, phone, DOB, gender, blood group)
- Address details
- Emergency contact information
- Medical history, allergies, current medications
- System fields (creator, timestamps, active status)

### Doctor Model
- Personal information (name, email, phone)
- Professional details (specialization, license, experience, qualification)
- Hospital affiliation and office address
- Consultation fee and bio
- System fields (creator, timestamps, active status)

### PatientDoctorMapping Model
- Patient-Doctor relationship
- Assignment date and status
- Notes
- System fields (creator, timestamps)

## 🛡️ Security Features

- **JWT Authentication**: Secure token-based authentication
- **Permission Classes**: User-specific data access
- **CORS Configuration**: Cross-origin request handling
- **Environment Variables**: Sensitive data protection
- **Input Validation**: Comprehensive data validation

## 🎯 API Features

- **Pagination**: Built-in pagination for list endpoints
- **Filtering**: User-specific data filtering
- **Error Handling**: Comprehensive error responses
- **Swagger Documentation**: Interactive API exploration
- **Admin Interface**: Django admin for data management

## 📊 Admin Interface

Access the Django admin at `http://127.0.0.1:8000/admin/`

**Superuser Credentials:**
- Username: `khadar`
- Email: `khadar@gmail.com`
- Password: `[as set during creation]`

## 🧪 Testing

### Using Swagger UI
1. Open `http://127.0.0.1:8000/swagger/`
2. Register a new user
3. Login to get access token
4. Use "Authorize" button to add Bearer token
5. Test all endpoints

### Using Postman
1. Import the API endpoints
2. Set up environment variables for base URL and tokens
3. Test authentication flow
4. Test CRUD operations for patients and doctors
5. Test patient-doctor mappings

## 🚀 Deployment

### For Production:

1. **Update Database**: Switch to PostgreSQL in settings.py
2. **Environment Variables**: Set production values in .env
3. **Static Files**: Configure static file serving
4. **Security**: Update ALLOWED_HOSTS, disable DEBUG
5. **HTTPS**: Configure SSL certificates

### Example Production Settings:
```python
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com']
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        # ... PostgreSQL configuration
    }
}
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes and add tests
4. Submit a pull request

## 📝 License

This project is licensed under the MIT License.

## 📞 Support

For support and questions, please contact: khadar@gmail.com

---

**Happy Coding! 🚀**
