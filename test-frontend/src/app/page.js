'use client';
import { useState } from 'react';
import { useRouter } from 'next/navigation';
import {login} from '@/api/authApi';
import { useUser } from './context/UserContext';
export default function Home() {
  const {setUser} = useUser();
  const navigation = useRouter();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const handleLoginSubmit = async (e) => {
    e.preventDefault();
    try{
      const response = await login(email, password);
      if (response.student) {
        const me = {displayName: response.student.display_name, universityId: response.student.university_id, userId: response.student.user_id, studentId : response.student.student_id, role: 'student', avatarUrl: response.student.avatar_image_url};
        setUser(me);
        setSuccess('Login successful!');
        setError('');
        navigation.push('/dashboard'); 
      }
      else {
        setError('Login failed. Please check your credentials.');
        setSuccess('');
      }
    } catch (err) {
      console.error("Login error:", err);
      setError('An error occurred while logging in. Please try again.');
      setSuccess('');
    }
  }



  return (
    <div className="min-h-screen flex items-center justify-center">
      <main className="text-center">
        <h1 className="text-2xl font-bold mb-4">UniversityApp</h1>
        <p>Welcome to the University Application</p>

        <form
          className="mt-8 flex flex-col items-center gap-8"
          onSubmit = {handleLoginSubmit}
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
