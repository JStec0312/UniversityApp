import instance from "../lib/axiosInstance";

export const getPaginatedNews = async (page: number, limit: number) => {
    try {
        const response = await instance.get('/news/all', {
            params: { page, limit }
        });
        return response.data;
    } catch (error) {
        console.error("Error fetching paginated news:", error);
        throw error;
    }
}

export const getNewsById = async (id: string) => {
    try {
        const response = await instance.get(`/news/${id}`);
        return response.data;
    } catch (error) {
        console.error("Error fetching news by ID:", error);
        throw error;
    }
}

