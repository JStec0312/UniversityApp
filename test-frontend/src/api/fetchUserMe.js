import axios from "@/lib/axiosInstance";

export const fetchStudentMe = async () => {
  try {
    const response = await axios.get("/user/student/me");
    return response.data;
  } catch (error) {
    console.error("Error fetching user data:", error);
    throw error; // Rethrow the error to handle it in the calling function
  }
}
