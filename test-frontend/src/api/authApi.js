import instance from "@/lib/axiosInstance";

export const login = async (email, password) => {
    try{
        const response = await instance.post('/user/student/auth', {
            email,
            password
        })

        return response.data;
    }
    catch (error) {
        console.error("Login error:", error);
        throw error;
    }
}

export const logout = async () => {
    try {
        const response = await instance.post('/user/student/logout');
        return response.data;
    } catch (error) {
        console.error("Logout error:", error);
        throw error;
    }
}

export const getUniversities = async () => {
    try {
        const response = await instance.get('/university/get-universities');
        return response.data;
    } catch (error) {
        console.error("Error fetching universities:", error);
        throw error;
    }
}

export const getFaculties = async (universityId) => {
    try{
        const response = await instance.get(`/university/get-faculties-by-uni-id/${universityId}`);
        return response.data;
    } catch (error) {
        console.error("Error fetching faculties:", error);
        throw error;
    }
}

export const getMajors = async (facultyId) => {
    try{
        const response = await instance.get(`/university/get-majors-by-faculty-id/${facultyId}`);
        return response.data;
    } catch (error) {
        console.error("Error fetching majors:", error);
        throw error;
    }
}

export const register = async (email, password, display_name, university_id) => {
    const res = await instance.post("/user/", {
        email,
        password,
        display_name,
        university_id: parseInt(university_id, 10),
    });
    if(res.status===400){
        throw new Error("Email already exists");
    }
    return res.data;
};

export const verify = async (token, facultyId, majorId) => {
    try {
        const response = await instance.post(`/user/student/verify/${token}`, {
            faculty_id: parseInt(facultyId, 10),
            major_id: parseInt(majorId, 10)
        });
        return response.data;
    } catch (error) {
        console.error("Verification error:", error);
        throw error;
    }
}