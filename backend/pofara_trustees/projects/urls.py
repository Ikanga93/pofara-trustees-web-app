"""
URL configuration for projects app.
"""

from django.urls import path, include
from . import views

app_name = 'projects'

urlpatterns = [
    # Project CRUD operations
    path('', views.ProjectListCreateView.as_view(), name='project_list_create'),
    path('<uuid:project_id>/', views.ProjectDetailView.as_view(), name='project_detail'),
    path('<uuid:project_id>/milestones/', views.MilestoneListCreateView.as_view(), name='milestone_list_create'),
    path('<uuid:project_id>/updates/', views.ProjectUpdateListCreateView.as_view(), name='update_list_create'),
    path('<uuid:project_id>/documents/', views.DocumentListCreateView.as_view(), name='document_list_create'),
    path('<uuid:project_id>/comments/', views.CommentListCreateView.as_view(), name='comment_list_create'),
    
    # Milestones
    path('milestones/<uuid:milestone_id>/', views.MilestoneDetailView.as_view(), name='milestone_detail'),
    
    # Updates
    path('updates/<uuid:update_id>/', views.ProjectUpdateDetailView.as_view(), name='update_detail'),
    
    # Documents
    path('documents/<uuid:document_id>/', views.DocumentDetailView.as_view(), name='document_detail'),
    
    # Inspection reports
    path('reports/', views.InspectionReportListView.as_view(), name='report_list'),
    path('reports/<uuid:report_id>/', views.InspectionReportDetailView.as_view(), name='report_detail'),
    
    # Comments
    path('comments/<uuid:comment_id>/', views.CommentDetailView.as_view(), name='comment_detail'),
] 