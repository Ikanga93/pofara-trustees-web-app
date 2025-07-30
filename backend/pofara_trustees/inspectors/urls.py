"""
URL configuration for inspectors app.
"""

from django.urls import path, include
from . import views

app_name = 'inspectors'

urlpatterns = [
    # Inspector management
    path('', views.InspectorListView.as_view(), name='inspector_list'),
    path('profile/', views.InspectorProfileView.as_view(), name='inspector_profile'),
    path('<uuid:inspector_id>/', views.InspectorDetailView.as_view(), name='inspector_detail'),
    
    # Certifications
    path('certifications/', views.CertificationListCreateView.as_view(), name='certification_list_create'),
    path('certifications/<uuid:cert_id>/', views.CertificationDetailView.as_view(), name='certification_detail'),
    
    # Ratings and reviews
    path('<uuid:inspector_id>/ratings/', views.RatingListCreateView.as_view(), name='rating_list_create'),
    path('ratings/<uuid:rating_id>/', views.RatingDetailView.as_view(), name='rating_detail'),
    
    # Availability
    path('availability/', views.AvailabilityListCreateView.as_view(), name='availability_list_create'),
    path('availability/<uuid:availability_id>/', views.AvailabilityDetailView.as_view(), name='availability_detail'),
    
    # Documents
    path('documents/', views.DocumentListCreateView.as_view(), name='document_list_create'),
    path('documents/<uuid:document_id>/', views.DocumentDetailView.as_view(), name='document_detail'),
    
    # Applications and bookings
    path('applications/', views.ApplicationListView.as_view(), name='application_list'),
    path('bookings/', views.BookingListView.as_view(), name='booking_list'),
] 