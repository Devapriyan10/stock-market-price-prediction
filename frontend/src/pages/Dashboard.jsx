import { useState, useEffect } from 'react';
import api from '../utils/apiClient';
import { authHeader } from '../utils/auth';
import Navbar from '../components/Navbar';
import { Link } from 'react-router-dom';

export default function Dashboard() {
  const [companies, setCompanies] = useState([]);
  const [ticker, setTicker] = useState('');
  const [year, setYear] = useState(new Date().getFullYear() + 1);
  const [prediction, setPrediction] = useState(null);
  const [portfolio, setPortfolio] = useState([]);

  useEffect(() => {
    api.get('/stocks/').then(r => setCompanies(r.data));
    api.get('/portfolio/', { headers: authHeader() }).then(r => setPortfolio(r.data));
  }, []);

  const predict = async () => {
    const r = await api.post('/stocks/predict', { ticker, year });
    setPrediction(r.data);
  };

  const save = async () => {
    const r = await api.post('/portfolio/', { ticker, year }, { headers: authHeader() });
    setPortfolio([...portfolio, r.data]);
  };

  return (
    <>
      <Navbar />
      <div className="p-6">
        <h1 className="text-2xl mb-4">Stock Predictor</h1>
        <div className="flex gap-2 mb-4">
          <select onChange={e => setTicker(e.target.value)} className="border p-2">
            <option value="">Select</option>
            {companies.map(c => <option key={c.ticker} value={c.ticker}>{c.name}</option>)}
          </select>
          <input type="number" value={year} onChange={e => setYear(+e.target.value)} className="border p-2" min={new Date().getFullYear()+1} />
          <button onClick={predict} className="bg-indigo-500 text-white p-2">Predict</button>
        </div>
        {prediction && (
          <div className="mb-4">
            <p>Predicted {prediction.ticker} in {prediction.year}: ₹{prediction.predicted_price}</p>
            <button onClick={save} className="bg-green-500 text-white p-2">Save</button>
          </div>
        )}
        <h2 className="text-xl mt-6">Your Portfolio</h2>
        <ul className="list-disc pl-6">
          {portfolio.map(p => <li key={p.id}>{p.ticker} — {p.year}: ₹{p.predicted_price}</li>)}
        </ul>
        <h2 className="text-xl mt-6">View Charts</h2>
        <ul className="pl-6">
          {companies.slice(0,10).map(c => (
            <li key={c.ticker}>
              <Link to={`/company/${c.ticker}`} className="text-blue-600">{c.name}</Link>
            </li>
          ))}
        </ul>
      </div>
    </>
  );
}
