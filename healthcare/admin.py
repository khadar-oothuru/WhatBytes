from django.contrib import admin
from .models import Patient, Doctor, PatientDoctorMapping


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'phone_number', 'gender', 'blood_group', 'created_by', 'created_at', 'is_active')
    list_filter = ('gender', 'blood_group', 'is_active', 'created_at')
    search_fields = ('first_name', 'last_name', 'email', 'phone_number')
    list_editable = ('is_active',)
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'email', 'phone_number', 'date_of_birth', 'gender', 'blood_group')
        }),
        ('Address', {
            'fields': ('address', 'city', 'state', 'zip_code', 'country')
        }),
        ('Emergency Contact', {
            'fields': ('emergency_contact_name', 'emergency_contact_phone')
        }),
        ('Medical Information', {
            'fields': ('medical_history', 'allergies', 'current_medications')
        }),
        ('System Information', {
            'fields': ('created_by', 'is_active', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'specialization', 'license_number', 'years_of_experience', 'consultation_fee', 'created_by', 'is_active')
    list_filter = ('specialization', 'is_active', 'created_at')
    search_fields = ('first_name', 'last_name', 'email', 'license_number', 'hospital_affiliation')
    list_editable = ('is_active',)
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'email', 'phone_number')
        }),
        ('Professional Information', {
            'fields': ('specialization', 'license_number', 'years_of_experience', 'qualification', 'hospital_affiliation', 'consultation_fee')
        }),
        ('Office Address', {
            'fields': ('office_address', 'city', 'state', 'zip_code', 'country')
        }),
        ('Additional Information', {
            'fields': ('bio',)
        }),
        ('System Information', {
            'fields': ('created_by', 'is_active', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(PatientDoctorMapping)
class PatientDoctorMappingAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'status', 'assigned_date', 'created_by')
    list_filter = ('status', 'assigned_date', 'created_at')
    search_fields = ('patient__first_name', 'patient__last_name', 'doctor__first_name', 'doctor__last_name')
    list_editable = ('status',)
    readonly_fields = ('assigned_date', 'created_at', 'updated_at')
    
    fieldsets = (
        ('Mapping Information', {
            'fields': ('patient', 'doctor', 'status', 'notes')
        }),
        ('System Information', {
            'fields': ('created_by', 'assigned_date', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
