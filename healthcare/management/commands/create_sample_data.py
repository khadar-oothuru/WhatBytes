from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from healthcare.models import Patient, Doctor, PatientDoctorMapping
from datetime import date
from decimal import Decimal


class Command(BaseCommand):
    help = 'Create sample data for testing the healthcare API'

    def add_arguments(self, parser):
        parser.add_argument(
            '--patients',
            type=int,
            default=5,
            help='Number of patients to create'
        )
        parser.add_argument(
            '--doctors',
            type=int,
            default=3,
            help='Number of doctors to create'
        )

    def handle(self, *args, **options):
        # Create a test user if it doesn't exist
        test_user, created = User.objects.get_or_create(
            username='testuser',
            defaults={
                'email': 'test@healthcare.com',
                'first_name': 'Test',
                'last_name': 'User',
                'is_staff': False,
                'is_active': True
            }
        )
        if created:
            test_user.set_password('testpassword123')
            test_user.save()
            self.stdout.write(
                self.style.SUCCESS('Created test user: testuser / testpassword123')
            )

        # Sample patient data
        patient_data = [
            {
                'first_name': 'John',
                'last_name': 'Doe',
                'email': 'john.doe@email.com',
                'phone_number': '+1234567890',
                'date_of_birth': date(1985, 3, 15),
                'gender': 'M',
                'blood_group': 'A+',
                'address': '123 Main St',
                'city': 'New York',
                'state': 'NY',
                'zip_code': '10001',
                'emergency_contact_name': 'Jane Doe',
                'emergency_contact_phone': '+1234567891'
            },
            {
                'first_name': 'Alice',
                'last_name': 'Johnson',
                'email': 'alice.johnson@email.com',
                'phone_number': '+1234567892',
                'date_of_birth': date(1990, 7, 22),
                'gender': 'F',
                'blood_group': 'B+',
                'address': '456 Oak Ave',
                'city': 'Los Angeles',
                'state': 'CA',
                'zip_code': '90210',
                'emergency_contact_name': 'Bob Johnson',
                'emergency_contact_phone': '+1234567893'
            },
            {
                'first_name': 'Michael',
                'last_name': 'Smith',
                'email': 'michael.smith@email.com',
                'phone_number': '+1234567894',
                'date_of_birth': date(1978, 11, 8),
                'gender': 'M',
                'blood_group': 'O+',
                'address': '789 Pine St',
                'city': 'Chicago',
                'state': 'IL',
                'zip_code': '60601',
                'emergency_contact_name': 'Sarah Smith',
                'emergency_contact_phone': '+1234567895'
            },
            {
                'first_name': 'Emily',
                'last_name': 'Davis',
                'email': 'emily.davis@email.com',
                'phone_number': '+1234567896',
                'date_of_birth': date(1992, 2, 14),
                'gender': 'F',
                'blood_group': 'AB+',
                'address': '321 Elm St',
                'city': 'Houston',
                'state': 'TX',
                'zip_code': '77001',
                'emergency_contact_name': 'David Davis',
                'emergency_contact_phone': '+1234567897'
            },
            {
                'first_name': 'Robert',
                'last_name': 'Wilson',
                'email': 'robert.wilson@email.com',
                'phone_number': '+1234567898',
                'date_of_birth': date(1975, 9, 30),
                'gender': 'M',
                'blood_group': 'A-',
                'address': '654 Maple Ave',
                'city': 'Phoenix',
                'state': 'AZ',
                'zip_code': '85001',
                'emergency_contact_name': 'Lisa Wilson',
                'emergency_contact_phone': '+1234567899'
            }
        ]

        # Sample doctor data
        doctor_data = [
            {
                'first_name': 'Sarah',
                'last_name': 'Johnson',
                'email': 'dr.sarah.johnson@hospital.com',
                'phone_number': '+1555001001',
                'specialization': 'CARDIOLOGY',
                'license_number': 'MD001234',
                'years_of_experience': 15,
                'qualification': 'MD, FACC',
                'hospital_affiliation': 'City General Hospital',
                'office_address': '100 Medical Center Dr, Suite 200',
                'city': 'New York',
                'state': 'NY',
                'zip_code': '10001',
                'consultation_fee': Decimal('250.00'),
                'bio': 'Experienced cardiologist with expertise in interventional cardiology.'
            },
            {
                'first_name': 'Michael',
                'last_name': 'Chen',
                'email': 'dr.michael.chen@hospital.com',
                'phone_number': '+1555001002',
                'specialization': 'NEUROLOGY',
                'license_number': 'MD001235',
                'years_of_experience': 12,
                'qualification': 'MD, PhD',
                'hospital_affiliation': 'Metro Medical Center',
                'office_address': '200 Health Plaza, Floor 3',
                'city': 'Los Angeles',
                'state': 'CA',
                'zip_code': '90210',
                'consultation_fee': Decimal('300.00'),
                'bio': 'Neurologist specializing in movement disorders and epilepsy.'
            },
            {
                'first_name': 'Jennifer',
                'last_name': 'Martinez',
                'email': 'dr.jennifer.martinez@hospital.com',
                'phone_number': '+1555001003',
                'specialization': 'PEDIATRICS',
                'license_number': 'MD001236',
                'years_of_experience': 8,
                'qualification': 'MD, MPH',
                'hospital_affiliation': 'Children\'s Hospital',
                'office_address': '300 Kids Care Blvd',
                'city': 'Chicago',
                'state': 'IL',
                'zip_code': '60601',
                'consultation_fee': Decimal('180.00'),
                'bio': 'Pediatrician focused on preventive care and child development.'
            }
        ]

        # Create patients
        patients_created = 0
        for i in range(min(options['patients'], len(patient_data))):
            patient_info = patient_data[i]
            patient_info['created_by'] = test_user
            
            patient, created = Patient.objects.get_or_create(
                email=patient_info['email'],
                defaults=patient_info
            )
            if created:
                patients_created += 1
                self.stdout.write(f"Created patient: {patient.full_name}")

        # Create doctors
        doctors_created = 0
        for i in range(min(options['doctors'], len(doctor_data))):
            doctor_info = doctor_data[i]
            doctor_info['created_by'] = test_user
            
            doctor, created = Doctor.objects.get_or_create(
                email=doctor_info['email'],
                defaults=doctor_info
            )
            if created:
                doctors_created += 1
                self.stdout.write(f"Created doctor: {doctor.full_name}")

        # Create some sample mappings
        patients = Patient.objects.filter(created_by=test_user)[:3]
        doctors = Doctor.objects.filter(created_by=test_user)[:2]
        
        mappings_created = 0
        for patient in patients:
            for doctor in doctors:
                mapping, created = PatientDoctorMapping.objects.get_or_create(
                    patient=patient,
                    doctor=doctor,
                    defaults={
                        'created_by': test_user,
                        'status': 'ACTIVE',
                        'notes': f'Sample assignment of {patient.full_name} to {doctor.full_name}'
                    }
                )
                if created:
                    mappings_created += 1

        self.stdout.write(
            self.style.SUCCESS(
                f'\nSample data creation completed!\n'
                f'Created {patients_created} patients\n'
                f'Created {doctors_created} doctors\n'
                f'Created {mappings_created} patient-doctor mappings\n'
                f'\nTest user credentials:\n'
                f'Username: testuser\n'
                f'Password: testpassword123'
            )
        )
