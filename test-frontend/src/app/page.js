'use client';
import { useState } from 'react';
import {  authStudent } from '@/api/authStudent';

export default function Home() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');

    try {
      const data = await authStudent(email, password);
      const token = data.access_token;

      setSuccess('Zalogowano!');
      window.location.href = "/dashboard";
    } catch (err) {
      if (err.response) {
        setError(err.response.data.detail || 'Błąd logowania');
      } else {
        setError('Błąd połączenia z serwerem');
      }
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center">
      <main className="text-center">
        <h1 className="text-2xl font-bold mb-4">UniversityApp</h1>
        <p>Welcome to the University Application</p>

        <form
          className="mt-8 flex flex-col items-center gap-8"
          onSubmit={handleSubmit}
        >
          <label className="block mb-2 w-64">
            <span className="text-white">Email:</span>
            <input
              type="email"
              className="mt-1 block w-full p-2 border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
              placeholder="Enter your email"
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
          </label>

          <label className="block mb-2 w-64">
            <span className="text-white">Password:</span>
            <input
              type="password"
              className="mt-1 block w-full p-2 border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
              placeholder="Enter your password"
              required
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </label>

          <button
            type="submit"
            className="bg-blue-600 text-white px-6 py-2 rounded hover:bg-blue-700"
          >
            Log in
          </button>
        </form>

        {error && <p className="text-red-600 mt-4">{error}</p>}
        {success && <p className="text-green-600 mt-4">{success}</p>}

        <a href="/register" className="text-blue-800 mt-8 block">
          Register
        </a>
      </main>
    </div>
  );
}
