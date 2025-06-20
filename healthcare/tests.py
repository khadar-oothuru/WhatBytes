import json
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from healthcare.models import Patient, Doctor, PatientDoctorMapping


class AuthenticationTestCase(APITestCase):
    """Test cases for user authentication"""
    
    def test_user_registration(self):
        """Test user registration"""
        url = reverse('healthcare:user-register')
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password': 'testpassword123',
            'password_confirm': 'testpassword123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='testuser').exists())
        self.assertIn('tokens', response.data)
    
    def test_user_login(self):
        """Test user login"""
        # Create user first
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword123'
        )
        
        url = reverse('healthcare:user-login')
        data = {
            'username': 'testuser',
            'password': 'testpassword123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('tokens', response.data)
    
    def test_invalid_login(self):
        """Test login with invalid credentials"""
        url = reverse('healthcare:user-login')
        data = {
            'username': 'invaliduser',
            'password': 'wrongpassword'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class PatientTestCase(APITestCase):
    """Test cases for patient management"""
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword123'
        )
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        
        self.patient_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
            'phone_number': '+1234567890',
            'date_of_birth': '1990-05-15',
            'gender': 'M',
            'blood_group': 'A+',
            'address': '123 Main St',
            'city': 'New York',
            'state': 'NY',
            'zip_code': '10001',
            'emergency_contact_name': 'Jane Doe',
            'emergency_contact_phone': '+1234567891'
        }
    
    def test_create_patient(self):
        """Test creating a new patient"""
        url = reverse('healthcare:patient-list-create')
        response = self.client.post(url, self.patient_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Patient.objects.filter(email='john.doe@example.com').exists())
    
    def test_get_patients(self):
        """Test retrieving patient list"""
        Patient.objects.create(created_by=self.user, **self.patient_data)
        url = reverse('healthcare:patient-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
    
    def test_get_patient_detail(self):
        """Test retrieving specific patient details"""
        patient = Patient.objects.create(created_by=self.user, **self.patient_data)
        url = reverse('healthcare:patient-detail', kwargs={'pk': patient.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'john.doe@example.com')
    
    def test_update_patient(self):
        """Test updating patient information"""
        patient = Patient.objects.create(created_by=self.user, **self.patient_data)
        url = reverse('healthcare:patient-detail', kwargs={'pk': patient.id})
        updated_data = self.patient_data.copy()
        updated_data['first_name'] = 'Updated John'
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        patient.refresh_from_db()
        self.assertEqual(patient.first_name, 'Updated John')
    
    def test_delete_patient(self):
        """Test deleting a patient"""
        patient = Patient.objects.create(created_by=self.user, **self.patient_data)
        url = reverse('healthcare:patient-detail', kwargs={'pk': patient.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Patient.objects.filter(id=patient.id).exists())
    
    def test_unauthorized_access(self):
        """Test accessing patients without authentication"""
        self.client.credentials()  # Remove authentication
        url = reverse('healthcare:patient-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class DoctorTestCase(APITestCase):
    """Test cases for doctor management"""
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword123'
        )
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        
        self.doctor_data = {
            'first_name': 'Dr. Sarah',
            'last_name': 'Johnson',
            'email': 'dr.sarah@hospital.com',
            'phone_number': '+1234567892',
            'specialization': 'CARDIOLOGY',
            'license_number': 'MD123456',
            'years_of_experience': 10,
            'qualification': 'MD, MBBS',
            'hospital_affiliation': 'City General Hospital',
            'office_address': '456 Medical Center Dr',
            'city': 'New York',
            'state': 'NY',
            'zip_code': '10002',
            'consultation_fee': '200.00'
        }
    
    def test_create_doctor(self):
        """Test creating a new doctor"""
        url = reverse('healthcare:doctor-list-create')
        response = self.client.post(url, self.doctor_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Doctor.objects.filter(email='dr.sarah@hospital.com').exists())
    
    def test_get_doctors(self):
        """Test retrieving doctor list"""
        Doctor.objects.create(created_by=self.user, **self.doctor_data)
        url = reverse('healthcare:doctor-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
    
    def test_get_doctor_detail(self):
        """Test retrieving specific doctor details"""
        doctor = Doctor.objects.create(created_by=self.user, **self.doctor_data)
        url = reverse('healthcare:doctor-detail', kwargs={'pk': doctor.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['specialization'], 'CARDIOLOGY')
    
    def test_update_doctor(self):
        """Test updating doctor information"""
        doctor = Doctor.objects.create(created_by=self.user, **self.doctor_data)
        url = reverse('healthcare:doctor-detail', kwargs={'pk': doctor.id})
        updated_data = self.doctor_data.copy()
        updated_data['years_of_experience'] = 15
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        doctor.refresh_from_db()
        self.assertEqual(doctor.years_of_experience, 15)
    
    def test_delete_doctor(self):
        """Test deleting a doctor"""
        doctor = Doctor.objects.create(created_by=self.user, **self.doctor_data)
        url = reverse('healthcare:doctor-detail', kwargs={'pk': doctor.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Doctor.objects.filter(id=doctor.id).exists())


class PatientDoctorMappingTestCase(APITestCase):
    """Test cases for patient-doctor mappings"""
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword123'
        )
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        
        # Create patient and doctor
        self.patient = Patient.objects.create(
            created_by=self.user,
            first_name='John',
            last_name='Doe',
            email='john.doe@example.com',
            phone_number='+1234567890',
            date_of_birth='1990-05-15',
            gender='M',
            address='123 Main St',
            city='New York',
            state='NY',
            zip_code='10001',
            emergency_contact_name='Jane Doe',
            emergency_contact_phone='+1234567891'
        )
        
        self.doctor = Doctor.objects.create(
            created_by=self.user,
            first_name='Dr. Sarah',
            last_name='Johnson',
            email='dr.sarah@hospital.com',
            phone_number='+1234567892',
            specialization='CARDIOLOGY',
            license_number='MD123456',
            years_of_experience=10,
            qualification='MD, MBBS',
            hospital_affiliation='City General Hospital',
            office_address='456 Medical Center Dr',
            city='New York',
            state='NY',
            zip_code='10002',
            consultation_fee='200.00'
        )
    
    def test_create_mapping(self):
        """Test creating patient-doctor mapping"""
        url = reverse('healthcare:mapping-list-create')
        data = {
            'patient': self.patient.id,
            'doctor': self.doctor.id,
            'status': 'ACTIVE',
            'notes': 'Regular checkup assignment'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            PatientDoctorMapping.objects.filter(
                patient=self.patient, 
                doctor=self.doctor
            ).exists()
        )
    
    def test_get_mappings(self):
        """Test retrieving all mappings"""
        PatientDoctorMapping.objects.create(
            patient=self.patient,
            doctor=self.doctor,
            created_by=self.user
        )
        url = reverse('healthcare:mapping-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
    
    def test_get_patient_doctors(self):
        """Test retrieving doctors for a specific patient"""
        PatientDoctorMapping.objects.create(
            patient=self.patient,
            doctor=self.doctor,
            created_by=self.user
        )
        url = reverse('healthcare:patient-doctors', kwargs={'patient_id': self.patient.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_delete_mapping(self):
        """Test deleting a patient-doctor mapping"""
        mapping = PatientDoctorMapping.objects.create(
            patient=self.patient,
            doctor=self.doctor,
            created_by=self.user
        )
        url = reverse('healthcare:mapping-detail', kwargs={'pk': mapping.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(PatientDoctorMapping.objects.filter(id=mapping.id).exists())
    
    def test_duplicate_mapping(self):
        """Test preventing duplicate mappings"""
        PatientDoctorMapping.objects.create(
            patient=self.patient,
            doctor=self.doctor,
            created_by=self.user
        )
        
        url = reverse('healthcare:mapping-list-create')
        data = {
            'patient': self.patient.id,
            'doctor': self.doctor.id,
            'status': 'ACTIVE'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class ModelTestCase(TestCase):
    """Test cases for model methods and properties"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword123'
        )
    
    def test_patient_full_name(self):
        """Test patient full_name property"""
        patient = Patient.objects.create(
            created_by=self.user,
            first_name='John',
            last_name='Doe',
            email='john.doe@example.com',
            date_of_birth='1990-05-15',
            gender='M',
            address='123 Main St',
            city='New York',
            state='NY',
            zip_code='10001',
            emergency_contact_name='Jane Doe',
            emergency_contact_phone='+1234567891'
        )
        self.assertEqual(patient.full_name, 'John Doe')
        self.assertEqual(str(patient), 'John Doe')
    
    def test_doctor_full_name(self):
        """Test doctor full_name property"""
        doctor = Doctor.objects.create(
            created_by=self.user,
            first_name='Sarah',
            last_name='Johnson',
            email='dr.sarah@hospital.com',
            phone_number='+1234567892',
            specialization='CARDIOLOGY',
            license_number='MD123456',
            years_of_experience=10,
            qualification='MD, MBBS',
            hospital_affiliation='City General Hospital',
            office_address='456 Medical Center Dr',
            city='New York',
            state='NY',
            zip_code='10002',
            consultation_fee='200.00'
        )
        self.assertEqual(doctor.full_name, 'Dr. Sarah Johnson')
        self.assertEqual(str(doctor), 'Dr. Sarah Johnson - CARDIOLOGY')


if __name__ == '__main__':
    import unittest
    unittest.main()
