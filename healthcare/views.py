from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import Patient, Doctor, PatientDoctorMapping
from .serializers import (
    UserRegistrationSerializer, UserLoginSerializer, PatientSerializer,
    DoctorSerializer, PatientDoctorMappingSerializer, PatientDetailSerializer,
    DoctorDetailSerializer
)


# Authentication Views
class UserRegistrationView(generics.CreateAPIView):
    """
    Register a new user with name, email, and password.
    """
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]
    
    @swagger_auto_schema(
        operation_description="Register a new user",
        request_body=UserRegistrationSerializer,
        responses={
            201: openapi.Response('User created successfully', UserRegistrationSerializer),
            400: 'Bad Request'
        }
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'message': 'User registered successfully',
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                },
                'tokens': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method='post',
    operation_description="Login user and return JWT token",
    request_body=UserLoginSerializer,
    responses={
        200: openapi.Response('Login successful', openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'message': openapi.Schema(type=openapi.TYPE_STRING),
                'user': openapi.Schema(type=openapi.TYPE_OBJECT),
                'tokens': openapi.Schema(type=openapi.TYPE_OBJECT),
            }
        )),
        400: 'Bad Request'
    }
)
@api_view(['POST'])
@permission_classes([AllowAny])
def user_login_view(request):
    """
    Log in a user and return a JWT token.
    """
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        return Response({
            'message': 'Login successful',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
            },
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Patient Management Views
class PatientListCreateView(generics.ListCreateAPIView):
    """
    GET: Retrieve all patients created by the authenticated user.
    POST: Add a new patient (Authenticated users only).
    """
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # Handle swagger schema generation
        if getattr(self, 'swagger_fake_view', False):
            return Patient.objects.none()
        return Patient.objects.filter(created_by=self.request.user, is_active=True)
    
    @swagger_auto_schema(
        operation_description="Get all patients for authenticated user",
        responses={200: PatientSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Create a new patient",
        request_body=PatientSerializer,
        responses={201: PatientSerializer}
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class PatientDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET: Get details of a specific patient.
    PUT: Update patient details.
    DELETE: Delete a patient record.
    """
    serializer_class = PatientDetailSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # Handle swagger schema generation
        if getattr(self, 'swagger_fake_view', False):
            return Patient.objects.none()
        return Patient.objects.filter(created_by=self.request.user)
    
    @swagger_auto_schema(
        operation_description="Get patient details",
        responses={200: PatientDetailSerializer}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Update patient details",
        request_body=PatientSerializer,
        responses={200: PatientSerializer}
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Delete patient record",
        responses={204: 'Patient deleted successfully'}
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


# Doctor Management Views
class DoctorListCreateView(generics.ListCreateAPIView):
    """
    GET: Retrieve all doctors.
    POST: Add a new doctor (Authenticated users only).
    """
    serializer_class = DoctorSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Doctor.objects.filter(is_active=True)
    
    @swagger_auto_schema(
        operation_description="Get all active doctors",
        responses={200: DoctorSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Create a new doctor",
        request_body=DoctorSerializer,
        responses={201: DoctorSerializer}
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class DoctorDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET: Get details of a specific doctor.
    PUT: Update doctor details.
    DELETE: Delete a doctor record.
    """
    serializer_class = DoctorDetailSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Doctor.objects.all()
    
    @swagger_auto_schema(
        operation_description="Get doctor details",
        responses={200: DoctorDetailSerializer}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Update doctor details",
        request_body=DoctorSerializer,
        responses={200: DoctorSerializer}
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Delete doctor record",
        responses={204: 'Doctor deleted successfully'}
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


# Patient-Doctor Mapping Views
class PatientDoctorMappingListCreateView(generics.ListCreateAPIView):
    """
    GET: Retrieve all patient-doctor mappings.
    POST: Assign a doctor to a patient.
    """
    serializer_class = PatientDoctorMappingSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return PatientDoctorMapping.objects.all()
    
    @swagger_auto_schema(
        operation_description="Get all patient-doctor mappings",
        responses={200: PatientDoctorMappingSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Assign a doctor to a patient",
        request_body=PatientDoctorMappingSerializer,
        responses={201: PatientDoctorMappingSerializer}
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


@swagger_auto_schema(
    method='get',
    operation_description="Get all doctors assigned to a specific patient",
    responses={200: PatientDoctorMappingSerializer(many=True)}
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def patient_doctors_view(request, patient_id):
    """
    Get all doctors assigned to a specific patient.
    """
    patient = get_object_or_404(Patient, id=patient_id, created_by=request.user)
    mappings = PatientDoctorMapping.objects.filter(patient=patient)
    serializer = PatientDoctorMappingSerializer(mappings, many=True)
    return Response(serializer.data)


class PatientDoctorMappingDetailView(generics.RetrieveDestroyAPIView):
    """
    GET: Get specific mapping details.
    DELETE: Remove a doctor from a patient.
    """
    serializer_class = PatientDoctorMappingSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return PatientDoctorMapping.objects.all()
    
    @swagger_auto_schema(
        operation_description="Get mapping details",
        responses={200: PatientDoctorMappingSerializer}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Remove doctor from patient",
        responses={204: 'Mapping deleted successfully'}
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
