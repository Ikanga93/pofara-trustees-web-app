import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { projectsAPI } from '../services/api';
import {
  CheckIcon,
  ArrowRightIcon,
  ArrowLeftIcon,
  HomeIcon,
  WrenchScrewdriverIcon,
  BuildingOffice2Icon,
  TruckIcon,
  BeakerIcon,
  ChartBarIcon,
  GlobeAltIcon,
  DocumentTextIcon,
  HeartIcon,
  EllipsisHorizontalIcon,
  CalendarDaysIcon,
  SparklesIcon,
  ShieldCheckIcon,
} from '@heroicons/react/24/outline';

const OnboardingPage = () => {
  const navigate = useNavigate();
  const { user } = useAuth();
  const [currentStep, setCurrentStep] = useState(1);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  
  const [selectedServices, setSelectedServices] = useState<string[]>([]);
  const [selectedCountries, setSelectedCountries] = useState<string[]>([]);
  const [timeline, setTimeline] = useState('');

  const services = [
    { 
      id: 'property_management', 
      name: 'Property Inspection', 
      description: 'Comprehensive property evaluation and assessment',
      icon: HomeIcon,
      color: 'from-blue-500 to-blue-600',
      bgColor: 'bg-blue-50'
    },
    { 
      id: 'construction', 
      name: 'Construction Monitoring', 
      description: 'Track construction progress and quality control',
      icon: WrenchScrewdriverIcon,
      color: 'from-orange-500 to-orange-600',
      bgColor: 'bg-orange-50'
    },
    { 
      id: 'renovation', 
      name: 'Renovation Oversight', 
      description: 'Monitor renovation projects and improvements',
      icon: BuildingOffice2Icon,
      color: 'from-purple-500 to-purple-600',
      bgColor: 'bg-purple-50'
    },
    { 
      id: 'business_setup', 
      name: 'Business Setup', 
      description: 'Business establishment and compliance assistance',
      icon: TruckIcon,
      color: 'from-green-500 to-green-600',
      bgColor: 'bg-green-50'
    },
    { 
      id: 'agriculture', 
      name: 'Agricultural Projects', 
      description: 'Farm and agriculture project monitoring',
      icon: BeakerIcon,
      color: 'from-emerald-500 to-emerald-600',
      bgColor: 'bg-emerald-50'
    },
    { 
      id: 'investment', 
      name: 'Investment Due Diligence', 
      description: 'Investment verification and risk analysis',
      icon: ChartBarIcon,
      color: 'from-indigo-500 to-indigo-600',
      bgColor: 'bg-indigo-50'
    },
    { 
      id: 'government_paperwork', 
      name: 'Government Paperwork', 
      description: 'Assistance with legal and regulatory compliance',
      icon: DocumentTextIcon,
      color: 'from-red-500 to-red-600',
      bgColor: 'bg-red-50'
    },
    { 
      id: 'donation', 
      name: 'Donation Projects', 
      description: 'Charitable donations and community projects',
      icon: HeartIcon,
      color: 'from-pink-500 to-pink-600',
      bgColor: 'bg-pink-50'
    },
    { 
      id: 'other', 
      name: 'Others', 
      description: 'Custom projects and specialized services',
      icon: EllipsisHorizontalIcon,
      color: 'from-gray-500 to-gray-600',
      bgColor: 'bg-gray-50'
    }
  ];

  const countries = [
    { name: 'Nigeria', flag: '🇳🇬', popular: true },
    { name: 'Ghana', flag: '🇬🇭', popular: true },
    { name: 'Kenya', flag: '🇰🇪', popular: true },
    { name: 'South Africa', flag: '🇿🇦', popular: true },
    { name: 'Ethiopia', flag: '🇪🇹', popular: false },
    { name: 'Tanzania', flag: '🇹🇿', popular: false },
    { name: 'Uganda', flag: '🇺🇬', popular: false },
    { name: 'Rwanda', flag: '🇷🇼', popular: false },
    { name: 'Senegal', flag: '🇸🇳', popular: false },
    { name: 'Cameroon', flag: '🇨🇲', popular: false },
    { name: 'Ivory Coast', flag: '🇨🇮', popular: false },
    { name: 'Zambia', flag: '🇿🇲', popular: false }
  ];

  const timelineOptions = [
    { value: '1', label: 'Within 1 month', description: 'Urgent project', icon: '🚀', popular: true },
    { value: '3', label: 'Within 3 months', description: 'Standard timeline', icon: '⏰', popular: true },
    { value: '6', label: 'Within 6 months', description: 'Flexible timeline', icon: '📅', popular: false },
    { value: '12', label: 'Within 1 year', description: 'Long-term project', icon: '🎯', popular: false }
  ];

  const toggleService = (serviceId: string) => {
    setSelectedServices(prev =>
      prev.includes(serviceId)
        ? prev.filter(id => id !== serviceId)
        : [...prev, serviceId]
    );
  };

  const toggleCountry = (country: string) => {
    setSelectedCountries(prev =>
      prev.includes(country)
        ? prev.filter(c => c !== country)
        : [...prev, country]
    );
  };

  const handleNext = () => {
    if (currentStep < 3) {
      setCurrentStep(currentStep + 1);
    }
  };

  const handleBack = () => {
    if (currentStep > 1) {
      setCurrentStep(currentStep - 1);
    }
  };

  const handleComplete = async () => {
    setLoading(true);
    setError('');
    
    try {
      const projectData = {
        title: selectedServices.map(id => services.find(s => s.id === id)?.name).join(', ') || 'New Project',
        description: `Project covering: ${selectedServices.map(id => services.find(s => s.id === id)?.name).join(', ')}`,
        project_type: selectedServices[0] || 'other',
        country: selectedCountries[0] || 'Nigeria',
        city: selectedCountries[0] ? `${selectedCountries[0]} City` : 'Lagos',
        address: 'Address to be determined during project setup',
                  budget_currency: 'USD',
          total_budget: 0, // No budget specified during creation
          planned_start_date: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
          planned_end_date: new Date(Date.now() + parseInt(timeline || '1') * 30 * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
          requirements: {
            services: selectedServices,
            countries: selectedCountries,
            timeline: timeline
          },
        deliverables: selectedServices.map(id => services.find(s => s.id === id)?.description || ''),
        priority: 'medium',
        is_public: false,
        allow_inspector_applications: true,
        requires_background_check: true
      };

      console.log('OnboardingPage: Sending project data:', JSON.stringify(projectData, null, 2));

      await projectsAPI.createProject(projectData);
      localStorage.removeItem('project_draft');
      
      navigate('/projects', { 
        replace: true,
        state: { message: 'Project created successfully!' }
      });
      
    } catch (err: any) {
      console.error('OnboardingPage: Error creating project:', err);
      console.log('OnboardingPage: Error response:', err.response?.data);
      
      let errorMessage = 'Failed to create project. Please try again.';
      
      if (err.response?.status === 400 && err.response?.data) {
        const errorData = err.response.data;
        console.log('OnboardingPage: Validation errors:', errorData);
        
        // Handle specific field validation errors
        if (typeof errorData === 'object') {
          const errorMessages = [];
          
          for (const [field, messages] of Object.entries(errorData)) {
            if (Array.isArray(messages)) {
              errorMessages.push(`${field}: ${messages.join(', ')}`);
            } else if (typeof messages === 'string') {
              errorMessages.push(`${field}: ${messages}`);
            }
          }
          
          if (errorMessages.length > 0) {
            errorMessage = `Validation errors: ${errorMessages.join('; ')}`;
          }
        } else if (typeof errorData === 'string') {
          errorMessage = errorData;
        }
      } else if (err.response?.data?.detail) {
        errorMessage = err.response.data.detail;
      } else if (err.message) {
        errorMessage = err.message;
      }
      
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  const canProceed = () => {
    switch (currentStep) {
      case 1: return selectedServices.length > 0;
      case 2: return selectedCountries.length > 0;
      case 3: return timeline !== '';
      default: return false;
    }
  };

  const getStepTitle = () => {
    switch (currentStep) {
      case 1: return 'What services do you need?';
      case 2: return 'Where is your project located?';
      case 3: return 'When do you need it completed?';
      default: return '';
    }
  };

  const getStepSubtitle = () => {
    switch (currentStep) {
      case 1: return 'Select all services that apply to your project. Our verified professionals will handle everything.';
      case 2: return 'Choose the countries where you need independent verification services.';
      case 3: return 'Set realistic expectations so we can prioritize and assign the best inspector.';
      default: return '';
    }
  };

  const renderStepContent = () => {
    switch (currentStep) {
      case 1:
        return (
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3">
            {services.map((service, index) => (
              <div
                key={service.id}
                onClick={() => toggleService(service.id)}
                className={`group relative p-4 rounded-lg cursor-pointer transition-all duration-200 border-2 ${
                  selectedServices.includes(service.id)
                    ? 'border-black bg-black text-white'
                    : 'border-gray-200 bg-white hover:border-gray-300 hover:shadow-sm'
                }`}
              >
                {/* Selection indicator */}
                <div className={`absolute top-2 right-2 w-5 h-5 rounded-full border-2 flex items-center justify-center transition-all duration-200 ${
                  selectedServices.includes(service.id)
                    ? 'border-white bg-white'
                    : 'border-gray-300 group-hover:border-gray-400'
                }`}>
                  {selectedServices.includes(service.id) && (
                    <CheckIcon className="w-3 h-3 text-black" />
                  )}
                </div>

                {/* Icon */}
                <div className={`w-10 h-10 rounded-lg flex items-center justify-center mb-3 transition-colors duration-200 ${
                  selectedServices.includes(service.id)
                    ? 'bg-white/10'
                    : 'bg-gray-100 group-hover:bg-gray-200'
                }`}>
                  <service.icon className={`w-5 h-5 transition-colors duration-200 ${
                    selectedServices.includes(service.id)
                      ? 'text-white'
                      : 'text-gray-700'
                  }`} />
                </div>

                {/* Content */}
                <h3 className={`text-sm font-semibold mb-1 leading-tight transition-colors duration-200 ${
                  selectedServices.includes(service.id)
                    ? 'text-white'
                    : 'text-gray-900'
                }`}>
                  {service.name}
                </h3>
                <p className={`text-xs leading-snug transition-colors duration-200 ${
                  selectedServices.includes(service.id)
                    ? 'text-gray-300'
                    : 'text-gray-600'
                }`}>
                  {service.description}
                </p>
              </div>
            ))}
          </div>
        );

      case 2:
        const popularCountries = countries.filter(c => c.popular);
        const otherCountries = countries.filter(c => !c.popular);
        
        return (
          <div className="space-y-8">
            {/* Popular Countries */}
            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
                <SparklesIcon className="w-5 h-5 mr-2 text-yellow-500" />
                Most Popular
              </h3>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                {popularCountries.map((country, index) => (
                  <div
                    key={country.name}
                    onClick={() => toggleCountry(country.name)}
                    className={`group p-4 border-2 rounded-xl cursor-pointer text-center transition-all duration-300 hover:shadow-md hover:-translate-y-1 ${
                      selectedCountries.includes(country.name)
                        ? 'border-blue-500 bg-blue-50 shadow-md'
                        : 'border-gray-200 hover:border-blue-300 bg-white'
                    }`}
                    style={{ animationDelay: `${index * 0.1}s` }}
                  >
                    <div className="text-3xl mb-2">{country.flag}</div>
                    <span className={`font-semibold transition-colors duration-300 ${
                      selectedCountries.includes(country.name) ? 'text-blue-700' : 'text-gray-900 group-hover:text-blue-600'
                    }`}>
                      {country.name}
                    </span>
                  </div>
                ))}
              </div>
            </div>

            {/* Other Countries */}
            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
                <GlobeAltIcon className="w-5 h-5 mr-2 text-gray-500" />
                Other Countries
              </h3>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                {otherCountries.map((country, index) => (
                  <div
                    key={country.name}
                    onClick={() => toggleCountry(country.name)}
                    className={`group p-4 border-2 rounded-xl cursor-pointer text-center transition-all duration-300 hover:shadow-md hover:-translate-y-1 ${
                      selectedCountries.includes(country.name)
                        ? 'border-blue-500 bg-blue-50 shadow-md'
                        : 'border-gray-200 hover:border-blue-300 bg-white'
                    }`}
                    style={{ animationDelay: `${index * 0.1}s` }}
                  >
                    <div className="text-3xl mb-2">{country.flag}</div>
                    <span className={`font-semibold transition-colors duration-300 ${
                      selectedCountries.includes(country.name) ? 'text-blue-700' : 'text-gray-900 group-hover:text-blue-600'
                    }`}>
                      {country.name}
                    </span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        );

      case 3:
        return (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {timelineOptions.map((option, index) => (
              <div
                key={option.value}
                onClick={() => setTimeline(option.value)}
                className={`group relative p-6 border-2 rounded-2xl cursor-pointer transition-all duration-300 hover:shadow-lg hover:-translate-y-1 ${
                  timeline === option.value
                    ? 'border-blue-500 bg-blue-50 shadow-lg'
                    : 'border-gray-200 hover:border-blue-300 bg-white'
                }`}
                style={{ animationDelay: `${index * 0.1}s` }}
              >
                {option.popular && (
                  <div className="absolute -top-3 left-1/2 transform -translate-x-1/2">
                    <span className="bg-green-500 text-white text-xs font-bold px-3 py-1 rounded-full">
                      Recommended
                    </span>
                  </div>
                )}

                <div className="text-center">
                  <div className="text-4xl mb-3">{option.icon}</div>
                  <h3 className={`text-xl font-bold mb-2 transition-colors duration-300 ${
                    timeline === option.value ? 'text-blue-700' : 'text-gray-900 group-hover:text-blue-600'
                  }`}>
                    {option.label}
                  </h3>
                  <p className="text-gray-600">
                    {option.description}
                  </p>
                </div>
              </div>
            ))}
          </div>
        );

      default:
        return null;
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 via-blue-50 to-indigo-50">
      {/* Header */}
      <div className="bg-white border-b border-gray-200 shadow-sm">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center">
              <h1 className="text-2xl font-bold text-black">Pofara</h1>
              <span className="ml-2 text-sm text-gray-500 font-medium">Trustees</span>
            </div>
            <button
              onClick={() => navigate('/dashboard')}
              className="text-sm text-gray-500 hover:text-black transition-colors duration-200"
            >
              Back to Dashboard
            </button>
          </div>
        </div>
      </div>

      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-6 sm:py-12">
        {/* Progress Section */}
        <div className="mb-8 sm:mb-12">
          {/* Step Indicators */}
          <div className="flex items-center justify-center mb-8">
            {[1, 2, 3].map((step, index) => (
              <div key={step} className="flex items-center">
                <div className={`flex items-center justify-center w-12 h-12 rounded-full text-sm font-bold transition-all duration-300 ${
                  step <= currentStep
                    ? 'bg-blue-600 text-white shadow-lg shadow-blue-600/30'
                    : 'bg-gray-200 text-gray-500'
                }`}>
                  {step < currentStep ? (
                    <CheckIcon className="w-6 h-6" />
                  ) : (
                    step
                  )}
                </div>
                {index < 2 && (
                  <div className={`w-16 h-1 mx-4 rounded-full transition-all duration-300 ${
                    step < currentStep ? 'bg-blue-600' : 'bg-gray-200'
                  }`} />
                )}
              </div>
            ))}
          </div>

          {/* Progress Bar */}
          <div className="max-w-2xl mx-auto">
            <div className="flex items-center justify-between text-sm font-medium text-gray-600 mb-2">
              <span>Step {currentStep} of 3</span>
              <span>{Math.round((currentStep / 3) * 100)}% Complete</span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-3 shadow-inner">
              <div
                className="bg-gradient-to-r from-blue-600 to-indigo-600 h-3 rounded-full transition-all duration-500 shadow-lg"
                style={{ width: `${(currentStep / 3) * 100}%` }}
              />
            </div>
          </div>
        </div>

        {/* Error Message */}
        {error && (
          <div className="max-w-4xl mx-auto mb-8">
            <div className="bg-red-50 border border-red-200 rounded-xl p-4">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <ShieldCheckIcon className="w-5 h-5 text-red-600" />
                </div>
                <div className="ml-3">
                  <p className="text-red-800 font-medium">{error}</p>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Main Content */}
        <div className="max-w-4xl mx-auto">
          {/* Step Header */}
          <div className="text-center mb-12">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">
              {getStepTitle()}
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto leading-relaxed">
              {getStepSubtitle()}
            </p>
          </div>

          {/* Step Content */}
          <div className="bg-white rounded-3xl shadow-xl border border-gray-100 p-4 sm:p-6 lg:p-8 mb-8">
            {renderStepContent()}
          </div>

          {/* Navigation */}
          <div className="flex justify-between items-center">
            <button
              onClick={handleBack}
              disabled={currentStep === 1}
              className={`flex items-center px-8 py-4 rounded-xl font-medium transition-all duration-200 ${
                currentStep === 1
                  ? 'text-gray-400 cursor-not-allowed'
                  : 'text-gray-700 hover:text-gray-900 border-2 border-gray-300 hover:border-gray-400 bg-white hover:shadow-md'
              }`}
            >
              <ArrowLeftIcon className="w-5 h-5 mr-2" />
              Back
            </button>

            {currentStep < 3 ? (
              <button
                onClick={handleNext}
                disabled={!canProceed()}
                className={`flex items-center px-8 py-4 rounded-xl font-medium transition-all duration-200 ${
                  canProceed()
                    ? 'bg-gradient-to-r from-blue-600 to-indigo-600 text-white hover:from-blue-700 hover:to-indigo-700 shadow-lg hover:shadow-xl transform hover:-translate-y-0.5'
                    : 'bg-gray-300 text-gray-500 cursor-not-allowed'
                }`}
              >
                Continue
                <ArrowRightIcon className="w-5 h-5 ml-2" />
              </button>
            ) : (
              <button
                onClick={handleComplete}
                disabled={!canProceed() || loading}
                className={`flex items-center px-8 py-4 rounded-xl font-medium transition-all duration-200 ${
                  canProceed() && !loading
                    ? 'bg-gradient-to-r from-green-600 to-emerald-600 text-white hover:from-green-700 hover:to-emerald-700 shadow-lg hover:shadow-xl transform hover:-translate-y-0.5'
                    : 'bg-gray-300 text-gray-500 cursor-not-allowed'
                }`}
              >
                {loading ? (
                  <>
                    <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
                    Creating Project...
                  </>
                ) : (
                  <>
                    <CheckIcon className="w-5 h-5 mr-2" />
                    Create Project
                  </>
                )}
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default OnboardingPage;