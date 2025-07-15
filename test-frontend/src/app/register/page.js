import RegisterForm from "@/components/RegisterFrom";
import { getUniversities } from "@/api/authApi";
export default async function RegisterPage() {
  let universities = [];
  try {
    universities = await getUniversities();
  } catch (error) {
    alert(error);
  }

  return (
      <RegisterForm universities={universities} />
  );
}

