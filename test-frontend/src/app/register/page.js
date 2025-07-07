'use client';
import { useState, useEffect } from 'react';
import { getUniversities } from '@/api/getUniversities';
import { registerStudent } from '@/api/authRegister';

export default function Register() {
  const [form, setForm] = useState({
    email: '',
    password: '',
    display_name: '',
    university_id: '',
  });

  const [universities, setUniversities] = useState([]);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  useEffect(() => {
    getUniversities()
      .then((res) => {
        setUniversities(res);
        if (res.length > 0) {
          setForm((prev) => ({ ...prev, university_id: res[0].id }));
        }
      })
      .catch((err) => {
        console.error(err);
        setError('Nie udało się pobrać uniwersytetów');
      });
  }, []);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');

    try {
      await registerStudent({
        ...form,
        university_id: Number(form.university_id),
      });
      setSuccess('Konto zostało utworzone - na maila wysłaliśmy kod weryfikacyjny!');
    } catch (err) {
      console.error(err);
      if (err.response?.data?.detail) {
        setError(err.response.data.detail);
      } else {
        setError('Rejestracja nie powiodła się');
      }
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-black text-white">
      <main className="bg-gray-900 p-8 rounded shadow-md w-full max-w-md">
        <h1 className="text-2xl font-bold mb-6 text-center">Zarejestruj się</h1>

        <form onSubmit={handleSubmit} className="flex flex-col gap-4">
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
