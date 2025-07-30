// User and Authentication Types
export interface User {
  id: string;
  username: string;
  email: string;
  firstName: string;
  lastName: string;
  role: 'admin' | 'user' | 'inspector' | 'support';
  status: 'active' | 'inactive' | 'suspended' | 'pending';
  phoneNumber?: string;
  phoneVerified: boolean;
  emailVerified: boolean;
  avatar?: string;
  createdAt: string;
  updatedAt: string;
}

export interface UserProfile {
  id: string;
  user: string;
  avatar?: string;
  dateOfBirth?: string;
  gender?: 'male' | 'female' | 'other' | 'prefer_not_to_say';
  bio?: string;
  country?: string;
  city?: string;
  address?: string;
  countryOfOrigin?: string;
  languagesSpoken: string[];
  kycStatus: 'pending' | 'in_review' | 'approved' | 'rejected' | 'additional_info_required';
  timezone: string;
  languagePreference: string;
}

// Inspector Types
export interface Inspector {
  id: string;
  user: User;
  status: 'pending' | 'in_review' | 'approved' | 'rejected' | 'suspended' | 'inactive';
  verificationLevel: number;
  experienceLevel: 'entry' | 'junior' | 'senior' | 'expert';
  yearsOfExperience: number;
  specializations: string[];
  skills: string[];
  languagesSpoken: string[];
  serviceRegions: string[];
  travelRadiusKm: number;
  baseHourlyRate: number;
  totalInspections: number;
  completedInspections: number;
  averageRating: number;
  totalRatings: number;
  isAvailable: boolean;
  bio?: string;
  createdAt: string;
  updatedAt: string;
}

// Project Types
export interface Project {
  id: string;
  projectNumber: string;
  owner: User;
  assignedInspector?: Inspector;
  title: string;
  description: string;
  projectType: 'construction' | 'renovation' | 'business_setup' | 'property_management' | 'agriculture' | 'investment' | 'other';
  status: 'draft' | 'pending_approval' | 'approved' | 'in_progress' | 'on_hold' | 'completed' | 'cancelled' | 'disputed';
  priority: 'low' | 'medium' | 'high' | 'urgent';
  country: string;
  city: string;
  address: string;
  coordinates?: {
    lat: number;
    lng: number;
  };
  budgetCurrency: string;
  totalBudget: number;
  spentAmount: number;
  escrowAmount: number;
  plannedStartDate: string;
  plannedEndDate: string;
  actualStartDate?: string;
  actualEndDate?: string;
  completionPercentage: number;
  requirements: Record<string, any>;
  deliverables: string[];
  createdAt: string;
  updatedAt: string;
}

export interface ProjectMilestone {
  id: string;
  project: string;
  title: string;
  description: string;
  order: number;
  status: 'pending' | 'in_progress' | 'completed' | 'overdue' | 'cancelled';
  plannedStartDate: string;
  plannedEndDate: string;
  actualStartDate?: string;
  actualEndDate?: string;
  budgetAllocation: number;
  actualCost: number;
  paymentReleased: boolean;
  requiresInspection: boolean;
  inspectionCompleted: boolean;
  completionPercentage: number;
  createdAt: string;
  updatedAt: string;
}

// Messaging Types
export interface Conversation {
  id: string;
  conversationType: 'direct' | 'group' | 'project' | 'support' | 'announcement';
  status: 'active' | 'archived' | 'closed' | 'suspended';
  title?: string;
  description?: string;
  participants: User[];
  lastMessageAt?: string;
  messageCount: number;
  isEncrypted: boolean;
  createdBy: User;
  createdAt: string;
  updatedAt: string;
}

export interface Message {
  id: string;
  conversation: string;
  sender: User;
  messageType: 'text' | 'file' | 'image' | 'video' | 'audio' | 'location' | 'system' | 'notification';
  status: 'sent' | 'delivered' | 'read' | 'failed' | 'deleted';
  content: string;
  replyTo?: string;
  mentionedUsers: User[];
  attachments: MessageAttachment[];
  edited: boolean;
  editedAt?: string;
  isImportant: boolean;
  isUrgent: boolean;
  createdAt: string;
  updatedAt: string;
}

export interface MessageAttachment {
  id: string;
  filename: string;
  fileSize: number;
  fileType: string;
  attachmentType: 'image' | 'video' | 'audio' | 'document' | 'archive' | 'other';
  thumbnail?: string;
  downloadCount: number;
  uploadedAt: string;
}

// Payment Types
export interface PaymentMethod {
  id: string;
  user: string;
  methodType: 'credit_card' | 'debit_card' | 'bank_account' | 'digital_wallet' | 'cryptocurrency' | 'mobile_money';
  status: 'active' | 'inactive' | 'pending_verification' | 'verified' | 'suspended' | 'expired';
  maskedNumber: string;
  lastFourDigits: string;
  brand?: string;
  expiryMonth?: number;
  expiryYear?: number;
  isDefault: boolean;
  isVerified: boolean;
  createdAt: string;
  updatedAt: string;
}

export interface Transaction {
  id: string;
  transactionNumber: string;
  transactionType: 'payment' | 'refund' | 'payout' | 'escrow_deposit' | 'escrow_release' | 'fee' | 'bonus' | 'penalty' | 'adjustment';
  status: 'pending' | 'processing' | 'completed' | 'failed' | 'cancelled' | 'disputed' | 'refunded' | 'partially_refunded';
  payer?: User;
  payee?: User;
  currency: string;
  amount: number;
  feeAmount: number;
  netAmount: number;
  description: string;
  processedAt?: string;
  createdAt: string;
  updatedAt: string;
}

// API Response Types
export interface ApiResponse<T> {
  success: boolean;
  data: T;
  message?: string;
  errors?: Record<string, string[]>;
}

export interface PaginatedResponse<T> {
  count: number;
  next?: string;
  previous?: string;
  results: T[];
}

// Form Types
export interface LoginFormData {
  email: string;
  password: string;
  rememberMe?: boolean;
}

export interface RegisterFormData {
  username: string;
  email: string;
  password: string;
  confirmPassword: string;
  firstName: string;
  lastName: string;
  phoneNumber?: string;
  termsAccepted: boolean;
}

export interface ProjectFormData {
  title: string;
  description: string;
  projectType: Project['projectType'];
  country: string;
  city: string;
  address: string;
  budgetCurrency: string;
  totalBudget: number;
  plannedStartDate: string;
  plannedEndDate: string;
  requirements: Record<string, any>;
  deliverables: string[];
}

// Component Props Types
export interface ButtonProps {
  variant?: 'primary' | 'secondary' | 'success' | 'warning' | 'danger';
  size?: 'sm' | 'md' | 'lg';
  disabled?: boolean;
  loading?: boolean;
  children: React.ReactNode;
  onClick?: () => void;
  type?: 'button' | 'submit' | 'reset';
  className?: string;
}

export interface InputProps {
  label?: string;
  error?: string;
  helperText?: string;
  required?: boolean;
  disabled?: boolean;
  className?: string;
}

// Navigation Types
export interface NavItem {
  label: string;
  href: string;
  icon?: React.ComponentType<any>;
  badge?: string | number;
  children?: NavItem[];
}

// Notification Types
export interface Notification {
  id: string;
  type: 'success' | 'error' | 'warning' | 'info';
  title: string;
  message: string;
  duration?: number;
  action?: {
    label: string;
    onClick: () => void;
  };
} 