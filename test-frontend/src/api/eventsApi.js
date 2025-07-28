import instance from "@/lib/axiosInstance";


export const getUpcomingEvents = async () => {
    try{
        const response = await instance.get("/event/upcoming");
        return response.data;
    } catch (error) {
        console.error("Error fetching upcoming events:", error);
        throw error;
    }

};