import { useState } from 'react';
import api from '../utils/apiClient';
import { setToken } from '../utils/auth';
import { useNavigate } from 'react-router-dom';
import Form from '../components/Form';

export default function Register() {
  const [email, setEmail] = useState('');
  const [pwd, setPwd] = useState('');
  const nav = useNavigate();

  const onSubmit = async (e) => {
    e.preventDefault();
    console.log('🟢 Register form submitted', { email, pwd });
    try {
      // show what URL we’re hitting
      console.log('API baseURL:', api.defaults.baseURL);
      const res = await api.post('/users/register', {
        email,
        password: pwd,
      });
      console.log('✅ Register response:', res.data);
      setToken(res.data.access_token);
      window.dispatchEvent(new Event("storage"));
      nav('/');
    } catch (err) {
      console.error('❌ Register error:', err.response || err);
      alert(err.response?.data?.detail || 'Registration failed');
    }
  };

  return (
    <Form onSubmit={onSubmit}>
      <h2 className="text-xl mb-4">Register</h2>
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
      {/* Explicitly mark this as a submit button */}
      <button
        type="submit"
        className="w-full bg-green-500 text-white p-2"
      >
        Sign Up
      </button>
    </Form>
  );
}
