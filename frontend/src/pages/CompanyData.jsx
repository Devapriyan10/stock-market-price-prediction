import { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import api from '../utils/apiClient';
import Chart from '../components/Chart';

export default function CompanyData() {
  const { ticker } = useParams();
  const [history, setHistory] = useState([]);

  useEffect(() => {
    // fetch 5-year history via yfinance proxy endpoint (not implemented)
    api.get(`/stocks/history/${ticker}`).then(r => setHistory(r.data));
  }, [ticker]);

  return (
    <div className="p-6">
      <h1 className="text-2xl mb-4">{ticker} 5-Year History</h1>
      <Chart data={history} />
    </div>
  );
}
