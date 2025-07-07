import axios from '../lib/axiosInstance';

export const authStudent = async (email, password) => {
  const response = await axios.post('/user/student/auth', {
    email,
    password,
  });
  return response.data;
};
