import axios from '../lib/axiosInstance';

export const registerStudent = async (form) => {
  const response = await axios.post('/user', {
    ...form,
    university_id: Number(form.university_id),
  });
  return response.data;
};
