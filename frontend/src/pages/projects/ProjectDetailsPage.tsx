import React, { useState, useEffect } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { projectsAPI } from '../../services/api';
import { Project } from '../../types';
import {
  ArrowLeftIcon,
  MapPinIcon,
  CalendarIcon,
  ClockIcon,
  CheckCircleIcon,
  ExclamationTriangleIcon,
  ArrowPathIcon,
  UserIcon,
  BuildingOffice2Icon,
  ChartBarIcon,
  DocumentTextIcon,
  PencilIcon,
  TrashIcon,
} from '@heroicons/react/24/outline';

const ProjectDetailsPage = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [project, setProject] = useState<Project | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    if (!id) {
      navigate('/projects');
      return;
    }

    loadProject();
  }, [id, navigate]);

  const loadProject = async () => {
    try {
      setLoading(true);
      setError('');
      console.log('ProjectDetailsPage: Loading project with ID:', id);
      
      const response = await projectsAPI.getProject(id!);
      console.log('ProjectDetailsPage: Project loaded:', response.data);
      console.log('ProjectDetailsPage: Project type:', response.data?.projectType, 'Type of projectType:', typeof response.data?.projectType);
      
      setProject(response.data);
    } catch (err: any) {
      console.error('ProjectDetailsPage: Error loading project:', err);
      const errorMessage = err.response?.status === 404 
        ? 'Project not found' 
        : err.response?.data?.detail || err.message || 'Failed to load project details';
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed': return 'text-green-700 bg-green-100';
      case 'in_progress': return 'text-blue-700 bg-blue-100';
      case 'on_hold': return 'text-yellow-700 bg-yellow-100';
      case 'cancelled': return 'text-red-700 bg-red-100';
      case 'disputed': return 'text-purple-700 bg-purple-100';
      case 'pending_approval': return 'text-orange-700 bg-orange-100';
      case 'approved': return 'text-indigo-700 bg-indigo-100';
      default: return 'text-gray-700 bg-gray-100';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'completed': return CheckCircleIcon;
      case 'in_progress': return ArrowPathIcon;
      case 'on_hold': return ClockIcon;
      case 'cancelled': return ExclamationTriangleIcon;
      case 'disputed': return ExclamationTriangleIcon;
      default: return ClockIcon;
    }
  };

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'urgent': return 'text-red-700 bg-red-100';
      case 'high': return 'text-orange-700 bg-orange-100';
      case 'medium': return 'text-yellow-700 bg-yellow-100';
      case 'low': return 'text-green-700 bg-green-100';
      default: return 'text-gray-700 bg-gray-100';
    }
  };

  const formatDate = (dateString: string | undefined) => {
    if (!dateString) return 'Not set';
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  };

  const formatProjectType = (type: string | undefined) => {
    if (!type) return 'Not specified';
    return type.split('_').map(word => 
      word.charAt(0).toUpperCase() + word.slice(1)
    ).join(' ');
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          {/* Loading State */}
          <div className="animate-pulse">
            <div className="h-8 bg-gray-200 rounded w-64 mb-6"></div>
            <div className="bg-white rounded-lg shadow p-6 mb-6">
              <div className="h-6 bg-gray-200 rounded w-48 mb-4"></div>
              <div className="space-y-3">
                <div className="h-4 bg-gray-200 rounded w-full"></div>
                <div className="h-4 bg-gray-200 rounded w-3/4"></div>
                <div className="h-4 bg-gray-200 rounded w-1/2"></div>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="bg-white rounded-lg shadow p-8 text-center">
            <ExclamationTriangleIcon className="w-16 h-16 text-red-500 mx-auto mb-4" />
            <h2 className="text-2xl font-bold text-gray-900 mb-2">Error Loading Project</h2>
            <p className="text-gray-600 mb-6">{error}</p>
            <div className="space-x-4">
              <button
                onClick={() => navigate('/projects')}
                className="bg-gray-600 text-white px-6 py-2 rounded-lg hover:bg-gray-700 transition-colors"
              >
                Back to Projects
              </button>
              <button
                onClick={loadProject}
                className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition-colors"
              >
                Try Again
              </button>
            </div>
          </div>
        </div>
      </div>
    );
  }

  if (!project) {
    return null;
  }

  const StatusIcon = getStatusIcon(project.status);

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center mb-4">
            <Link
              to="/projects"
              className="flex items-center text-gray-600 hover:text-gray-900 transition-colors mr-4"
            >
              <ArrowLeftIcon className="w-5 h-5 mr-2" />
              Back to Projects
            </Link>
          </div>
          
          <div className="flex items-start justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-900 mb-2">{project.title || 'Untitled Project'}</h1>
              <p className="text-gray-600 text-lg">Project #{project.projectNumber || 'N/A'}</p>
            </div>
            
            <div className="flex items-center space-x-3">
              <span className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ${getStatusColor(project.status)}`}>
                <StatusIcon className="w-4 h-4 mr-1.5" />
                {project.status.replace('_', ' ').toUpperCase()}
              </span>
              <span className={`inline-flex px-3 py-1 rounded-full text-sm font-medium ${getPriorityColor(project.priority)}`}>
                {project.priority.toUpperCase()} PRIORITY
              </span>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Main Content */}
          <div className="lg:col-span-2 space-y-6">
            {/* Project Overview */}
            <div className="bg-white rounded-lg shadow p-6">
              <h2 className="text-xl font-semibold text-gray-900 mb-4 flex items-center">
                <DocumentTextIcon className="w-5 h-5 mr-2" />
                Project Overview
              </h2>
              <p className="text-gray-700 leading-relaxed">{project.description || 'No description provided'}</p>
            </div>

            {/* Location & Timeline */}
            <div className="bg-white rounded-lg shadow p-6">
              <h2 className="text-xl font-semibold text-gray-900 mb-4 flex items-center">
                <MapPinIcon className="w-5 h-5 mr-2" />
                Location & Timeline
              </h2>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <h3 className="font-medium text-gray-900 mb-2">Location</h3>
                  <p className="text-gray-600">{project.address || 'Not specified'}</p>
                  <p className="text-gray-600">{project.city || 'N/A'}, {project.country || 'N/A'}</p>
                  {project.coordinates && (
                    <p className="text-sm text-gray-500 mt-1">
                      {project.coordinates.lat}, {project.coordinates.lng}
                    </p>
                  )}
                </div>
                <div>
                  <h3 className="font-medium text-gray-900 mb-2">Timeline</h3>
                  <div className="space-y-2 text-sm">
                    <div className="flex justify-between">
                      <span className="text-gray-600">Planned Start:</span>
                      <span className="font-medium">{formatDate(project.plannedStartDate)}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600">Planned End:</span>
                      <span className="font-medium">{formatDate(project.plannedEndDate)}</span>
                    </div>
                    {project.actualStartDate && (
                      <div className="flex justify-between">
                        <span className="text-gray-600">Actual Start:</span>
                        <span className="font-medium">{formatDate(project.actualStartDate)}</span>
                      </div>
                    )}
                    {project.actualEndDate && (
                      <div className="flex justify-between">
                        <span className="text-gray-600">Actual End:</span>
                        <span className="font-medium">{formatDate(project.actualEndDate)}</span>
                      </div>
                    )}
                  </div>
                </div>
              </div>
            </div>

            {/* Progress */}
            <div className="bg-white rounded-lg shadow p-6">
              <h2 className="text-xl font-semibold text-gray-900 mb-4 flex items-center">
                <ChartBarIcon className="w-5 h-5 mr-2" />
                Progress
              </h2>
              <div className="mb-4">
                <div className="flex justify-between text-sm font-medium text-gray-700 mb-2">
                  <span>Completion</span>
                  <span>{project.completionPercentage || 0}%</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-3">
                  <div
                    className="bg-blue-600 h-3 rounded-full transition-all duration-300"
                    style={{ width: `${project.completionPercentage || 0}%` }}
                  ></div>
                </div>
              </div>
              
              {/* Budget Information */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-6">
                <div className="text-center p-4 bg-gray-50 rounded-lg">
                  <p className="text-sm text-gray-600">Total Budget</p>
                  <p className="text-lg font-semibold text-gray-900">
                    {(project.totalBudget || 0) > 0 ? `${project.totalBudget} ${project.budgetCurrency || 'USD'}` : 'Not specified'}
                  </p>
                </div>
                <div className="text-center p-4 bg-gray-50 rounded-lg">
                  <p className="text-sm text-gray-600">Spent Amount</p>
                  <p className="text-lg font-semibold text-gray-900">
                    {project.spentAmount || 0} {project.budgetCurrency || 'USD'}
                  </p>
                </div>
                <div className="text-center p-4 bg-gray-50 rounded-lg">
                  <p className="text-sm text-gray-600">Escrow Amount</p>
                  <p className="text-lg font-semibold text-gray-900">
                    {project.escrowAmount || 0} {project.budgetCurrency || 'USD'}
                  </p>
                </div>
              </div>
            </div>

            {/* Requirements & Deliverables */}
            <div className="bg-white rounded-lg shadow p-6">
              <h2 className="text-xl font-semibold text-gray-900 mb-4">Requirements & Deliverables</h2>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <h3 className="font-medium text-gray-900 mb-3">Requirements</h3>
                  {Object.keys(project.requirements || {}).length > 0 ? (
                    <div className="space-y-2">
                      {Object.entries(project.requirements || {}).map(([key, value]) => (
                        <div key={key} className="flex justify-between text-sm">
                          <span className="text-gray-600 capitalize">{key.replace('_', ' ')}:</span>
                          <span className="font-medium">
                            {Array.isArray(value) ? value.join(', ') : String(value)}
                          </span>
                        </div>
                      ))}
                    </div>
                  ) : (
                    <p className="text-gray-500 text-sm">No specific requirements</p>
                  )}
                </div>
                <div>
                  <h3 className="font-medium text-gray-900 mb-3">Deliverables</h3>
                  {project.deliverables?.length > 0 ? (
                    <ul className="space-y-1">
                      {project.deliverables?.map((deliverable, index) => (
                        <li key={index} className="text-sm text-gray-600 flex items-start">
                          <span className="w-2 h-2 bg-blue-600 rounded-full mt-2 mr-2 flex-shrink-0"></span>
                          {deliverable}
                        </li>
                      ))}
                    </ul>
                  ) : (
                    <p className="text-gray-500 text-sm">No deliverables specified</p>
                  )}
                </div>
              </div>
            </div>
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            {/* Project Info */}
            <div className="bg-white rounded-lg shadow p-6">
              <h2 className="text-lg font-semibold text-gray-900 mb-4">Project Information</h2>
              <div className="space-y-3 text-sm">
                <div className="flex justify-between">
                  <span className="text-gray-600">Type:</span>
                  <span className="font-medium">{formatProjectType(project.projectType)}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Created:</span>
                  <span className="font-medium">{formatDate(project.createdAt)}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Last Updated:</span>
                  <span className="font-medium">{formatDate(project.updatedAt)}</span>
                </div>
              </div>
            </div>

            {/* Team */}
            <div className="bg-white rounded-lg shadow p-6">
              <h2 className="text-lg font-semibold text-gray-900 mb-4">Team</h2>
              <div className="space-y-4">
                <div className="flex items-center">
                  <div className="w-10 h-10 bg-blue-100 rounded-full flex items-center justify-center">
                    <UserIcon className="w-5 h-5 text-blue-600" />
                  </div>
                  <div className="ml-3">
                    <p className="text-sm font-medium text-gray-900">
                      {project.owner?.firstName || 'Unknown'} {project.owner?.lastName || 'User'}
                    </p>
                    <p className="text-xs text-gray-600">Project Owner</p>
                  </div>
                </div>
                
                {project.assignedInspector ? (
                  <div className="flex items-center">
                    <div className="w-10 h-10 bg-green-100 rounded-full flex items-center justify-center">
                      <BuildingOffice2Icon className="w-5 h-5 text-green-600" />
                    </div>
                    <div className="ml-3">
                      <p className="text-sm font-medium text-gray-900">
                        {project.assignedInspector.user?.firstName || 'Unknown'} {project.assignedInspector.user?.lastName || 'Inspector'}
                      </p>
                      <p className="text-xs text-gray-600">Assigned Inspector</p>
                    </div>
                  </div>
                ) : (
                  <div className="text-center py-4 text-gray-500">
                    <BuildingOffice2Icon className="w-8 h-8 mx-auto mb-2 text-gray-400" />
                    <p className="text-sm">No inspector assigned</p>
                  </div>
                )}
              </div>
            </div>

            {/* Actions */}
            <div className="bg-white rounded-lg shadow p-6">
              <h2 className="text-lg font-semibold text-gray-900 mb-4">Actions</h2>
              <div className="space-y-3">
                <button className="w-full flex items-center justify-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors">
                  <PencilIcon className="w-4 h-4 mr-2" />
                  Edit Project
                </button>
                <button className="w-full flex items-center justify-center px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors">
                  <TrashIcon className="w-4 h-4 mr-2" />
                  Delete Project
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProjectDetailsPage; 