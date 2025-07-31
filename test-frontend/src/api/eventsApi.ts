import instance from "@/lib/axiosInstance";
import { UpdateEventType } from "@/types/UpdateEventType";

export const getUpcomingEvents = async (limit: number, offset: number) => {
    try{
        const response = await instance.get("/event/upcoming", {
            params: {
                limit,
                offset
            }
        });
        return response.data;
    } catch (error) {
        console.error("Error fetching upcoming events:", error);
        throw error;
    }

};

export const getPastEvents = async (limit: number, offset: number) => {
    try{
        const response = await instance.get("/event/past", {
            params: {
                limit,
                offset
            }
        });
        return response.data;
    } catch (error) {
        console.error("Error fetching past events:", error);
        throw error;
    }
}

export const getEventsByName = async (name: string) => {
    try {
        const response = await instance.get(`/event/search`, {
            params: {
                name
            }
        });
        return response.data;
    } catch (error) {
        console.error("Error fetching events by name:", error);
        throw error;
    }
}

export const getAllEvents = async (limit: number, offset: number) => {
    try {
        const response = await instance.get("/event/all", {
            params: {
                limit,
                offset
            }
        });
        return response.data;
    } catch (error) {
        console.error("Error fetching all events:", error);
        throw error;
    }
};

export const fetchEventById = async (id: number) => {
    try {
        const response = await instance.get(`/event/${id}`);
        return response.data;
    } catch (error) {
        console.error("Error fetching event by ID:", error);
        throw error;
    }
}

export const updateEvent = async (id: number, eventData: UpdateEventType) => {
    try {
        const response = await instance.patch(`/event/${id}`, eventData);
        return response.data;
    } catch (error) {
        console.error("Error updating event:", error);
        throw error;
    }
}

export const deleteEvent = async (id: number) => {
    try {
        const response = await instance.delete(`/event/${id}`);
        return response.data;
    } catch (error) {
        console.error("Error deleting event:", error);
        throw error;
    }
}


    


