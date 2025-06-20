from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import Patient, Doctor, PatientDoctorMapping


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'password', 'password_confirm')
        
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Passwords don't match")
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        return user


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    
    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise serializers.ValidationError('Invalid credentials')
            if not user.is_active:
                raise serializers.ValidationError('User account is disabled')
            attrs['user'] = user
            return attrs
        else:
            raise serializers.ValidationError('Must include username and password')


class PatientSerializer(serializers.ModelSerializer):
    full_name = serializers.ReadOnlyField()
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    
    class Meta:
        model = Patient
        fields = [
            'id', 'first_name', 'last_name', 'full_name', 'email', 'phone_number',
            'date_of_birth', 'gender', 'blood_group', 'address', 'city', 'state',
            'zip_code', 'country', 'emergency_contact_name', 'emergency_contact_phone',
            'medical_history', 'allergies', 'current_medications', 'created_by_username',
            'created_at', 'updated_at', 'is_active'
        ]
        read_only_fields = ('id', 'created_at', 'updated_at', 'full_name', 'created_by_username')
    
    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)


class DoctorSerializer(serializers.ModelSerializer):
    full_name = serializers.ReadOnlyField()
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    
    class Meta:
        model = Doctor
        fields = [
            'id', 'first_name', 'last_name', 'full_name', 'email', 'phone_number',
            'specialization', 'license_number', 'years_of_experience', 'qualification',
            'hospital_affiliation', 'office_address', 'city', 'state', 'zip_code',
            'country', 'consultation_fee', 'bio', 'created_by_username',
            'created_at', 'updated_at', 'is_active'
        ]
        read_only_fields = ('id', 'created_at', 'updated_at', 'full_name', 'created_by_username')
    
    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)


class PatientDoctorMappingSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.full_name', read_only=True)
    doctor_name = serializers.CharField(source='doctor.full_name', read_only=True)
    patient_email = serializers.CharField(source='patient.email', read_only=True)
    doctor_email = serializers.CharField(source='doctor.email', read_only=True)
    doctor_specialization = serializers.CharField(source='doctor.specialization', read_only=True)
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    
    class Meta:
        model = PatientDoctorMapping
        fields = [
            'id', 'patient', 'doctor', 'patient_name', 'doctor_name',
            'patient_email', 'doctor_email', 'doctor_specialization',
            'assigned_date', 'status', 'notes', 'created_by_username',
            'created_at', 'updated_at'
        ]
        read_only_fields = ('id', 'assigned_date', 'created_at', 'updated_at', 'created_by_username')
    
    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)
    
    def validate(self, attrs):
        patient = attrs.get('patient')
        doctor = attrs.get('doctor')
        
        # Check if mapping already exists
        if PatientDoctorMapping.objects.filter(patient=patient, doctor=doctor).exists():
            raise serializers.ValidationError("This patient is already assigned to this doctor")
        
        return attrs


class PatientDetailSerializer(PatientSerializer):
    """Detailed patient serializer with doctor mappings"""
    doctor_mappings = PatientDoctorMappingSerializer(many=True, read_only=True)
    
    class Meta(PatientSerializer.Meta):
        fields = PatientSerializer.Meta.fields + ['doctor_mappings']


class DoctorDetailSerializer(DoctorSerializer):
    """Detailed doctor serializer with patient mappings"""
    patient_mappings = PatientDoctorMappingSerializer(many=True, read_only=True)
    
    class Meta(DoctorSerializer.Meta):
        fields = DoctorSerializer.Meta.fields + ['patient_mappings']
