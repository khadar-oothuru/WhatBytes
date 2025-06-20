from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from healthcare.models import Patient
from datetime import date


class Command(BaseCommand):
    help = 'Add additional patients to the database'

    def handle(self, *args, **options):
        # Get or create a test user
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

        # Additional patient data
        additional_patients = [
            {
                'first_name': 'Sarah',
                'last_name': 'Williams',
                'email': 'sarah.williams@email.com',
                'phone_number': '+1555123001',
                'date_of_birth': date(1988, 4, 12),
                'gender': 'F',
                'blood_group': 'O+',
                'address': '789 Elm Street',
                'city': 'Boston',
                'state': 'MA',
                'zip_code': '02101',
                'emergency_contact_name': 'Mark Williams',
                'emergency_contact_phone': '+1555123002',
                'medical_history': 'Mild asthma, previous ankle fracture',
                'allergies': 'Penicillin',
                'current_medications': 'Albuterol inhaler as needed'
            },
            {
                'first_name': 'David',
                'last_name': 'Brown',
                'email': 'david.brown@email.com',
                'phone_number': '+1555123003',
                'date_of_birth': date(1982, 11, 25),
                'gender': 'M',
                'blood_group': 'A-',
                'address': '456 Oak Avenue',
                'city': 'Seattle',
                'state': 'WA',
                'zip_code': '98101',
                'emergency_contact_name': 'Linda Brown',
                'emergency_contact_phone': '+1555123004',
                'medical_history': 'Hypertension, diabetes type 2',
                'allergies': 'Shellfish',
                'current_medications': 'Metformin 500mg twice daily, Lisinopril 10mg daily'
            },
            {
                'first_name': 'Maria',
                'last_name': 'Garcia',
                'email': 'maria.garcia@email.com',
                'phone_number': '+1555123005',
                'date_of_birth': date(1995, 8, 18),
                'gender': 'F',
                'blood_group': 'B+',
                'address': '321 Pine Street',
                'city': 'Miami',
                'state': 'FL',
                'zip_code': '33101',
                'emergency_contact_name': 'Carlos Garcia',
                'emergency_contact_phone': '+1555123006',
                'medical_history': 'No significant medical history',
                'allergies': 'Latex',
                'current_medications': 'Birth control pills'
            },
            {
                'first_name': 'James',
                'last_name': 'Miller',
                'email': 'james.miller@email.com',
                'phone_number': '+1555123007',
                'date_of_birth': date(1976, 1, 30),
                'gender': 'M',
                'blood_group': 'AB-',
                'address': '654 Maple Drive',
                'city': 'Denver',
                'state': 'CO',
                'zip_code': '80201',
                'emergency_contact_name': 'Susan Miller',
                'emergency_contact_phone': '+1555123008',
                'medical_history': 'Previous heart surgery (2018), high cholesterol',
                'allergies': 'Aspirin',
                'current_medications': 'Atorvastatin 20mg daily, Metoprolol 50mg twice daily'
            },
            {
                'first_name': 'Jennifer',
                'last_name': 'Taylor',
                'email': 'jennifer.taylor@email.com',
                'phone_number': '+1555123009',
                'date_of_birth': date(1991, 6, 14),
                'gender': 'F',
                'blood_group': 'O-',
                'address': '987 Cedar Lane',
                'city': 'Portland',
                'state': 'OR',
                'zip_code': '97201',
                'emergency_contact_name': 'Robert Taylor',
                'emergency_contact_phone': '+1555123010',
                'medical_history': 'Migraines, anxiety disorder',
                'allergies': 'Ibuprofen',
                'current_medications': 'Sumatriptan as needed, Sertraline 50mg daily'
            },
            {
                'first_name': 'Christopher',
                'last_name': 'Anderson',
                'email': 'christopher.anderson@email.com',
                'phone_number': '+1555123011',
                'date_of_birth': date(1984, 9, 7),
                'gender': 'M',
                'blood_group': 'A+',
                'address': '159 Birch Street',
                'city': 'Atlanta',
                'state': 'GA',
                'zip_code': '30301',
                'emergency_contact_name': 'Michelle Anderson',
                'emergency_contact_phone': '+1555123012',
                'medical_history': 'Kidney stones (2020), seasonal allergies',
                'allergies': 'Pollen, dust mites',
                'current_medications': 'Claritin daily during allergy season'
            },
            {
                'first_name': 'Lisa',
                'last_name': 'Thompson',
                'email': 'lisa.thompson@email.com',
                'phone_number': '+1555123013',
                'date_of_birth': date(1979, 12, 3),
                'gender': 'F',
                'blood_group': 'B-',
                'address': '753 Willow Avenue',
                'city': 'Phoenix',
                'state': 'AZ',
                'zip_code': '85001',
                'emergency_contact_name': 'Kevin Thompson',
                'emergency_contact_phone': '+1555123014',
                'medical_history': 'Osteoporosis, previous breast cancer (remission)',
                'allergies': 'Sulfa drugs',
                'current_medications': 'Calcium supplements, Alendronate weekly'
            },
            {
                'first_name': 'Daniel',
                'last_name': 'White',
                'email': 'daniel.white@email.com',
                'phone_number': '+1555123015',
                'date_of_birth': date(1993, 3, 22),
                'gender': 'M',
                'blood_group': 'O+',
                'address': '842 Spruce Court',
                'city': 'Nashville',
                'state': 'TN',
                'zip_code': '37201',
                'emergency_contact_name': 'Amanda White',
                'emergency_contact_phone': '+1555123016',
                'medical_history': 'ADHD, previous sports injuries',
                'allergies': 'None known',
                'current_medications': 'Adderall XR 20mg daily'
            }
        ]

        patients_created = 0
        for patient_data in additional_patients:
            patient_data['created_by'] = test_user
            
            patient, created = Patient.objects.get_or_create(
                email=patient_data['email'],
                defaults=patient_data
            )
            if created:
                patients_created += 1
                self.stdout.write(f"✅ Created patient: {patient.full_name}")
            else:
                self.stdout.write(f"⚠️ Patient already exists: {patient.full_name}")

        self.stdout.write(
            self.style.SUCCESS(
                f'\n🎉 Patient creation completed!\n'
                f'📊 Created {patients_created} new patients\n'
                f'📋 Total patients in database: {Patient.objects.count()}'
            )
        )
