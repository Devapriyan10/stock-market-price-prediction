import React from 'react';
import { Link } from 'react-router-dom';
import { SignedIn, SignedOut } from '@clerk/clerk-react';
import { TrendingUp, BarChart3, Shield, Zap, ArrowRight } from 'lucide-react';

const Home: React.FC = () => {
  const features = [
    {
      icon: <TrendingUp className="h-8 w-8 text-blue-600" />,
      title: 'AI-Powered Predictions',
      description: 'Advanced machine learning algorithms analyze market trends and predict future stock prices with high accuracy.',
    },
    {
      icon: <BarChart3 className="h-8 w-8 text-indigo-600" />,
      title: 'Interactive Charts',
      description: 'Visualize historical data and future predictions with beautiful, interactive charts and comprehensive analytics.',
    },
    {
      icon: <Shield className="h-8 w-8 text-green-600" />,
      title: 'Secure & Reliable',
      description: 'Enterprise-grade security with Clerk authentication ensures your data is protected and accessible only to you.',
    },
    {
      icon: <Zap className="h-8 w-8 text-yellow-600" />,
      title: 'Real-time Data',
      description: 'Access up-to-date market information and get instant predictions for over 250 top Indian stocks.',
    },
  ];

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="relative overflow-hidden bg-gradient-to-br from-blue-900 via-blue-800 to-indigo-900">
        <div className="absolute inset-0 bg-black/20"></div>
        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-20 pb-24">
          <div className="text-center">
            <h1 className="text-4xl md:text-6xl font-bold text-white mb-6 leading-tight">
              Stock Market Price
              <span className="block text-blue-300">Prediction System</span>
            </h1>
            <p className="text-xl text-blue-100 mb-8 max-w-3xl mx-auto leading-relaxed">
              Harness the power of artificial intelligence to predict stock prices and make informed investment decisions. 
              Get accurate forecasts for top Indian stocks with our advanced ML models.
            </p>
            
            <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
              <SignedOut>
                <Link
                  to="/sign-up"
                  className="inline-flex items-center px-8 py-4 bg-blue-600 text-white text-lg font-semibold rounded-lg hover:bg-blue-700 transition-all duration-200 shadow-lg hover:shadow-xl group"
                >
                  Register Now
                  <ArrowRight className="ml-2 h-5 w-5 group-hover:translate-x-1 transition-transform duration-200" />
                </Link>
                <Link
                  to="/sign-in"
                  className="inline-flex items-center px-8 py-4 bg-white/10 text-white text-lg font-semibold rounded-lg hover:bg-white/20 transition-all duration-200 backdrop-blur-sm border border-white/20"
                >
                  Sign In
                </Link>
              </SignedOut>
              
              <SignedIn>
                <Link
                  to="/dashboard"
                  className="inline-flex items-center px-8 py-4 bg-blue-600 text-white text-lg font-semibold rounded-lg hover:bg-blue-700 transition-all duration-200 shadow-lg hover:shadow-xl group"
                >
                  Go to Dashboard
                  <ArrowRight className="ml-2 h-5 w-5 group-hover:translate-x-1 transition-transform duration-200" />
                </Link>
              </SignedIn>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              Why Choose Our Platform?
            </h2>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              Cutting-edge technology meets user-friendly design to deliver the most accurate stock predictions
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {features.map((feature, index) => (
              <div
                key={index}
                className="p-6 bg-gray-50 rounded-xl hover:bg-white hover:shadow-lg transition-all duration-300 border border-gray-100 group"
              >
                <div className="mb-4 group-hover:scale-110 transition-transform duration-300">
                  {feature.icon}
                </div>
                <h3 className="text-xl font-semibold text-gray-900 mb-3">
                  {feature.title}
                </h3>
                <p className="text-gray-600 leading-relaxed">
                  {feature.description}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-gradient-to-r from-blue-600 to-indigo-600">
        <div className="max-w-4xl mx-auto text-center px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl md:text-4xl font-bold text-white mb-6">
            Ready to Start Predicting?
          </h2>
          <p className="text-xl text-blue-100 mb-8">
            Join thousands of investors who trust our AI-powered predictions to make smarter investment decisions.
          </p>
          
          <SignedOut>
            <Link
              to="/sign-up"
              className="inline-flex items-center px-8 py-4 bg-white text-blue-600 text-lg font-semibold rounded-lg hover:bg-gray-50 transition-all duration-200 shadow-lg hover:shadow-xl group"
            >
              Get Started Free
              <ArrowRight className="ml-2 h-5 w-5 group-hover:translate-x-1 transition-transform duration-200" />
            </Link>
          </SignedOut>
        </div>
      </section>
    </div>
  );
};

export default Home;