import React, { useState, useEffect } from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { projectsAPI } from '../../services/api';
import { Project } from '../../types';
import {
  PlusIcon,
  EyeIcon,
  CalendarIcon,
  MapPinIcon,
  ClockIcon,
  CheckCircleIcon,
  ExclamationTriangleIcon,
  ArrowPathIcon,
  FolderIcon,
} from '@heroicons/react/24/outline';

const ProjectsPage = () => {
  console.log('ProjectsPage: Component is rendering');
  
  const [projects, setProjects] = useState<Project[]>([]);
  console.log('ProjectsPage: Initial projects state:', projects);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [retryCount, setRetryCount] = useState(0);
  const location = useLocation();
  const navigate = useNavigate();

  // Show success message if coming from onboarding
  const [showSuccess, setShowSuccess] = useState(false);

  useEffect(() => {
    console.log('ProjectsPage: useEffect for location.state triggered');
    if (location.state?.message) {
      setShowSuccess(true);
      // Clear the message after showing it
      window.history.replaceState({}, document.title);
      setTimeout(() => setShowSuccess(false), 5000);
    }
  }, [location]);

  useEffect(() => {
    console.log('ProjectsPage: useEffect for loadProjects triggered');
    loadProjects();
  }, []);

  const loadProjects = async (isRetry: boolean = false) => {
    console.log('ProjectsPage: loadProjects called, isRetry:', isRetry);
    
    try {
      if (!isRetry) {
        setLoading(true);
      }
      setError('');
      
      console.log('ProjectsPage: Making API call to get projects');
      const response = await projectsAPI.getProjects();
      console.log('ProjectsPage: API response received:', response);
      
      // Handle different response structures
      let projectsData = [];
      if (response.data) {
        if (Array.isArray(response.data)) {
          projectsData = response.data;
        } else if (response.data.results && Array.isArray(response.data.results)) {
          // Handle paginated responses
          projectsData = response.data.results;
        } else if (response.data.projects && Array.isArray(response.data.projects)) {
          // Handle nested projects
          projectsData = response.data.projects;
        } else {
          console.warn('ProjectsPage: Unexpected response structure:', response.data);
          projectsData = [];
        }
      }
      
      console.log('ProjectsPage: Processed projects data:', projectsData);
      setProjects(projectsData);
      setRetryCount(0);
    } catch (err: any) {
      console.error('ProjectsPage: Error loading projects:', err);
      const errorMessage = err.response?.data?.detail || err.message || 'Failed to load projects. Please try again.';
      setError(errorMessage);
      
      // Ensure projects is an empty array on error
      setProjects([]);
      
      // Auto-retry up to 2 times for network errors
      if (retryCount < 2 && (err.code === 'NETWORK_ERROR' || err.response?.status >= 500)) {
        console.log('ProjectsPage: Retrying due to network error, retry count:', retryCount);
        setTimeout(() => {
          setRetryCount(prev => prev + 1);
          loadProjects(true);
        }, 2000);
      }
    } finally {
      console.log('ProjectsPage: Setting loading to false');
      setLoading(false);
    }
  };

  const handleRetry = () => {
    console.log('ProjectsPage: Manual retry triggered');
    setRetryCount(0);
    loadProjects();
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed':
        return 'bg-green-100 text-green-800';
      case 'in_progress':
        return 'bg-blue-100 text-blue-800';
      case 'pending_approval':
        return 'bg-yellow-100 text-yellow-800';
      case 'on_hold':
        return 'bg-red-100 text-red-800';
      case 'draft':
        return 'bg-gray-100 text-gray-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'completed':
        return <CheckCircleIcon className="w-4 h-4" />;
      case 'in_progress':
        return <ClockIcon className="w-4 h-4" />;
      case 'on_hold':
        return <ExclamationTriangleIcon className="w-4 h-4" />;
      default:
        return <ClockIcon className="w-4 h-4" />;
    }
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
    });
  };

  console.log('ProjectsPage: Current state - loading:', loading, 'error:', error, 'projects:', projects.length);

  // Safety check to ensure projects is always an array
  const safeProjects = Array.isArray(projects) ? projects : [];
  console.log('ProjectsPage: Safe projects count:', safeProjects.length, 'type:', typeof projects);

  if (loading) {
    console.log('ProjectsPage: Rendering loading state');
    return (
      <div className="min-h-screen bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          {/* Header Skeleton */}
          <div className="mb-8">
            <div className="h-8 bg-gray-200 rounded w-48 mb-2 animate-pulse"></div>
            <div className="h-4 bg-gray-200 rounded w-96 animate-pulse"></div>
          </div>
          
          {/* Loading State */}
          <div className="flex flex-col items-center justify-center py-20">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mb-4"></div>
            <p className="text-gray-600 font-medium">Loading your projects...</p>
            {retryCount > 0 && (
              <p className="text-sm text-gray-500 mt-2">Retrying... ({retryCount}/2)</p>
            )}
          </div>
        </div>
      </div>
    );
  }

  console.log('ProjectsPage: Rendering main content');

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Debug Info */}
        <div className="mb-4 p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
          <h3 className="text-sm font-medium text-yellow-800 mb-2">Debug Information:</h3>
          <ul className="text-xs text-yellow-700 space-y-1">
            <li>Loading: {loading.toString()}</li>
            <li>Error: {error || 'None'}</li>
            <li>Projects raw count: {Array.isArray(projects) ? projects.length : 'Not an array'}</li>
            <li>Projects type: {typeof projects}</li>
            <li>Safe projects count: {safeProjects.length}</li>
            <li>Retry count: {retryCount}</li>
            <li>Show success: {showSuccess.toString()}</li>
            <li>Location pathname: {location.pathname}</li>
            <li>Projects data: {JSON.stringify(projects).substring(0, 100)}...</li>
          </ul>
        </div>

        {/* Header */}
        <div className="sm:flex sm:items-center sm:justify-between mb-8">
          <div className="sm:flex-auto">
            <h1 className="text-3xl font-bold text-black">My Projects</h1>
            <p className="mt-2 text-lg text-gray-600">
              Manage your inspection projects and track their progress across Africa.
            </p>
          </div>
          <div className="mt-4 sm:mt-0 sm:ml-16 sm:flex-none">
            <Link
              to="/onboarding"
              className="inline-flex items-center justify-center rounded-xl bg-blue-600 px-6 py-3 text-sm font-semibold text-white shadow-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-all duration-200 hover:shadow-xl"
            >
              <PlusIcon className="w-5 h-5 mr-2" />
              New Project
            </Link>
          </div>
        </div>

        {/* Success Message */}
        {showSuccess && (
          <div className="rounded-xl bg-green-50 p-4 mb-6 border border-green-200">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <CheckCircleIcon className="h-6 w-6 text-green-600" />
              </div>
              <div className="ml-3">
                <p className="text-sm font-semibold text-green-800">
                  {location.state?.message || 'Project created successfully!'}
                </p>
              </div>
            </div>
          </div>
        )}

        {/* Error Message */}
        {error && (
          <div className="rounded-xl bg-red-50 p-6 mb-6 border border-red-200">
            <div className="flex items-center justify-between">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <ExclamationTriangleIcon className="h-6 w-6 text-red-600" />
                </div>
                <div className="ml-3">
                  <p className="text-sm font-semibold text-red-800">Unable to load projects</p>
                  <p className="text-sm text-red-700 mt-1">{error}</p>
                </div>
              </div>
              <button
                onClick={handleRetry}
                className="flex items-center px-4 py-2 bg-red-100 hover:bg-red-200 text-red-800 rounded-lg text-sm font-medium transition-colors duration-200"
              >
                <ArrowPathIcon className="w-4 h-4 mr-2" />
                Retry
              </button>
            </div>
          </div>
        )}

        {/* Projects Content */}
        {!error && (
          <>
            {safeProjects.length === 0 ? (
              // Empty State - Enhanced Design
              <div className="text-center bg-white shadow-lg rounded-2xl p-16 border border-gray-200">
                <div className="mx-auto h-32 w-32 text-gray-400 mb-6">
                  <FolderIcon className="h-32 w-32" />
                </div>
                <h3 className="text-2xl font-bold text-gray-900 mb-4">No projects yet</h3>
                <p className="text-lg text-gray-600 mb-8 max-w-md mx-auto">
                  Ready to get started? Create your first project and connect with verified inspectors across Africa.
                </p>
                <div className="space-y-4">
                  <Link
                    to="/onboarding"
                    className="inline-flex items-center px-8 py-4 bg-blue-600 text-white font-semibold rounded-xl hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-all duration-200 shadow-lg hover:shadow-xl"
                  >
                    <PlusIcon className="w-5 h-5 mr-2" />
                    Create Your First Project
                  </Link>
                  <div className="text-sm text-gray-500">
                    <p>✓ Professional verification</p>
                    <p>✓ Transparent pricing</p>
                    <p>✓ Real-time updates</p>
                  </div>
                </div>
              </div>
            ) : (
              // Projects Grid - Enhanced Design
              <>
                <div className="mb-6 flex items-center justify-between">
                  <p className="text-gray-600">
                    Showing <span className="font-semibold text-black">{safeProjects.length}</span> project{safeProjects.length !== 1 ? 's' : ''}
                  </p>
                </div>

                <div className="grid gap-8 sm:grid-cols-2 lg:grid-cols-3">
                  {safeProjects.map((project) => {
                    console.log('ProjectsPage: Rendering project:', project.id, typeof project.id, project);
                    
                    // Validate project ID (UUID string)
                    const validProjectId = project.id && typeof project.id === 'string' && project.id.trim() !== '' ? project.id : null;
                    if (!validProjectId) {
                      console.error('ProjectsPage: Invalid project ID:', project.id, 'for project:', project);
                    }
                    
                    return (
                      <div
                        key={project.id || `invalid-${Math.random()}`}
                        className="bg-white rounded-2xl shadow-lg hover:shadow-xl transition-all duration-300 overflow-hidden border border-gray-200 hover:border-gray-300"
                      >
                        <div className="p-8">
                          {/* Header */}
                          <div className="flex items-start justify-between mb-6">
                            <div className="flex-1 min-w-0">
                              <h3 className="text-xl font-bold text-gray-900 truncate mb-2">
                                {project.title}
                              </h3>
                              <p className="text-sm text-gray-500 font-medium">
                                {project.projectNumber}
                              </p>
                            </div>
                            <span
                              className={`inline-flex items-center px-3 py-1 rounded-full text-xs font-semibold ${getStatusColor(
                                project.status
                              )}`}
                            >
                              {getStatusIcon(project.status)}
                              <span className="ml-1.5 capitalize">{project.status.replace('_', ' ')}</span>
                            </span>
                          </div>

                          {/* Description */}
                          <p className="text-gray-600 text-sm mb-6 line-clamp-3 leading-relaxed">
                            {project.description}
                          </p>

                          {/* Project Details */}
                          <div className="space-y-3 mb-6">
                            <div className="flex items-center text-sm text-gray-600">
                              <MapPinIcon className="w-4 h-4 mr-3 text-gray-400" />
                              <span>{project.city}, {project.country}</span>
                            </div>
                            <div className="flex items-center text-sm text-gray-600">
                              <CalendarIcon className="w-4 h-4 mr-3 text-gray-400" />
                              <span>Due {formatDate(project.plannedEndDate)}</span>
                            </div>
                          </div>

                          {/* Progress Bar */}
                          <div className="mb-6">
                            <div className="flex items-center justify-between text-sm font-medium text-gray-700 mb-2">
                              <span>Progress</span>
                              <span>{project.completionPercentage}%</span>
                            </div>
                            <div className="w-full bg-gray-200 rounded-full h-3 shadow-inner">
                              <div
                                className="bg-gradient-to-r from-blue-500 to-blue-600 h-3 rounded-full transition-all duration-500 shadow-sm"
                                style={{ width: `${project.completionPercentage}%` }}
                              ></div>
                            </div>
                          </div>

                          {/* Overdue Warning */}
                          {new Date(project.plannedEndDate) < new Date() && project.status !== 'completed' && (
                            <div className="mb-6 p-3 bg-red-50 border border-red-200 rounded-lg">
                              <div className="flex items-center">
                                <ExclamationTriangleIcon className="w-4 h-4 text-red-600 mr-2" />
                                <span className="text-sm text-red-800 font-semibold">Project is overdue</span>
                              </div>
                            </div>
                          )}

                          {/* Actions */}
                          <div className="flex space-x-3">
                            {validProjectId ? (
                              <Link
                                to={`/projects/${validProjectId}`}
                                className="flex-1 bg-black text-white text-center px-4 py-3 rounded-xl text-sm font-semibold hover:bg-gray-800 transition-colors duration-200 flex items-center justify-center"
                              >
                                <EyeIcon className="w-4 h-4 mr-2" />
                                View Details
                              </Link>
                            ) : (
                              <div className="flex-1 bg-gray-300 text-gray-500 text-center px-4 py-3 rounded-xl text-sm font-semibold cursor-not-allowed flex items-center justify-center">
                                <ExclamationTriangleIcon className="w-4 h-4 mr-2" />
                                Invalid Project ID
                              </div>
                            )}
                          </div>
                        </div>
                      </div>
                    );
                  })}
                </div>
              </>
            )}
          </>
        )}
      </div>
    </div>
  );
};

export default ProjectsPage; 