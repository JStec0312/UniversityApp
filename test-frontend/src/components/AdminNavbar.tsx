"use client";

import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { logout } from '@/api/authApi';
export default function AdminNavbar() {
    const router = useRouter();

    const handleLogout = async () => {
        await logout();
        router.push('/admin-login');
    };

    return (
        <nav className="bg-gray-800 shadow-sm">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div className="flex justify-between items-center h-16">
                    {/* Logo/Title */}
                    <div className="flex items-center">
                        <Link href="/admin-dashboard" className="text-white text-xl font-bold">
                            Admin Dashboard
                        </Link>
                    </div>

                    {/* Navigation Links */}
                    <div className="flex items-center space-x-6">
                        <Link 
                            href="/admin-dashboard" 
                            className="text-gray-300 hover:text-white px-3 py-2 rounded-md text-sm font-medium transition-colors"
                        >
                            Dashboard
                        </Link>
                        <Link 
                            href="/admin-dashboard/add-event" 
                            className="text-gray-300 hover:text-white px-3 py-2 rounded-md text-sm font-medium transition-colors"
                        >
                            Add Event
                        </Link>
                        <Link 
                            href="/admin-dashboard/edit-events" 
                            className="text-gray-300 hover:text-white px-3 py-2 rounded-md text-sm font-medium transition-colors"
                        >
                            Manage Events
                        </Link>
                        
                        {/* Logout Button */}
                        <button
                            onClick={handleLogout}
                            className="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-md text-sm font-medium transition-colors"
                        >
                            Logout
                        </button>
                    </div>
                </div>
            </div>
        </nav>
    );
}
