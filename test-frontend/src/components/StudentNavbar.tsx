"use client";

import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { logout } from '@/api/authApi';
export default function StudentNavbar() {
    const router = useRouter();

    const handleLogout = async () => {
        await logout();
        router.push('/');
    };

    return (
        <nav className="bg-blue-600 shadow-sm">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div className="flex justify-between items-center h-16">
                    {/* Logo/Title */}
                    <div className="flex items-center">
                        <Link href="/dashboard" className="text-white text-xl font-bold">
                            Student Portal
                        </Link>
                    </div>

                    {/* Navigation Links */}
                    <div className="flex items-center space-x-6">
                        <Link 
                            href="/dashboard" 
                            className="text-blue-100 hover:text-white px-3 py-2 rounded-md text-sm font-medium transition-colors"
                        >
                            Dashboard
                        </Link>
                        <Link 
                            href="/dashboard/events" 
                            className="text-blue-100 hover:text-white px-3 py-2 rounded-md text-sm font-medium transition-colors"
                        >
                            Events
                        </Link>
                        <Link 
                            href="/dashboard/profile" 
                            className="text-blue-100 hover:text-white px-3 py-2 rounded-md text-sm font-medium transition-colors"
                        >
                            Profile
                        </Link>
                        
                        {/* Logout Button */}
                        <button
                            onClick={handleLogout}
                            className="bg-blue-800 hover:bg-blue-900 text-white px-4 py-2 rounded-md text-sm font-medium transition-colors"
                        >
                            Logout
                        </button>
                    </div>
                </div>
            </div>
        </nav>
    );
}
