import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { SignedIn, SignedOut, UserButton, useUser } from '@clerk/clerk-react';
import { TrendingUp, LogIn, UserPlus } from 'lucide-react';

const Header: React.FC = () => {
  const navigate = useNavigate();
  const { user } = useUser();

  return (
    <header className="fixed top-0 left-0 right-0 z-50 bg-white/80 backdrop-blur-md border-b border-gray-200 shadow-sm">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <Link to="/" className="flex items-center space-x-2 group">
            <div className="p-2 bg-gradient-to-r from-blue-600 to-indigo-600 rounded-lg group-hover:from-blue-700 group-hover:to-indigo-700 transition-all duration-200">
              <TrendingUp className="h-6 w-6 text-white" />
            </div>
            <span className="text-xl font-bold text-gray-900 group-hover:text-blue-600 transition-colors duration-200">
              StockPredict
            </span>
          </Link>

          {/* Auth Navigation */}
          <nav className="flex items-center space-x-4">
            {/* When user is not signed in */}
            <SignedOut>
              <button
                onClick={() => navigate('/sign-in')}
                className="flex items-center space-x-2 px-4 py-2 text-gray-600 hover:text-blue-600 transition-colors duration-200"
              >
                <LogIn className="h-4 w-4" />
                <span>Sign In</span>
              </button>
              <button
                onClick={() => navigate('/sign-up')}
                className="flex items-center space-x-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors duration-200"
              >
                <UserPlus className="h-4 w-4" />
                <span>Register</span>
              </button>
            </SignedOut>

            {/* When user is signed in */}
            <SignedIn>
              <Link
                to="/dashboard"
                className="px-4 py-2 text-gray-600 hover:text-blue-600 transition-colors duration-200"
              >
                Dashboard
              </Link>
              <div className="flex items-center space-x-3">
                <span className="text-sm text-gray-600">
                  Welcome, {user?.firstName || 'User'}!
                </span>
                <UserButton afterSignOutUrl="/" />
              </div>
            </SignedIn>
          </nav>
        </div>
      </div>
    </header>
  );
};

export default Header;
