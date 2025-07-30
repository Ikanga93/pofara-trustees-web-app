import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import {
  PlusIcon,
  EyeIcon,
  DocumentTextIcon,
  ArrowRightIcon,
  FolderOpenIcon,
} from '@heroicons/react/24/outline';

const DashboardPage = () => {
  const { user } = useAuth();
  const navigate = useNavigate();

  const handleCreateProject = () => {
    navigate('/onboarding');
  };

  const handleViewProjects = () => {
    navigate('/projects');
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-black">
            Welcome back, {user?.first_name}
          </h1>
          <p className="text-gray-600 mt-2">
            Here's what's happening with your projects across Africa
          </p>
        </div>

        {/* Create Project CTA */}
        <div className="mb-8">
          <div className="bg-gradient-to-r from-black to-gray-800 rounded-2xl p-8 text-white">
            <div className="flex items-center justify-between">
              <div>
                <h2 className="text-2xl font-bold mb-2">Ready to start a new project?</h2>
                <p className="text-gray-300 mb-4">
                  Connect with verified local inspectors in just a few simple steps
                </p>
                <button
                  onClick={handleCreateProject}
                  className="inline-flex items-center px-6 py-3 bg-white text-black font-medium rounded-lg hover:bg-gray-100 transition-colors duration-200"
                >
                  <PlusIcon className="w-5 h-5 mr-2" />
                  Create a project
                </button>
              </div>
              <div className="hidden md:block">
                <div className="w-24 h-24 bg-white/10 rounded-full flex items-center justify-center">
                  <DocumentTextIcon className="w-12 h-12 text-white/80" />
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Quick Actions - Full Width */}
        <div className="max-w-4xl mx-auto mb-8">
          <div className="bg-white rounded-2xl border border-gray-200 p-8">
            <h3 className="text-2xl font-semibold text-black mb-8 text-center">Quick Actions</h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <button
                onClick={handleViewProjects}
                className="flex flex-col items-center p-6 border border-gray-200 rounded-xl hover:border-blue-500 hover:shadow-lg transition-all duration-200 group"
            >
                <div className="w-16 h-16 bg-blue-500 rounded-2xl flex items-center justify-center mb-4 group-hover:scale-110 transition-transform duration-200">
                  <FolderOpenIcon className="w-8 h-8 text-white" />
                </div>
                <div className="text-center">
                  <p className="font-semibold text-gray-900 text-lg mb-2">View Projects</p>
                  <p className="text-sm text-gray-500">See your existing projects and track progress</p>
                </div>
              </button>

              <button className="flex flex-col items-center p-6 border border-gray-200 rounded-xl hover:border-gray-300 hover:shadow-lg transition-all duration-200 group">
                <div className="w-16 h-16 bg-gray-100 rounded-2xl flex items-center justify-center mb-4 group-hover:scale-110 transition-transform duration-200">
                  <EyeIcon className="w-8 h-8 text-gray-600" />
                </div>
                <div className="text-center">
                  <p className="font-semibold text-gray-900 text-lg mb-2">Browse Inspectors</p>
                  <p className="text-sm text-gray-500">Find local experts in your project area</p>
                </div>
              </button>

              <button className="flex flex-col items-center p-6 border border-gray-200 rounded-xl hover:border-gray-300 hover:shadow-lg transition-all duration-200 group">
                <div className="w-16 h-16 bg-gray-100 rounded-2xl flex items-center justify-center mb-4 group-hover:scale-110 transition-transform duration-200">
                  <DocumentTextIcon className="w-8 h-8 text-gray-600" />
                </div>
                <div className="text-center">
                  <p className="font-semibold text-gray-900 text-lg mb-2">View Reports</p>
                  <p className="text-sm text-gray-500">Access your inspection reports and documents</p>
                </div>
              </button>
            </div>
          </div>
        </div>

        {/* Need Help Section */}
        <div className="bg-blue-50 rounded-2xl p-8 border border-blue-200">
          <div className="text-center">
            <h3 className="text-2xl font-semibold text-blue-900 mb-4">Need an inspection?</h3>
            <p className="text-blue-700 text-lg mb-6 max-w-2xl mx-auto">
                Our network of verified inspectors across Africa is ready to help with your next project.
              Get professional verification, transparent pricing, and peace of mind.
              </p>
            <button
              onClick={handleCreateProject}
              className="bg-blue-600 text-white px-8 py-4 rounded-xl font-semibold hover:bg-blue-700 transition-colors duration-200 text-lg"
            >
              Get started now
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DashboardPage; 