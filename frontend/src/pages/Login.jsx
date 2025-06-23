import { useState } from 'react';
import api from '../utils/apiClient';
import { setToken } from '../utils/auth';
import { useNavigate } from 'react-router-dom';
import Form from '../components/Form';

export default function Login() {
  const [email, setEmail] = useState('');
  const [pwd, setPwd] = useState('');
  const nav = useNavigate();

  const onSubmit = async (e) => {
    e.preventDefault();
    try {
      const formData = new URLSearchParams();
      formData.append('username', email);
      formData.append('password', pwd);

      const res = await api.post('/users/login', formData, {
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      });

      setToken(res.data.access_token);
      nav('/');
    } catch (err) {
      console.error('❌ Login error:', err.response || err);
      alert(err.response?.data?.detail || 'Login failed');
    }
  };

  return (
    <Form onSubmit={onSubmit}>
      <h2 className="text-xl mb-4">Login</h2>
      <input
        type="email"
        placeholder="Email"
        onChange={e => setEmail(e.target.value)}
        className="w-full mb-2 p-2 border"
        required
      />
      <input
        type="password"
        placeholder="Password"
        onChange={e => setPwd(e.target.value)}
        className="w-full mb-4 p-2 border"
        required
      />
      <button type="submit" className="w-full bg-blue-500 text-white p-2">
        Sign In
      </button>
    </Form>
  );
}
