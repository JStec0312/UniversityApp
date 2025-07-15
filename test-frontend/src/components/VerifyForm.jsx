'use client';
import { useRouter } from 'next/navigation';
import { useState, useEffect } from 'react';
import { getMajors } from '@/api/authApi';
import { verify } from '@/api/authApi';

export default function VerifyForm({ faculties, majors: initialMajors, token }) {
  const router = useRouter();
  const [message, setMessage] = useState('');
  const [majors, setMajors] = useState(initialMajors || []);
  const [facultyId, setFacultyId] = useState(faculties?.[0]?.id || '');
  const [majorId, setMajorId] = useState(initialMajors?.[0]?.id || '');
  const [formSubmitted, setFormSubmitted] = useState(false);
  let timer = 5;
  useEffect(() => {
    const fetchMajors = async () => {
      try {
        const newMajors = await getMajors(facultyId);
        setMajors(newMajors);
        setMajorId(newMajors?.[0]?.id || '');
      } catch (err) {
        console.error("Błąd pobierania majors:", err);
        setMajors([]);
      }
    };

    if (facultyId) fetchMajors();
  }, [facultyId]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try{
      await verify(token, facultyId, majorId);
      setMessage('Konto zostało pomyślnie zweryfikowane! Zostaniesz przekierowany na stronę główną za ' + timer + ' sekund.');
      setFormSubmitted(true);
      const interval = setInterval(() => {
        timer -= 1;
        if (timer <= 0) {
          clearInterval(interval);
          router.push('/'); 
        } else {
          setMessage(`Konto zostało pomyślnie zweryfikowane! Zostaniesz przekierowany na stronę główną za ${timer} sekund.`);
        }
      }, 1000);
    } catch (error) {
      console.error("Błąd weryfikacji:", error);
      setMessage('Wystąpił błąd podczas weryfikacji konta. Spróbuj ponownie.');
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-black text-white">
      <main className="bg-gray-900 p-8 rounded shadow-md w-full max-w-md">
        <h1 className="text-2xl font-bold mb-6 text-center">Weryfikacja konta</h1>

        {!formSubmitted && <form onSubmit={handleSubmit} className="flex flex-col gap-4">
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
            disabled={!majors.length}
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
        </form>}

        {message && <p className="mt-4 text-center">{message}</p>}
      </main>
    </div>
  );
}
