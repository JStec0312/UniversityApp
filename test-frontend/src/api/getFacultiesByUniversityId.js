import axios from '../lib/axiosInstance';

export const getFacultiesByUniversityId = async (universityId) => {
  const response = await axios.get(`/university/get-faculties-by-uni-id/${universityId}`);
  return response.data;
};