import VerifyForm from "@/components/VerifyForm";
import { getFaculties, getMajors } from "@/api/authApi";

export default async function VerifyPage({ searchParams }) {
  const universityId = parseInt(searchParams.university_id, 10);
  const token        = searchParams.token ?? "";

  let faculties = [];
  let majors    = [];

  try {
    faculties = await getFaculties(universityId);
    if (faculties.length) {
      majors = await getMajors(faculties[0].id);
    }
  } catch (err) {
    console.error("Fetch error:", err);
    return <p className="text-red-500">Nie udało się pobrać danych.</p>;
  }

  return (
    <VerifyForm
      faculties={faculties}
      majors={majors}
      token={token}
    />
  );
}
