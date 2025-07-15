"use client";
import { useState, useEffect } from 'react';
import { register } from '@/api/authApi';
export default function RegisterForm({universities}) {
  const [form, setForm] = useState({
    email: '',
    password: '',
    display_name: '',
    university_id: universities[0].id,
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
      setSuccess('Rejestracja zakończona sukcesem! Sprawdź swoją skrzynkę e-mail.');
      setError('');
    } catch (err) {
      if(err.response && err.response.status === 400) {
        setError('Podany email jest już zajęty. Spróbuj inny.');
      } else {
      setError('Wystąpił błąd podczas rejestracji. Spróbuj ponownie.');
      setSuccess('');
      }
    }
  };

    

  return (
    <div className="min-h-screen flex items-center justify-center bg-black text-white">
      <main className="bg-gray-900 p-8 rounded shadow-md w-full max-w-md">
        <h1 className="text-2xl font-bold mb-6 text-center">Zarejestruj się</h1>

        <form  className="flex flex-col gap-4" onSubmit={handleRegisterSubmit}>
          <input
            type="text"
            name="display_name"
            placeholder="Display Name"
            value={form.display_name}
            onChange={handleChange}
            className="p-2 border rounded bg-gray-800 text-white"
            required
          />
          <input
            type="email"
            name="email"
            placeholder="Email"
            value={form.email}
            onChange={handleChange}
            className="p-2 border rounded bg-gray-800 text-white"
            required
          />
          <input
            type="password"
            name="password"
            placeholder="Hasło"
            value={form.password}
            onChange={handleChange}
            className="p-2 border rounded bg-gray-800 text-white"
            required
          />
          <select
            name="university_id"
            value={form.university_id}
            onChange={handleChange}
            className="p-2 border rounded bg-gray-800 text-white"
            required
          >
            {universities.map((uni) => (
              <option key={uni.id} value={uni.id}>
                {uni.name}
              </option>
            ))}
          </select>
          <button
            type="submit"
            className="bg-blue-600 text-white py-2 rounded hover:bg-blue-700"
          >
            Zarejestruj
          </button>
        </form>

        {error && <p className="text-red-500 mt-4">{error}</p>}
        {success && <p className="text-green-400 mt-4">{success}</p>}

        <a href="/" className="block text-blue-400 mt-6 text-center">
          Wróć do logowania
        </a>
      </main>
    </div>
  );
}