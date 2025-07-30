import { Link } from 'react-router-dom';
import { useState } from 'react';
import {
  CheckIcon,
  ShieldCheckIcon,
  GlobeAltIcon,
  UserGroupIcon,
  StarIcon,
  ArrowRightIcon,
  EyeIcon,
  LinkIcon,
  ClockIcon,
  XMarkIcon,
  ChevronLeftIcon,
  ChevronRightIcon,
} from '@heroicons/react/24/outline';

// Add custom styles for animations
const modalStyles = `
  @keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
  }
  
  @keyframes slideUp {
    from { 
      opacity: 0;
      transform: translateY(60px) scale(0.95); 
    }
    to { 
      opacity: 1;
      transform: translateY(0) scale(1); 
    }
  }
  
  .animate-fadeIn {
    animation: fadeIn 0.3s ease-out;
  }
  
  .animate-slideUp {
    animation: slideUp 0.4s ease-out;
  }
`;

const LandingPage = () => {
  const [showStoriesModal, setShowStoriesModal] = useState(false);
  const [currentStoryIndex, setCurrentStoryIndex] = useState(0);

  const realStories = [
    {
      title: "The Property Tax Scam",
      problem: "A diaspora member needed to pay overdue property taxes back home.",
      what_happened: "His trusted lawyer told him the taxes would cost $1,000. Something felt off, so he decided to get a second opinion before sending the money.",
      reality: "When we investigated, we discovered the actual property taxes were only $500. The lawyer was trying to double the amount and keep the extra $500.",
      outcome: "He saved $500 by using our verified tax professional instead. Now he always checks with us before making any payments back home."
    },
    {
      title: "The Birth Certificate Markup",
      problem: "A couple wanted to get birth certificates for their elderly parents back in Africa.",
      what_happened: "Family members told them it would cost $1,000 per certificate ($2,000 total) and were asking for the money to be sent.",
      reality: "When we investigated, the actual cost for each birth certificate was only $250. The family members were trying to keep $1,500 of the $2,000.",
      outcome: "We informed the couple about the real price before they sent any money. They decided not to proceed through their family members after learning about the massive markup."
    },
    {
      title: "The Missing House",
      problem: "A woman sent money to her brother for years to build her dream retirement home.",
      what_happened: "She regularly sent construction funds and received photos of progress. After several years, she was excited to finally visit her new home.",
      reality: "When she arrived, she found only an empty plot of land. Her brother had used all the construction money for his own needs and sent fake progress photos.",
      outcome: "She lost everything - years of savings gone. This is exactly why diaspora need independent verification before sending money to family members back home."
    }
  ];

  const nextStory = () => {
    setCurrentStoryIndex((prev) => (prev + 1) % realStories.length);
  };

  const prevStory = () => {
    setCurrentStoryIndex((prev) => (prev - 1 + realStories.length) % realStories.length);
  };

  const features = [
    {
      icon: ShieldCheckIcon,
      title: 'Verified Inspectors',
      description: 'All inspectors are thoroughly vetted and certified professionals with proven track records.',
    },
    {
      icon: GlobeAltIcon,
      title: 'Pan-African Network',
      description: 'Access trusted local inspectors across major African cities and regions.',
    },
    {
      icon: UserGroupIcon,
      title: 'Diaspora-Focused',
      description: 'Specifically designed for Africans abroad investing in their home countries.',
    },
  ];

  const testimonials = [
    {
      name: 'Amina Johnson',
      location: 'London, UK → Lagos, Nigeria',
      content: 'Pofara gave me peace of mind when buying property in Lagos. The inspector was professional and detailed.',
      rating: 5,
    },
    {
      name: 'Kwame Asante',
      location: 'Toronto, Canada → Accra, Ghana',
      content: 'Finally, a service that understands the unique challenges of investing from abroad. Excellent work!',
      rating: 5,
    },
    {
      name: 'Fatou Diallo',
      location: 'Paris, France → Dakar, Senegal',
      content: 'The inspection report was thorough and helped me negotiate a better price. Highly recommended.',
      rating: 5,
    },
  ];

  const steps = [
    {
      step: '01',
      title: 'Create Your Project',
      description: 'Tell us about your property or investment that needs inspection.',
    },
    {
      step: '02',
      title: 'Match with Inspector',
      description: 'We connect you with verified local inspectors in your target area.',
    },
    {
      step: '03',
      title: 'Get Your Report',
      description: 'Receive detailed inspection reports with photos and recommendations.',
    },
  ];

  const aboutCards = [
    {
      icon: EyeIcon,
      title: 'Independent Verification',
      description: 'Get accurate market pricing and quality assessments from professionals who have no personal interest in inflating costs or cutting corners.',
      color: 'from-blue-500 to-blue-600',
    },
    {
      icon: LinkIcon,
      title: 'Professional Standards',
      description: 'Work with qualified professionals who maintain their reputation through consistent, reliable service and transparent reporting.',
      color: 'from-green-500 to-green-600',
    },
    {
      icon: ShieldCheckIcon,
      title: 'Accountability & Trust',
      description: 'Every professional is vetted and accountable for their work. You get detailed reports and verification you can rely on.',
      color: 'from-purple-500 to-purple-600',
    },
  ];

  return (
    <div className="min-h-screen bg-white">
      {/* Inject custom styles for modal animations */}
      <style>{modalStyles}</style>
      {/* Navigation */}
      <nav className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center">
              <h1 className="text-2xl font-bold text-black">Pofara</h1>
            </div>
            <div className="flex items-center space-x-4">
              <Link
                to="/login"
                className="text-gray-700 hover:text-black font-medium transition-colors duration-200"
              >
                Sign in
              </Link>
              <Link
                to="/register"
                className="bg-black text-white px-4 py-2 rounded-lg font-medium hover:bg-gray-800 transition-colors duration-200"
              >
                Get started
              </Link>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="pt-20 pb-16 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto text-center">
          <h1 className="text-5xl md:text-6xl font-bold text-black mb-6 leading-tight">
            When you can't verify it yourself
            <br />
            <span className="text-gray-600">important things go wrong</span>
          </h1>
          <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto leading-relaxed">
            Distance makes it impossible to verify costs, inspect progress, or ensure quality when handling 
            important matters back home. We provide independent verification you can trust.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link
              to="/register"
              className="bg-black text-white px-8 py-4 rounded-lg text-lg font-medium hover:bg-gray-800 transition-colors duration-200 inline-flex items-center justify-center"
            >
              Get verified help
              <ArrowRightIcon className="ml-2 h-5 w-5" />
            </Link>
            <Link
              to="/login"
              className="bg-white text-black px-8 py-4 rounded-lg text-lg font-medium border border-gray-300 hover:bg-gray-50 transition-colors duration-200"
            >
              Sign in
            </Link>
          </div>
        </div>
      </section>

      {/* About Us Section */}
      <section className="py-20 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-black mb-4">
              Who we are and what we do
            </h2>
            <p className="text-xl text-gray-600 max-w-4xl mx-auto mb-8">
              Every African living abroad faces this challenge: Distance makes it impossible to verify costs, inspect progress, or ensure quality when handling important matters back home. Without independent verification, you can't be certain if you're getting accurate information, fair pricing, or proper execution.
            </p>
            <p className="text-lg text-gray-700 max-w-3xl mx-auto">
              We connect you with verified professionals who provide transparent verification services. No conflicts of interest. No uncertainty. Just reliable, independent confirmation of costs, quality, and progress.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-16">
            {aboutCards.map((card, index) => (
              <div 
                key={index}
                className="group relative bg-white rounded-2xl p-8 shadow-lg hover:shadow-xl transition-all duration-300 hover:-translate-y-2"
              >
                <div className={`absolute inset-0 bg-gradient-to-br ${card.color} opacity-0 group-hover:opacity-5 rounded-2xl transition-opacity duration-300`}></div>
                
                <div className={`inline-flex items-center justify-center w-16 h-16 bg-gradient-to-br ${card.color} rounded-2xl mb-6 group-hover:scale-110 transition-transform duration-300`}>
                  <card.icon className="w-8 h-8 text-white" />
                </div>
                
                <h3 className="text-xl font-semibold text-black mb-4 group-hover:text-gray-800 transition-colors duration-300">
                  {card.title}
                </h3>
                <p className="text-gray-600 leading-relaxed">
                  {card.description}
                </p>
              </div>
            ))}
          </div>



          {/* Problem/Solution Highlight */}
          <div className="mt-16 bg-gradient-to-r from-black to-gray-800 rounded-2xl p-8 text-white">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 items-center">
              <div>
                <h3 className="text-2xl font-bold mb-4">The Verification Challenge</h3>
                <p className="text-gray-300 mb-6">
                  Distance creates a fundamental verification problem. You can't personally inspect quality, verify market prices, or monitor progress in real-time. Without independent verification systems, you must rely entirely on others' word, making it impossible to distinguish between accurate and inaccurate information. This uncertainty affects decisions and outcomes.
                </p>
                <div className="flex items-center text-red-400">
                  <ClockIcon className="w-5 h-5 mr-2" />
                  <span className="text-sm">This verification gap limits confident diaspora investment</span>
                </div>
              </div>
              <div>
                <h3 className="text-2xl font-bold mb-4 text-green-400">Independent Verification Network</h3>
                <p className="text-gray-300 mb-6">
                  We built a network of verified professionals who provide independent verification services. Their reputation depends on accuracy, transparency, and reliability. We monitor their work, verify their assessments, and ensure quality standards. This creates a system where verification is done by qualified professionals with no conflicts of interest.
                </p>
                <div className="flex items-center text-green-400">
                  <CheckIcon className="w-5 h-5 mr-2" />
                  <span className="text-sm">Finally, a system designed to provide reliable verification you can trust</span>
                </div>
              </div>
            </div>
            
            {/* Real Stories Button - Uber Style */}
            <div className="mt-8 text-center">
              <button
                onClick={() => setShowStoriesModal(true)}
                className="bg-black text-white px-8 py-4 rounded-lg text-lg font-medium hover:bg-gray-800 transition-colors duration-200 inline-flex items-center"
              >
                <EyeIcon className="w-6 h-6 mr-3" />
                Real Stories
                <ArrowRightIcon className="w-5 h-5 ml-2" />
              </button>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-black mb-4">
              Why choose Pofara?
            </h2>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              We solve the biggest challenge facing diaspora: lack of independent verification when distance prevents you from checking things yourself.
            </p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {features.map((feature, index) => (
              <div key={index} className="bg-gray-50 p-8 rounded-2xl border border-gray-200 hover:shadow-lg transition-shadow duration-200">
                <feature.icon className="h-12 w-12 text-black mb-4" />
                <h3 className="text-xl font-semibold text-black mb-3">{feature.title}</h3>
                <p className="text-gray-600 leading-relaxed">{feature.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* How it Works - Uber Style Clean Design */}
      <section className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-20">
            <h2 className="text-4xl md:text-5xl font-bold text-black mb-6">
              How it works
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto leading-relaxed">
              Stop trusting family and friends with your money. Get professional verification in three simple steps.
            </p>
          </div>

          {/* Clean Steps - Uber Style */}
          <div className="relative">
            {/* Simple Connection Line */}
            <div className="hidden md:block absolute top-1/2 left-0 right-0 h-px bg-gray-200 transform -translate-y-1/2 z-0"></div>
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-12 relative z-10">
            {steps.map((step, index) => (
                <div 
                  key={index} 
                  className="group relative text-center"
                >
                  {/* Step Number - Clean Black Circle */}
                  <div className="relative mb-8">
                    <div className="inline-flex items-center justify-center w-16 h-16 bg-black text-white rounded-full text-xl font-bold mb-6 group-hover:bg-gray-800 transition-colors duration-200">
                  {step.step}
                    </div>
                    
                    {/* Simple Arrow for Desktop */}
                    {index < steps.length - 1 && (
                      <div className="hidden md:block absolute -right-20 top-6 text-gray-300">
                        <ArrowRightIcon className="w-6 h-6" />
                      </div>
                    )}
                  </div>

                  {/* Content */}
                  <div>
                    <h3 className="text-2xl font-bold text-black mb-4">
                      {step.title}
                    </h3>
                    <p className="text-gray-600 leading-relaxed text-lg">
                      {step.description}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Clean Comparison Section - Uber Style */}
          <div className="mt-20 bg-gray-50 rounded-lg p-8 border border-gray-200">
            <div className="text-center mb-8">
              <h3 className="text-2xl font-bold text-black mb-4">See the Difference</h3>
              <p className="text-gray-600">Compare the old way vs. the Pofara way</p>
            </div>
            
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
              {/* Old Way - Problem */}
              <div className="bg-white rounded-lg p-6 border border-gray-200">
                <div className="mb-4">
                  <h4 className="text-xl font-bold text-black mb-2">Personal Connections</h4>
                  <div className="text-sm text-gray-500 font-medium">❌ WITHOUT VERIFICATION</div>
                </div>
                <ul className="space-y-3 text-gray-700">
                  <li className="flex items-center">
                    <div className="w-1.5 h-1.5 bg-black rounded-full mr-3"></div>
                    "Trust me, this is the cost"
                  </li>
                  <li className="flex items-center">
                    <div className="w-1.5 h-1.5 bg-black rounded-full mr-3"></div>
                    No independent way to verify pricing
                  </li>
                  <li className="flex items-center">
                    <div className="w-1.5 h-1.5 bg-black rounded-full mr-3"></div>
                    No progress verification or quality checks
                  </li>
                  <li className="flex items-center">
                    <div className="w-1.5 h-1.5 bg-black rounded-full mr-3"></div>
                    Discover issues too late to fix them
                  </li>
                </ul>
                <div className="mt-4 text-black font-semibold">Result: Uncertainty and potential losses</div>
              </div>

              {/* New Way - Solution */}
              <div className="bg-black text-white rounded-lg p-6">
                <div className="mb-4">
                  <h4 className="text-xl font-bold text-white mb-2">Verified Professionals</h4>
                  <div className="text-sm text-gray-300 font-medium">✅ POFARA WAY</div>
                </div>
                <ul className="space-y-3 text-gray-200">
                  <li className="flex items-center">
                    <div className="w-1.5 h-1.5 bg-white rounded-full mr-3"></div>
                    "Here's the verified cost with documentation"
                  </li>
                  <li className="flex items-center">
                    <div className="w-1.5 h-1.5 bg-white rounded-full mr-3"></div>
                    Independent verification with proof
                  </li>
                  <li className="flex items-center">
                    <div className="w-1.5 h-1.5 bg-white rounded-full mr-3"></div>
                    Quality checks and progress monitoring
                  </li>
                  <li className="flex items-center">
                    <div className="w-1.5 h-1.5 bg-white rounded-full mr-3"></div>
                    Real-time updates and transparent reporting
                  </li>
                </ul>
                <div className="mt-4 text-white font-semibold">Result: Confidence and peace of mind</div>
              </div>
            </div>
          </div>

          {/* Call to Action - Uber Style */}
          <div className="text-center mt-16">
            <Link
              to="/register"
              className="inline-flex items-center bg-black text-white px-10 py-4 rounded-lg text-xl font-medium hover:bg-gray-800 transition-colors duration-200"
            >
              Get Verified Help Now
              <ArrowRightIcon className="w-6 h-6 ml-3" />
            </Link>
            <p className="text-gray-500 mt-4 text-sm">No upfront costs • Pay only when satisfied</p>
          </div>
        </div>
      </section>

      {/* Testimonials */}
      <section className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-black mb-4">
              Trusted by diaspora who value independent verification
            </h2>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              See how they gained confidence by using verified professionals for important matters.
            </p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {testimonials.map((testimonial, index) => (
              <div key={index} className="bg-gray-50 p-8 rounded-2xl border border-gray-200">
                <div className="flex items-center mb-4">
                  {[...Array(testimonial.rating)].map((_, i) => (
                    <StarIcon key={i} className="h-5 w-5 text-yellow-400 fill-current" />
                  ))}
                </div>
                <p className="text-gray-600 mb-6 leading-relaxed">"{testimonial.content}"</p>
                <div>
                  <p className="font-semibold text-black">{testimonial.name}</p>
                  <p className="text-sm text-gray-500">{testimonial.location}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-gray-50">
        <div className="max-w-4xl mx-auto text-center px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl md:text-4xl font-bold text-black mb-6">
            Ready to handle important matters with confidence?
          </h2>
          <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
            Join thousands of diaspora who now use independent verification 
            to ensure their important projects are handled properly.
          </p>
          <Link
            to="/register"
            className="bg-black text-white px-8 py-4 rounded-lg text-lg font-medium hover:bg-gray-800 transition-colors duration-200 inline-flex items-center"
          >
                         Get verified help today
            <ArrowRightIcon className="ml-2 h-5 w-5" />
          </Link>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-black text-white py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            <div>
              <h3 className="text-xl font-bold mb-4">Pofara</h3>
              <p className="text-gray-400">
                Connecting diaspora investors with trusted local inspectors across Africa.
              </p>
            </div>
            <div>
              <h4 className="font-semibold mb-4">Services</h4>
              <ul className="space-y-2 text-gray-400">
                <li><a href="#" className="hover:text-white transition-colors">Property Inspection</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Due Diligence</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Investment Verification</a></li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold mb-4">Company</h4>
              <ul className="space-y-2 text-gray-400">
                <li><a href="#" className="hover:text-white transition-colors">About Us</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Contact</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Careers</a></li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold mb-4">Legal</h4>
              <ul className="space-y-2 text-gray-400">
                <li><Link to="/privacy" className="hover:text-white transition-colors">Privacy Policy</Link></li>
                <li><Link to="/terms" className="hover:text-white transition-colors">Terms of Service</Link></li>
              </ul>
            </div>
          </div>
          <div className="border-t border-gray-800 mt-8 pt-8 text-center text-gray-400">
            <p>&copy; 2024 Pofara. All rights reserved.</p>
          </div>
        </div>
      </footer>

      {/* Real Stories Modal - Modern Design */}
      {showStoriesModal && (
        <div className="fixed inset-0 bg-black/80 backdrop-blur-sm flex items-center justify-center z-50 p-4 animate-fadeIn">
          <div className="bg-white rounded-3xl max-w-5xl w-full max-h-[90vh] overflow-hidden relative shadow-2xl transform animate-slideUp">
            {/* Clean Header - Uber Style */}
            <div className="bg-black px-8 py-6 text-white">
              <div className="flex items-center justify-between">
                <div>
                  <h3 className="text-3xl font-bold mb-2">Real Stories</h3>
                  <p className="text-gray-300 text-sm">Authentic experiences from the African diaspora</p>
                </div>
                <button
                  onClick={() => setShowStoriesModal(false)}
                  className="p-3 hover:bg-gray-800 rounded-lg transition-colors duration-200"
                >
                  <XMarkIcon className="w-6 h-6 text-white" />
                </button>
              </div>
            </div>

            {/* Story Content - Modern Card Design */}
            <div className="p-8 overflow-y-auto max-h-[calc(90vh-180px)]">
              {realStories[currentStoryIndex] && (
                <div className="relative">
                  {/* Story Card */}
                  <div className="bg-gradient-to-br from-gray-50 to-white rounded-3xl p-8 shadow-lg border border-gray-100 mb-8">
                    <div className="flex items-start gap-8 mb-8">
                      <div className="flex-1">
                        <div className="inline-flex items-center px-4 py-2 bg-gray-100 text-gray-700 rounded-lg text-sm font-medium mb-4">
                          Story {currentStoryIndex + 1} of {realStories.length}
                        </div>
                        <h4 className="text-4xl font-bold text-gray-900 mb-3 leading-tight">{realStories[currentStoryIndex].title}</h4>
                      </div>
                      {currentStoryIndex === 0 && (
                        <div className="flex-shrink-0">
                          <div className="w-32 h-32 rounded-2xl overflow-hidden shadow-lg border-4 border-white">
                            {/* AI Generated Style Image Placeholder */}
                            <div className="w-full h-full bg-gradient-to-br from-amber-100 via-orange-50 to-yellow-100 flex items-center justify-center relative">
                              <div className="absolute inset-0 bg-gradient-to-br from-slate-800/10 to-slate-900/20"></div>
                              <div className="relative">
                                {/* Stylized representation of an elderly man thinking */}
                                <div className="text-6xl filter drop-shadow-sm">👨🏾‍🦳</div>
                                <div className="absolute -top-2 -right-1 text-2xl animate-pulse">💭</div>
                              </div>
                            </div>
                          </div>
                          <p className="text-xs text-gray-600 text-center mt-3 font-medium bg-green-50 px-3 py-1 rounded-full">
                            Smart decision saved $500
                          </p>
                        </div>
                      )}
                    </div>
                    
                    <div className="grid gap-6">
                      {/* The Situation */}
                      <div className="bg-white rounded-2xl p-6 border border-gray-200 shadow-sm">
                        <div className="flex items-center mb-3">
                          <div className="w-2 h-2 bg-blue-500 rounded-full mr-3"></div>
                          <h5 className="text-xl font-bold text-gray-900">The Situation</h5>
                        </div>
                        <p className="text-gray-700 leading-relaxed text-lg">{realStories[currentStoryIndex].problem}</p>
                      </div>
                      
                      {/* What They Were Told */}
                      <div className="bg-white rounded-2xl p-6 border border-gray-200 shadow-sm">
                        <div className="flex items-center mb-3">
                          <div className="w-2 h-2 bg-orange-500 rounded-full mr-3"></div>
                          <h5 className="text-xl font-bold text-gray-900">What They Were Told</h5>
                        </div>
                        <p className="text-gray-700 leading-relaxed text-lg">{realStories[currentStoryIndex].what_happened}</p>
                      </div>
                      
                      {/* The Reality - Warning Style */}
                      <div className="bg-gradient-to-r from-red-50 to-pink-50 rounded-2xl p-6 border-l-4 border-red-500 shadow-sm">
                        <div className="flex items-center mb-3">
                          <div className="w-8 h-8 bg-red-500 rounded-full flex items-center justify-center mr-3">
                            <span className="text-white text-sm font-bold">!</span>
                          </div>
                          <h5 className="text-xl font-bold text-red-900">The Shocking Reality</h5>
                        </div>
                        <p className="text-red-800 leading-relaxed text-lg font-medium">{realStories[currentStoryIndex].reality}</p>
                      </div>
                      
                                             {/* Outcome - Success Style or Warning Style */}
                       <div className={`rounded-2xl p-6 border-l-4 shadow-sm ${
                         currentStoryIndex === 2 
                           ? 'bg-gradient-to-r from-orange-50 to-amber-50 border-orange-500' 
                           : 'bg-gradient-to-r from-green-50 to-emerald-50 border-green-500'
                       }`}>
                         <div className="flex items-center mb-3">
                           <div className={`w-8 h-8 rounded-full flex items-center justify-center mr-3 ${
                             currentStoryIndex === 2 
                               ? 'bg-orange-500' 
                               : 'bg-green-500'
                           }`}>
                             {currentStoryIndex === 2 ? (
                               <span className="text-white text-sm font-bold">!</span>
                             ) : (
                               <CheckIcon className="w-5 h-5 text-white" />
                             )}
                           </div>
                           <h5 className={`text-xl font-bold ${
                             currentStoryIndex === 2 
                               ? 'text-orange-900' 
                               : 'text-green-900'
                           }`}>
                             {currentStoryIndex === 2 ? 'The Tragic Outcome' : 'How Pofara Saved the Day'}
                           </h5>
                         </div>
                         <p className={`leading-relaxed text-lg font-medium ${
                           currentStoryIndex === 2 
                             ? 'text-orange-800' 
                             : 'text-green-800'
                         }`}>
                           {realStories[currentStoryIndex].outcome}
                         </p>
                       </div>
                    </div>
                  </div>

                  {/* Modern Navigation */}
                  <div className="flex items-center justify-between bg-gray-50 rounded-2xl p-6">
                    <button
                      onClick={prevStory}
                      className="flex items-center px-6 py-3 bg-white hover:bg-gray-100 rounded-xl transition-all duration-200 shadow-sm border border-gray-200 group"
                    >
                      <ChevronLeftIcon className="w-5 h-5 mr-2 group-hover:-translate-x-1 transition-transform" />
                      <span className="font-medium">Previous</span>
                    </button>
                    
                    <div className="flex space-x-3">
                      {realStories.map((_, index) => (
                        <button
                          key={index}
                          onClick={() => setCurrentStoryIndex(index)}
                          className={`w-4 h-4 rounded-full transition-all duration-200 ${
                            index === currentStoryIndex 
                              ? 'bg-black' 
                              : 'bg-gray-300 hover:bg-gray-400'
                          }`}
                        />
                      ))}
                    </div>
                    
                    <button
                      onClick={nextStory}
                      className="flex items-center px-6 py-3 bg-white hover:bg-gray-100 rounded-xl transition-all duration-200 shadow-sm border border-gray-200 group"
                    >
                      <span className="font-medium">Next</span>
                      <ChevronRightIcon className="w-5 h-5 ml-2 group-hover:translate-x-1 transition-transform" />
                    </button>
                  </div>
                </div>
              )}

              {/* Clean Call to Action - Uber Style */}
              <div className="mt-8 bg-black rounded-lg p-8 text-white">
                <div className="text-center">
                  <h4 className="text-3xl font-bold mb-4">Don't Be the Next Victim</h4>
                  <p className="text-gray-300 mb-8 text-lg max-w-2xl mx-auto">
                    Join thousands of smart diaspora investors who protect their money with verified professionals.
                  </p>
                  <Link
                    to="/register"
                    onClick={() => setShowStoriesModal(false)}
                    className="inline-flex items-center bg-white text-black px-8 py-4 rounded-lg text-lg font-medium hover:bg-gray-100 transition-colors duration-200"
                  >
                    Protect Your Investment Now
                    <ArrowRightIcon className="w-6 h-6 ml-3" />
                  </Link>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default LandingPage; 