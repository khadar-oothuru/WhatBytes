from django.urls import path
from . import views

app_name = 'healthcare'

urlpatterns = [
    # Authentication URLs
    path('auth/register/', views.UserRegistrationView.as_view(), name='user-register'),
    path('auth/login/', views.user_login_view, name='user-login'),
    
    # Patient URLs
    path('patients/', views.PatientListCreateView.as_view(), name='patient-list-create'),
    path('patients/<int:pk>/', views.PatientDetailView.as_view(), name='patient-detail'),
    
    # Doctor URLs
    path('doctors/', views.DoctorListCreateView.as_view(), name='doctor-list-create'),
    path('doctors/<int:pk>/', views.DoctorDetailView.as_view(), name='doctor-detail'),
    
    # Patient-Doctor Mapping URLs
    path('mappings/', views.PatientDoctorMappingListCreateView.as_view(), name='mapping-list-create'),
    path('mappings/<int:patient_id>/', views.patient_doctors_view, name='patient-doctors'),
    path('mappings/detail/<int:pk>/', views.PatientDoctorMappingDetailView.as_view(), name='mapping-detail'),
]
