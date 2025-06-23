import React from 'react';
import { TrendingUp, TrendingDown, Calendar, AlertCircle } from 'lucide-react';
import LoadingSpinner from './LoadingSpinner';
import type { Company, Prediction } from '../types';

interface PredictionCardProps {
  company: Company;
  year: number;
  prediction: Prediction | null | undefined;
  isLoading: boolean;
  error: Error | null;
}

const PredictionCard: React.FC<PredictionCardProps> = ({
  company,
  year,
  prediction,
  isLoading,
  error
}) => {
  const formatCurrency = (amount?: number): string => {
    if (typeof amount !== 'number' || isNaN(amount)) {
      return '—'; // Placeholder for undefined or invalid numbers
    }
    return amount.toLocaleString('en-IN', {
      style: 'currency',
      currency: 'INR',
      minimumFractionDigits: 2,
      maximumFractionDigits: 2
    });
  };

  const getPriceChange = () => {
    if (!prediction || typeof prediction.currentPrice !== 'number' || typeof prediction.predictedPrice !== 'number') return null;

    const change = prediction.predictedPrice - prediction.currentPrice;
    const changePercent = (change / prediction.currentPrice) * 100;

    return {
      amount: change,
      percent: changePercent,
      isPositive: change > 0
    };
  };

  const priceChange = getPriceChange();

  return (
    <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
      <div className="flex items-center mb-4">
        <Calendar className="h-5 w-5 text-blue-600 mr-2" />
        <h4 className="text-lg font-semibold text-gray-900">
          {year} Prediction
        </h4>
      </div>

      {isLoading ? (
        <div className="flex items-center justify-center py-8">
          <LoadingSpinner size="sm" />
        </div>
      ) : error ? (
        <div className="text-center py-8">
          <AlertCircle className="h-12 w-12 text-red-400 mx-auto mb-3" />
          <p className="text-red-600 text-sm">
            Unable to load prediction. Please try again.
          </p>
        </div>
      ) : prediction ? (
        <div className="space-y-4">
          {/* Current Price */}
          {typeof prediction.currentPrice === 'number' && (
            <div className="bg-gray-50 p-4 rounded-lg">
              <p className="text-sm text-gray-600 mb-1">Current Price</p>
              <p className="text-xl font-semibold text-gray-900">
                {formatCurrency(prediction.currentPrice)}
              </p>
            </div>
          )}

          {/* Predicted Price */}
          {typeof prediction.predictedPrice === 'number' && (
            <div className="bg-blue-50 p-4 rounded-lg">
              <p className="text-sm text-blue-600 mb-1">
                Predicted Price ({year})
              </p>
              <p className="text-2xl font-bold text-blue-900">
                {formatCurrency(prediction.predictedPrice)}
              </p>
            </div>
          )}

          {/* Price Change */}
          {priceChange && (
            <div className={`p-4 rounded-lg ${
              priceChange.isPositive ? 'bg-green-50' : 'bg-red-50'
            }`}>
              <div className="flex items-center mb-2">
                {priceChange.isPositive ? (
                  <TrendingUp className="h-5 w-5 text-green-600 mr-2" />
                ) : (
                  <TrendingDown className="h-5 w-5 text-red-600 mr-2" />
                )}
                <p className={`text-sm font-medium ${
                  priceChange.isPositive ? 'text-green-600' : 'text-red-600'
                }`}>
                  Expected Change
                </p>
              </div>
              <p className={`text-lg font-semibold ${
                priceChange.isPositive ? 'text-green-800' : 'text-red-800'
              }`}>
                {priceChange.isPositive ? '+' : ''}
                {formatCurrency(priceChange.amount)}
              </p>
              <p className={`text-sm ${
                priceChange.isPositive ? 'text-green-600' : 'text-red-600'
              }`}>
                ({priceChange.isPositive ? '+' : ''}
                {priceChange.percent.toFixed(2)}%)
              </p>
            </div>
          )}

          {/* Confidence Score */}
          <div className="bg-yellow-50 p-4 rounded-lg">
            <p className="text-sm text-yellow-700 mb-1">Confidence Score</p>
            <div className="flex items-center">
              <div className="flex-1 bg-yellow-200 rounded-full h-2 mr-3">
                <div 
                  className="bg-yellow-600 h-2 rounded-full transition-all duration-500"
                  style={{ width: `${prediction.confidence ?? 0}%` }}
                ></div>
              </div>
              <span className="text-sm font-semibold text-yellow-800">
                {prediction.confidence ?? '—'}%
              </span>
            </div>
          </div>

          {/* Disclaimer */}
          <div className="text-xs text-gray-500 bg-gray-50 p-3 rounded-lg">
            <p className="flex items-start">
              <AlertCircle className="h-3 w-3 mr-1 mt-0.5 flex-shrink-0" />
              This prediction is based on historical data and AI models. 
              Past performance does not guarantee future results. 
              Please consult with financial advisors before making investment decisions.
            </p>
          </div>
        </div>
      ) : (
        <div className="text-center py-8 text-gray-500">
          <p>Select a year to see predictions</p>
        </div>
      )}
    </div>
  );
};

export default PredictionCard;
