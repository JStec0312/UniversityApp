'use client';
import { useSearchParams } from 'next/navigation';
import { useState, useEffect } from 'react';
import { verifyStudent } from '@/api/verifyStudent';
import { getFacultiesByUniversityId } from '@/api/getFacultiesByUniversityId';
import { getMajorsByFacultyId } from '@/api/getMajorsByFacultyId';

export default function VerifyPage() {
  const searchParams = useSearchParams();
  const token = searchParams.get('token');
  const universityId = searchParams.get('university_id');

  const [faculties, setFaculties] = useState([]);
  const [facultyId, setFacultyId] = useState('');
  const [majors, setMajors] = useState([]);
  const [majorId, setMajorId] = useState('');
  const [message, setMessage] = useState('');

  useEffect(() => {
    if (!universityId) return;

    getFacultiesByUniversityId(parseInt(universityId))
      .then((res) => {
        setFaculties(res);
        if (res.length > 0) {
          setFacultyId(res[0].id.toString());
        }
      })
      .catch((err) => {
        console.error(err);
        setMessage('Nie udało się pobrać listy wydziałów');
      });
  }, [universityId]);

  // ⏬ Fetch majors gdy zmienia się wydział
  useEffect(() => {
    if (!facultyId) return;

    getMajorsByFacultyId(parseInt(facultyId))
      .then((res) => {
        setMajors(res);
        if (res.length > 0) {
          setMajorId(res[0].id.toString());
        }
      })
      .catch((err) => {
        console.error(err);
        setMessage('Nie udało się pobrać listy kierunków');
      });
  }, [facultyId]);

  const handleVerify = async (e) => {
    e.preventDefault();
    setMessage('');

    if (!token) {
      setMessage('Brak tokenu w adresie URL');
      return;
    }

    try {
      await verifyStudent(token, {
        faculty_id: facultyId ? parseInt(facultyId) : null,
        major_id: majorId ? parseInt(majorId) : null,
      });
      setMessage('Konto zostało zweryfikowane! Zostaniesz przekierowany do logowania za 5 sekund.');
      setTimeout(() => {
        window.location.href = '/';
      }, 5000); // Przekierowanie po 5 sekundach
    } catch (err) {
      console.error(err);
      setMessage('Błąd podczas weryfikacji');
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-black text-white">
      <main className="bg-gray-900 p-8 rounded shadow-md w-full max-w-md">
        <h1 className="text-2xl font-bold mb-6 text-center">Weryfikacja konta</h1>

        <form onSubmit={handleVerify} className="flex flex-col gap-4">
          <select
            value={facultyId}
            onChange={(e) => setFacultyId(e.target.value)}
            className="p-2 border rounded bg-gray-800 text-white"
          >
            {faculties.map((faculty) => (
              <option key={faculty.id} value={faculty.id}>
                {faculty.name}
              </option>
            ))}
          </select>

          <select
            value={majorId}
            onChange={(e) => setMajorId(e.target.value)}
            className="p-2 border rounded bg-gray-800 text-white"
          >
            {majors.map((major) => (
              <option key={major.id} value={major.id}>
                {major.name}
              </option>
            ))}
          </select>

          <button
            type="submit"
            className="bg-green-600 text-white py-2 rounded hover:bg-green-700"
          >
            Zweryfikuj konto
          </button>
        </form>

        {message && <p className="mt-4 text-center">{message}</p>}
      </main>
    </div>
  );
}
