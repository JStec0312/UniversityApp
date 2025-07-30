import instance from "@/lib/axiosInstance";
import AddEventType from "@/types/AddEventType";

export const addEvent = async (eventData: AddEventType) => {
    try{
        const response = await instance.post("/user/admin/event", eventData);
        return response.data;
    } catch (error) {
        console.error("Error adding event:", error);
        throw error;
    }
}