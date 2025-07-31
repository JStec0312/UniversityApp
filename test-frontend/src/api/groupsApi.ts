import instance from "@/lib/axiosInstance";


export const getGroups = async () => {
    try {
        const response = await instance.get(`/group/get-groups-from-university`);
        return response.data;
    } catch (error) {
        console.error("Error fetching groups:", error);
        throw error;
    }
}

