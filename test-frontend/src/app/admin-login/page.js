"use client";
import {useState} from 'react';
import { useRouter } from 'next/navigation';
import { adminLogin } from '@/api/adminAuthApi';
import { useUser } from '@/context/UserContext';

export default function AdminLoginPage(){
    const {setUser} = useUser();
    const [form, setForm] = useState({
        email: '',
        password: ''
    });
    const [message, setMessage] = useState('');
    const router = useRouter();
    const handleInputChange = (e) =>{
        const {name, value} = e.target;
        setForm((prev) => ({
            ...prev,
            [name]: value
        }))
    }
    
    const handleAdminLoginSubmit = async (e) => {
        e.preventDefault();
        try{
            const response = await adminLogin(form.email, form.password);
            setMessage('Zalogowano pomyślnie! Przekierowywanie do panelu administratora...');
            const me = {displayName: response.admin.display_name, universityId: response.admin.university_id, userId: response.admin.user_id, groupId: response.admin.group_id, adminId: response.admin.admin_id, role: 'admin'}
            console.log(me);
            setUser(me); // Set user in context
            setTimeout(() => {
                router.push('/admin-dashboard'); // Redirect to admin dashboard
            }, 2000);
        } catch (error) {
            console.error("Błąd logowania administratora:", error);
            if (error.response && error.response.status === 401) {
                setMessage('Nieprawidłowy email lub hasło.');
            } else {
                setMessage('Wystąpił błąd podczas logowania. Spróbuj ponownie.');
            }
        }
    };
    return(
        <div className="flex items-center justify-center">
            <main className="bg-gray-900 p-8 rounded shadow-md flex flex-col gap-8 w-full max-w-md mx-auto mt-20">
                <h1 className="text-2xl font-bold mb-6 text-center text-white">Admin Login</h1>
                <form onSubmit={handleAdminLoginSubmit} className="flex flex-col gap-4" >
                    <input
                        type="email"
                        placeholder="Email"
                        className="p-2 border rounded bg-gray-800 text-white"
                        required
                        name="email"
                        onChange={handleInputChange}
                        value={form.email}
                    />
                    <input
                        type="password"
                        placeholder="Password"
                        className="p-2 border rounded bg-gray-800 text-white"
                        required
                        name="password"
                        onChange={handleInputChange}
                        value={form.password}
                    />
                    <button
                        type="submit"
                        className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
                    >
                        Login
                    </button>
                </form>
                <a href ="/admin-login/register" className="text-blue-600">Zarejestruj się jako administrator</a>
                <p>{message}</p>
            </main>
        </div>
    )
}