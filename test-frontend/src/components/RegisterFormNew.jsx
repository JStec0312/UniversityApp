"use client";
import { useState, useEffect } from 'react';
import { register } from '@/api/authApi';

export default function RegisterForm({universities}) {
  const [form, setForm] = useState({
    email: '',
    password: '',
    display_name: '',
    university_id: universities[0]?.id || '',
  });

  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleRegisterSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await register(form.email, form.password, form.display_name, form.university_id); 
      setSuccess('Registration successful! Check your email.');
      setError('');
    } catch (err) {
      if(err.response && err.response.status === 400) {
        setError('Email is already taken. Please try another one.');
      } else {
        setError('Registration failed. Please try again.');
        setSuccess('');
      }
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50 flex items-center justify-center px-4">
      <div className="w-full max-w-md">
        {/* Enhanced Header */}
        <div className="text-center mb-8">
          <div className="text-6xl mb-4">🎓</div>
          <h1 className="text-4xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent mb-2">
            Join University
          </h1>
          <p className="text-gray-600">Create your account to get started</p>
        </div>

        {/* Enhanced Form Card */}
        <div className="bg-white/80 backdrop-blur-lg rounded-2xl shadow-xl border border-white/20 p-8">
          <form className="space-y-6" onSubmit={handleRegisterSubmit}>
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">
                  Display Name
                </label>
                <input
                  type="text"
                  name="display_name"
                  placeholder="Enter your display name"
                  value={form.display_name}
                  onChange={handleChange}
                  required
                  className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:ring-4 focus:ring-blue-500/20 focus:border-blue-500 transition-all duration-300 bg-white/90 backdrop-blur-sm"
                />
              </div>

              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">
                  Email Address
                </label>
                <input
                  type="email"
                  name="email"
                  placeholder="Enter your email address"
                  value={form.email}
                  onChange={handleChange}
                  required
                  className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:ring-4 focus:ring-blue-500/20 focus:border-blue-500 transition-all duration-300 bg-white/90 backdrop-blur-sm"
                />
              </div>

              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">
                  Password
                </label>
                <input
                  type="password"
                  name="password"
                  placeholder="Create a strong password"
                  value={form.password}
                  onChange={handleChange}
                  required
                  className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:ring-4 focus:ring-blue-500/20 focus:border-blue-500 transition-all duration-300 bg-white/90 backdrop-blur-sm"
                />
              </div>

              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">
                  University
                </label>
                <select
                  name="university_id"
                  value={form.university_id}
                  onChange={handleChange}
                  required
                  className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:ring-4 focus:ring-blue-500/20 focus:border-blue-500 transition-all duration-300 bg-white/90 backdrop-blur-sm"
                >
                  {universities.map((university) => (
                    <option key={university.id} value={university.id}>
                      {university.name}
                    </option>
                  ))}
                </select>
              </div>
            </div>

            {/* Error and Success Messages */}
            {error && (
              <div className="bg-red-50 border border-red-200 rounded-xl p-4 flex items-center gap-3">
                <span className="text-red-500 text-xl">⚠️</span>
                <p className="text-red-700 font-medium">{error}</p>
              </div>
            )}

            {success && (
              <div className="bg-green-50 border border-green-200 rounded-xl p-4 flex items-center gap-3">
                <span className="text-green-500 text-xl">✅</span>
                <p className="text-green-700 font-medium">{success}</p>
              </div>
            )}

            <button
              type="submit"
              className="w-full bg-gradient-to-r from-blue-500 to-purple-600 text-white py-4 px-6 rounded-xl font-semibold hover:from-blue-600 hover:to-purple-700 transition-colors duration-200 shadow-lg"
            >
              Create Account
            </button>
          </form>

          {/* Footer Links */}
          <div className="mt-6 text-center">
            <p className="text-gray-600">
              Already have an account?{' '}
              <a href="/login" className="text-blue-600 hover:text-blue-700 font-semibold transition-colors">
                Sign in here
              </a>
            </p>
          </div>
        </div>

        {/* Additional Info */}
        <div className="mt-6 text-center text-sm text-gray-500">
          <p>By creating an account, you agree to our Terms of Service and Privacy Policy</p>
        </div>
      </div>
    </div>
  );
}
