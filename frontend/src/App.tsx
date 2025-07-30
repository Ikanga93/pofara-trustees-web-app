import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { AuthProvider } from './contexts/AuthContext';
import Layout from './components/layout/Layout';
import ProtectedRoute from './components/auth/ProtectedRoute';

// Pages
import LandingPage from './pages/LandingPage';
import LoginPage from './pages/auth/LoginPage';
import RegisterPage from './pages/auth/RegisterPage';
import OnboardingPage from './pages/OnboardingPage';
import DashboardPage from './pages/DashboardPage';
import ProjectsPage from './pages/projects/ProjectsPage';
import ProjectDetailsPage from './pages/projects/ProjectDetailsPage';
import InspectorsPage from './pages/inspectors/InspectorsPage';
import InspectorDetailsPage from './pages/inspectors/InspectorDetailsPage';
import MessagingPage from './pages/messaging/MessagingPage';
import ProfilePage from './pages/ProfilePage';

// Create a query client
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 5 * 60 * 1000, // 5 minutes
      retry: 1,
    },
  },
});

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <AuthProvider>
        <Router>
          <div className="min-h-screen bg-gray-50">
            <Routes>
              {/* Public routes */}
              <Route path="/" element={<LandingPage />} />
              <Route path="/login" element={<LoginPage />} />
              <Route path="/register" element={<RegisterPage />} />
              
              {/* Onboarding route */}
              <Route path="/onboarding" element={<ProtectedRoute><OnboardingPage /></ProtectedRoute>} />
              
              {/* Protected routes */}
              <Route path="/dashboard" element={<ProtectedRoute><Layout /></ProtectedRoute>}>
                <Route index element={<DashboardPage />} />
              </Route>
              <Route path="/projects" element={<ProtectedRoute><Layout /></ProtectedRoute>}>
                <Route index element={<ProjectsPage />} />
                <Route path=":id" element={<ProjectDetailsPage />} />
              </Route>
              <Route path="/inspectors" element={<ProtectedRoute><Layout /></ProtectedRoute>}>
                <Route index element={<InspectorsPage />} />
                <Route path=":id" element={<InspectorDetailsPage />} />
              </Route>
              <Route path="/messages" element={<ProtectedRoute><Layout /></ProtectedRoute>}>
                <Route index element={<MessagingPage />} />
              </Route>
              <Route path="/profile" element={<ProtectedRoute><Layout /></ProtectedRoute>}>
                <Route index element={<ProfilePage />} />
              </Route>
              
              {/* Catch all route - redirect to landing page */}
              <Route path="*" element={<Navigate to="/" replace />} />
            </Routes>
          </div>
        </Router>
      </AuthProvider>
    </QueryClientProvider>
  );
}

export default App;
