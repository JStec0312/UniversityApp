import instance from "@/lib/axiosInstance";

export const getUserEmail = async () => {
    try {
        const response = await instance.get('/user/getEmail');
        return response.data;
    } catch (error) {
        console.error("Error fetching user email:", error);
        throw error;
    }
}