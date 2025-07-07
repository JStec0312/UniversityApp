import axios from '../lib/axiosInstance';

export const getMajorsByFacultyId = async (facultyId) => {
  const response = await axios.get(`/university/get-majors-by-faculty-id/${facultyId}`);
  return response.data;
};