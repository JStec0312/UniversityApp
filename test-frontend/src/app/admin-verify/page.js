import { getGroupsByUniversityId } from "@/api/adminAuthApi";
import AdminVerifyPageContent from "@/components/AdminVerifyPageContent";

export default async function adminVerifyPage({searchParams}) {
      const { token, university_id } = await searchParams;

    if (!token) {
        return <p className="text-red-500">Brak tokenu w parametrach URL.</p>;
    }
    if (isNaN(university_id)) {
        return <p className="text-red-500">Nieprawidłowy identyfikator uniwersytetu.</p>;
    }   
    
    let groups = [];
    try{
        groups = await getGroupsByUniversityId(university_id);
        if (!groups || groups.length === 0) {
            throw new Error("No groups found for the specified university.");
        }
    } catch (error) {
        console.error("Error fetching groups:", error);
    }

    return (
        <AdminVerifyPageContent groups={groups} university_id={university_id} token={token}  />
    )

}