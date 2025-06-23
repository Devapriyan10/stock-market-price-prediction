import React, { useState } from 'react';
import { useUser } from '@clerk/clerk-react';
import { useQuery } from '@tanstack/react-query';
import { Search, TrendingUp, Calendar, DollarSign } from 'lucide-react';
import PredictionCard from '../components/PredictionCard';
import LoadingSpinner from '../components/LoadingSpinner';
import { fetchCompanies, fetchPrediction } from '../services/api';
import type { Company } from '../types';

const Dashboard: React.FC = () => {
  const { user } = useUser();
  const [selectedCompany, setSelectedCompany] = useState<Company | null>(null);
  const [selectedYear, setSelectedYear] = useState<number>(2026);
  const [searchTerm, setSearchTerm] = useState('');

  const { data: companies, isLoading: companiesLoading, error: companiesError } = useQuery({
    queryKey: ['companies'],
    queryFn: fetchCompanies,
  });

  const { data: prediction, isLoading: predictionLoading, error: predictionError } = useQuery({
    queryKey: ['prediction', selectedCompany?.ticker, selectedYear],
    queryFn: () => selectedCompany ? fetchPrediction(selectedCompany.ticker, selectedYear) : null,
    enabled: !!selectedCompany && !!selectedYear,
  });

  const filteredCompanies = companies?.filter(company =>
    company.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    company.ticker.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const futureYears = Array.from({ length: 10 }, (_, i) => new Date().getFullYear() + 1 + i);

  if (companiesLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <LoadingSpinner />
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Welcome Section */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">
          Welcome back, {user?.firstName || 'User'}! 👋
        </h1>
        <p className="text-gray-600">
          Explore stock predictions and market insights with our AI-powered system
        </p>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
          <div className="flex items-center">
            <div className="p-2 bg-blue-100 rounded-lg">
              <TrendingUp className="h-6 w-6 text-blue-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm text-gray-600">Available Stocks</p>
              <p className="text-2xl font-semibold text-gray-900">{companies?.length || 0}</p>
            </div>
          </div>
        </div>
        
        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
          <div className="flex items-center">
            <div className="p-2 bg-green-100 rounded-lg">
              <Calendar className="h-6 w-6 text-green-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm text-gray-600">Prediction Years</p>
              <p className="text-2xl font-semibold text-gray-900">2025-2034</p>
            </div>
          </div>
        </div>
        
        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
          <div className="flex items-center">
            <div className="p-2 bg-purple-100 rounded-lg">
              <DollarSign className="h-6 w-6 text-purple-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm text-gray-600">Data Range</p>
              <p className="text-2xl font-semibold text-gray-900">5 Years</p>
            </div>
          </div>
        </div>
      </div>

      {/* Stock Selection */}
      <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 mb-8">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">Select a Stock</h2>
        
        <div className="relative mb-4">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
          <input
            type="text"
            placeholder="Search stocks by name or ticker..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
        </div>

        {companiesError && (
          <div className="text-red-600 mb-4">
            Error loading companies. Please try again later.
          </div>
        )}

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 max-h-60 overflow-y-auto">
          {filteredCompanies?.map((company) => (
            <button
              key={company.ticker}
              onClick={() => setSelectedCompany(company)}
              className={`p-4 text-left rounded-lg border transition-all duration-200 ${
                selectedCompany?.ticker === company.ticker
                  ? 'border-blue-500 bg-blue-50 ring-2 ring-blue-200'
                  : 'border-gray-200 hover:border-gray-300 hover:bg-gray-50'
              }`}
            >
              <div className="font-semibold text-gray-900">{company.ticker}</div>
              <div className="text-sm text-gray-600 truncate">{company.name}</div>
            </button>
          ))}
        </div>
      </div>

      {/* Prediction Section */}
      {selectedCompany && (
        <div className="lg:max-w-lg mx-auto">
          {/* Year Selection */}
          <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 mb-6">
            <h4 className="text-lg font-semibold text-gray-900 mb-4">Select Prediction Year</h4>
            <select
              value={selectedYear}
              onChange={(e) => setSelectedYear(Number(e.target.value))}
              className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              {futureYears.map((year) => (
                <option key={year} value={year}>
                  {year}
                </option>
              ))}
            </select>
          </div>

          {/* Prediction Result */}
          <PredictionCard
            company={selectedCompany}
            year={selectedYear}
            prediction={prediction}
            isLoading={predictionLoading}
            error={predictionError}
          />
        </div>
      )}

      {!selectedCompany && (
        <div className="bg-white p-12 rounded-xl shadow-sm border border-gray-100 text-center">
          <TrendingUp className="h-16 w-16 text-gray-400 mx-auto mb-4" />
          <h3 className="text-xl font-semibold text-gray-900 mb-2">
            Select a Stock to Get Started
          </h3>
          <p className="text-gray-600">
            Choose from over 250 top Indian stocks to view AI-powered price predictions.
          </p>
        </div>
      )}
    </div>
  );
};

export default Dashboard;
