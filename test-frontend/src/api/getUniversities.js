import axios from '../lib/axiosInstance';

export const getUniversities = async () => {
  const response = await axios.get('/university/get-universities');
  return response.data;
};
