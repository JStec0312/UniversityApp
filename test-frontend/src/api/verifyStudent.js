import axios from '../lib/axiosInstance';

export const verifyStudent = async (token, data) => {
  const response = await axios.post(`/user/verify/student/${token}`, data);
  return response.data;
};
