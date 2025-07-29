import instance from "@/lib/axiosInstance";

export const adminLogin = async (email, password) => {
    try {
        const response = await instance.post('/user/admin/auth', {
            email,
            password
        });
        return response.data;
    } catch (error) {
        console.error("Admin login error:", error);
        throw error;
    }
}

export const getGroupsByUniversityId = async (universityId) => {
    try {
        const response = await instance.get(`/group/get-groups-by-university-id/${universityId}`);
        return response.data;
    } catch (error) {
        console.error("Error fetching groups:", error);
        throw error;
    }
}

export const verifyAdminGroup = async (token, group_id, group_password)  => {
        try{
            const verification_info = {
            group_id: parseInt(group_id, 10),
            group_password: group_password
        };
        const response = await instance.post(`/user/admin/verify/${token}`, verification_info);
        return response.data;
    } catch (error) {
        throw error;
    }
}