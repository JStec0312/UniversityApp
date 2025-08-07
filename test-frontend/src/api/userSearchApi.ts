import { cookies } from 'next/headers';
import instance from "@/lib/axiosInstance";

export const searchUsers = async (name: string) => {
    try {
        const response = await instance.get(`/user/search`, {
            params: { name: name, limit: 10, offset: 0 }
        });
        return response.data;
    } catch (error) {
        console.error("Error searching users:", error);
        throw error;
    }
};


export const getUserById = async (id: number, cookieHeader = '') => {
  const { data } = await instance.get(`/user/${id}`, {
    headers: { Cookie: cookieHeader },   // ⬅️⭢ API
    withCredentials: true,              // nie zaszkodzi w Node
  });
  return data;
};

