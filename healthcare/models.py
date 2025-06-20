from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator


class Patient(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    
    BLOOD_GROUP_CHOICES = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    ]
    
    # Basic Information
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    
    # Personal Details
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES, blank=True)
    
    # Address Information
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)
    country = models.CharField(max_length=100, default='USA')
    
    # Medical Information
    emergency_contact_name = models.CharField(max_length=100)
    emergency_contact_phone = models.CharField(validators=[phone_regex], max_length=17)
    medical_history = models.TextField(blank=True)
    allergies = models.TextField(blank=True)
    current_medications = models.TextField(blank=True)
    
    # System Fields
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='patients')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class Doctor(models.Model):
    SPECIALIZATION_CHOICES = [
        ('CARDIOLOGY', 'Cardiology'),
        ('NEUROLOGY', 'Neurology'),
        ('ORTHOPEDICS', 'Orthopedics'),
        ('PEDIATRICS', 'Pediatrics'),
        ('GYNECOLOGY', 'Gynecology'),
        ('DERMATOLOGY', 'Dermatology'),
        ('PSYCHIATRY', 'Psychiatry'),
        ('OPHTHALMOLOGY', 'Ophthalmology'),
        ('ENT', 'ENT (Ear, Nose, Throat)'),
        ('GENERAL', 'General Medicine'),
        ('SURGERY', 'Surgery'),
        ('ANESTHESIOLOGY', 'Anesthesiology'),
        ('RADIOLOGY', 'Radiology'),
        ('PATHOLOGY', 'Pathology'),
        ('EMERGENCY', 'Emergency Medicine'),
        ('OTHER', 'Other'),
    ]
    
    # Basic Information
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    phone_number = models.CharField(validators=[phone_regex], max_length=17)
    
    # Professional Information
    specialization = models.CharField(max_length=50, choices=SPECIALIZATION_CHOICES)
    license_number = models.CharField(max_length=50, unique=True)
    years_of_experience = models.PositiveIntegerField()
    qualification = models.CharField(max_length=200)
    hospital_affiliation = models.CharField(max_length=200)
    
    # Contact Information
    office_address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)
    country = models.CharField(max_length=100, default='USA')
    
    # Additional Information
    consultation_fee = models.DecimalField(max_digits=10, decimal_places=2)
    bio = models.TextField(blank=True)
    
    # System Fields
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='doctors_created')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return f"Dr. {self.first_name} {self.last_name} - {self.specialization}"
    
    @property
    def full_name(self):
        return f"Dr. {self.first_name} {self.last_name}"


class PatientDoctorMapping(models.Model):
    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('INACTIVE', 'Inactive'),
        ('COMPLETED', 'Completed'),
    ]
    
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='doctor_mappings')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='patient_mappings')
    assigned_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE')
    notes = models.TextField(blank=True)
    
    # System Fields
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mappings_created')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['patient', 'doctor']
        ordering = ['-assigned_date']
        
    def __str__(self):
        return f"{self.patient.full_name} assigned to {self.doctor.full_name}"
