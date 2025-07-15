"use client";
// This component is used to verify the admin's group and password
import {useState, useEffect} from 'react';
import { verifyAdminGroup } from '@/api/adminAuthApi';
export default function AdminVerifyPageContent({ groups,  token}){
    const [formData, setFormData] = useState({
        group_id: groups[0].group_id,
        group_password: ''
    });
    const handleChange = (e) => {
        const {name, value} = e.target;
        setFormData((prev) => ({
            ...prev,
            [name]: value
        }));
    }

    const onSubmit = async (e) => {
        e.preventDefault();
        try{
            const response = await verifyAdminGroup(token, formData.group_id, formData.group_password);
            console.log(response);
        } catch(error){
            console.error("Error:", error);
        }
    }
    return(
        <div className='flex flex-col items-center justify-center min-h-screen bg-black text-white'>
            <form className='flex flex-col gap-8 p-8 bg-blue-600 w-1/2  rounded shadow-lg' onSubmit={onSubmit}>
                <label htmlFor="">Nazwa grupy</label>
                <select name="group_id" onChange={handleChange} className='p-2 border rounded bg-gray-800 text-white'>
                    {groups.map((group, index) => (
                        <option key={index} value={group.group_id}>
                            {group.group_name} 
                        </option>
                    ))}
                </select>
                <label>Hasło grupy</label>
                <input type="password" name="group_password" onChange={handleChange} className='p-2 border rounded bg-gray-800 text-white' />
                <button type="submit" className='bg-blue-700 text-white py-2 rounded hover:bg-blue-800'>
                    Zweryfikuj
                </button>
            </form>
        </div>
    )
}