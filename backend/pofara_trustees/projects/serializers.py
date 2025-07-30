"""
Serializers for projects app.
"""

from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Project, ProjectMilestone, ProjectUpdate, ProjectDocument, InspectionReport, ProjectComment

User = get_user_model()


class ProjectListSerializer(serializers.ModelSerializer):
    """Serializer for project list view with essential fields only."""
    
    owner_name = serializers.CharField(source='owner.get_full_name', read_only=True)
    days_remaining = serializers.ReadOnlyField()
    budget_remaining = serializers.ReadOnlyField()
    is_overdue = serializers.ReadOnlyField()
    
    class Meta:
        model = Project
        fields = [
            'id', 'project_number', 'title', 'description', 'project_type', 
            'status', 'priority', 'country', 'city', 'total_budget', 
            'budget_currency', 'completion_percentage', 'planned_start_date', 
            'planned_end_date', 'created_at', 'owner_name', 'days_remaining',
            'budget_remaining', 'is_overdue'
        ]


class ProjectCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating new projects."""
    
    class Meta:
        model = Project
        fields = [
            'title', 'description', 'project_type', 'priority', 'country', 
            'state_province', 'city', 'address', 'postal_code', 
            'coordinates_lat', 'coordinates_lng', 'budget_currency', 
            'total_budget', 'planned_start_date', 'planned_end_date',
            'requirements', 'deliverables', 'stakeholders', 
            'communication_preferences', 'risk_assessment', 
            'compliance_requirements', 'quality_standards', 'success_criteria',
            'is_public', 'allow_inspector_applications', 'requires_background_check'
        ]
    
    def create(self, validated_data):
        # Set the owner to the current user
        validated_data['owner'] = self.context['request'].user
        
        # Generate project number (simple implementation)
        import uuid
        validated_data['project_number'] = f"POF-{str(uuid.uuid4())[:8].upper()}"
        
        return super().create(validated_data)


class ProjectDetailSerializer(serializers.ModelSerializer):
    """Detailed project serializer with all fields."""
    
    owner_name = serializers.CharField(source='owner.get_full_name', read_only=True)
    owner_email = serializers.CharField(source='owner.email', read_only=True)
    assigned_inspector_name = serializers.CharField(source='assigned_inspector.user.get_full_name', read_only=True)
    days_remaining = serializers.ReadOnlyField()
    budget_remaining = serializers.ReadOnlyField()
    budget_utilization_percentage = serializers.ReadOnlyField()
    is_overdue = serializers.ReadOnlyField()
    
    class Meta:
        model = Project
        fields = '__all__'
        read_only_fields = ['id', 'project_number', 'owner', 'created_at', 'updated_at']


class ProjectUpdateSerializer(serializers.ModelSerializer):
    """Serializer for project updates."""
    
    class Meta:
        model = Project
        fields = [
            'title', 'description', 'project_type', 'priority', 'status', 
            'country', 'state_province', 'city', 'address', 'postal_code',
            'coordinates_lat', 'coordinates_lng', 'budget_currency', 
            'total_budget', 'planned_start_date', 'planned_end_date',
            'requirements', 'deliverables', 'stakeholders', 
            'communication_preferences', 'risk_assessment', 
            'compliance_requirements', 'quality_standards', 'success_criteria',
            'is_public', 'allow_inspector_applications', 'requires_background_check'
        ]


# Additional serializers for related models (simplified)
class ProjectMilestoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectMilestone
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


class ProjectUpdateListSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    
    class Meta:
        model = ProjectUpdate
        fields = ['id', 'title', 'content', 'update_type', 'progress_percentage', 
                 'has_issues', 'issue_severity', 'created_by_name', 'created_at']


class ProjectDocumentSerializer(serializers.ModelSerializer):
    uploaded_by_name = serializers.CharField(source='uploaded_by.get_full_name', read_only=True)
    
    class Meta:
        model = ProjectDocument
        fields = '__all__'
        read_only_fields = ['uploaded_by', 'file_size', 'file_type', 'checksum', 'created_at', 'updated_at'] 