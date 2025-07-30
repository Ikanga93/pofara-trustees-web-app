"""
Views for projects app.
"""

from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .models import (
    Project, ProjectMilestone, ProjectUpdate, 
    ProjectDocument, InspectionReport, ProjectComment
)
from .serializers import (
    ProjectListSerializer, ProjectCreateSerializer, ProjectDetailSerializer,
    ProjectUpdateSerializer, ProjectMilestoneSerializer, ProjectUpdateListSerializer,
    ProjectDocumentSerializer
)


class ProjectListCreateView(generics.ListCreateAPIView):
    """
    List all projects for authenticated user or create a new project.
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        # Return projects owned by the user or where they are assigned as inspector
        return Project.objects.filter(
            Q(owner=user) | Q(assigned_inspector__user=user)
        ).distinct().select_related('owner', 'assigned_inspector__user')
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ProjectCreateSerializer
        return ProjectListSerializer
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ProjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a project.
    """
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'
    lookup_url_kwarg = 'project_id'
    
    def get_queryset(self):
        user = self.request.user
        return Project.objects.filter(
            Q(owner=user) | Q(assigned_inspector__user=user)
        ).select_related('owner', 'assigned_inspector__user')
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return ProjectUpdateSerializer
        return ProjectDetailSerializer
    
    def perform_update(self, serializer):
        # Only allow owner to update project
        if self.get_object().owner != self.request.user:
            raise permissions.PermissionDenied("Only project owner can update project details.")
        serializer.save()
    
    def perform_destroy(self, instance):
        # Only allow owner to delete project
        if instance.owner != self.request.user:
            raise permissions.PermissionDenied("Only project owner can delete the project.")
        instance.delete()


class MilestoneListCreateView(generics.ListCreateAPIView):
    """
    List milestones for a project or create a new milestone.
    """
    serializer_class = ProjectMilestoneSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        project_id = self.kwargs['project_id']
        project = get_object_or_404(Project, id=project_id)
        
        # Check if user has access to this project
        if not (project.owner == self.request.user or 
                (project.assigned_inspector and project.assigned_inspector.user == self.request.user)):
            return ProjectMilestone.objects.none()
        
        return project.milestones.all()
    
    def perform_create(self, serializer):
        project_id = self.kwargs['project_id']
        project = get_object_or_404(Project, id=project_id)
        
        # Only project owner can create milestones
        if project.owner != self.request.user:
            raise permissions.PermissionDenied("Only project owner can create milestones.")
        
        serializer.save(project=project)


class MilestoneDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a milestone.
    """
    serializer_class = ProjectMilestoneSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'
    lookup_url_kwarg = 'milestone_id'
    
    def get_queryset(self):
        user = self.request.user
        return ProjectMilestone.objects.filter(
            Q(project__owner=user) | Q(project__assigned_inspector__user=user)
        ).select_related('project__owner', 'project__assigned_inspector__user')


class ProjectUpdateListCreateView(generics.ListCreateAPIView):
    """
    List updates for a project or create a new update.
    """
    serializer_class = ProjectUpdateListSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        project_id = self.kwargs['project_id']
        project = get_object_or_404(Project, id=project_id)
        
        # Check if user has access to this project
        if not (project.owner == self.request.user or 
                (project.assigned_inspector and project.assigned_inspector.user == self.request.user)):
            return ProjectUpdate.objects.none()
        
        return project.updates.all().select_related('created_by')
    
    def perform_create(self, serializer):
        project_id = self.kwargs['project_id']
        project = get_object_or_404(Project, id=project_id)
        
        # Check if user has access to this project
        if not (project.owner == self.request.user or 
                (project.assigned_inspector and project.assigned_inspector.user == self.request.user)):
            raise permissions.PermissionDenied("You don't have permission to create updates for this project.")
        
        serializer.save(project=project, created_by=self.request.user)


class ProjectUpdateDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a project update.
    """
    serializer_class = ProjectUpdateListSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'
    lookup_url_kwarg = 'update_id'
    
    def get_queryset(self):
        user = self.request.user
        return ProjectUpdate.objects.filter(
            Q(project__owner=user) | Q(project__assigned_inspector__user=user) | Q(created_by=user)
        ).select_related('project__owner', 'created_by')


class DocumentListCreateView(generics.ListCreateAPIView):
    """
    List documents for a project or upload a new document.
    """
    serializer_class = ProjectDocumentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        project_id = self.kwargs['project_id']
        project = get_object_or_404(Project, id=project_id)
        
        # Check if user has access to this project
        if not (project.owner == self.request.user or 
                (project.assigned_inspector and project.assigned_inspector.user == self.request.user)):
            return ProjectDocument.objects.none()
        
        return project.documents.all().select_related('uploaded_by')
    
    def perform_create(self, serializer):
        project_id = self.kwargs['project_id']
        project = get_object_or_404(Project, id=project_id)
        
        # Check if user has access to this project
        if not (project.owner == self.request.user or 
                (project.assigned_inspector and project.assigned_inspector.user == self.request.user)):
            raise permissions.PermissionDenied("You don't have permission to upload documents for this project.")
        
        serializer.save(project=project, uploaded_by=self.request.user)


class DocumentDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a document.
    """
    serializer_class = ProjectDocumentSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'
    lookup_url_kwarg = 'document_id'
    
    def get_queryset(self):
        user = self.request.user
        return ProjectDocument.objects.filter(
            Q(project__owner=user) | Q(project__assigned_inspector__user=user) | Q(uploaded_by=user)
        ).select_related('project__owner', 'uploaded_by')


class CommentListCreateView(generics.ListCreateAPIView):
    """
    List comments for a project or create a new comment.
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        project_id = self.kwargs['project_id']
        project = get_object_or_404(Project, id=project_id)
        
        # Check if user has access to this project
        if not (project.owner == self.request.user or 
                (project.assigned_inspector and project.assigned_inspector.user == self.request.user)):
            return ProjectComment.objects.none()
        
        return project.comments.all().select_related('author')


class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a comment.
    """
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'
    lookup_url_kwarg = 'comment_id'
    
    def get_queryset(self):
        user = self.request.user
        return ProjectComment.objects.filter(
            Q(project__owner=user) | Q(project__assigned_inspector__user=user) | Q(author=user)
        ).select_related('project__owner', 'author')


class InspectionReportListView(generics.ListAPIView):
    """
    List inspection reports for projects accessible to the user.
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        return InspectionReport.objects.filter(
            Q(project__owner=user) | Q(project__assigned_inspector__user=user) | Q(inspector__user=user)
        ).select_related('project', 'inspector__user')


class InspectionReportDetailView(generics.RetrieveAPIView):
    """
    Retrieve an inspection report.
    """
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'
    lookup_url_kwarg = 'report_id'
    
    def get_queryset(self):
        user = self.request.user
        return InspectionReport.objects.filter(
            Q(project__owner=user) | Q(project__assigned_inspector__user=user) | Q(inspector__user=user)
        ).select_related('project', 'inspector__user')
