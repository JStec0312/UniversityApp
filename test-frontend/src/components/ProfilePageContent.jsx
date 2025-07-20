import { usePathname, useRouter } from "next/navigation";
import Link from "next/link";

export default function ProfilePageContent({ user, loading = false }) {
    const here = usePathname();
    const router = useRouter();
    const go = (sub) => `${here}/${sub}`;
    
    return (
        <div className="max-w-4xl mx-auto p-6">
            <div className="bg-white shadow-lg rounded-lg overflow-hidden">
                {/* Header Section */}
                <div className="bg-gradient-to-r from-blue-500 to-purple-600 px-6 py-8">
                    <h1 className="text-3xl font-bold text-white mb-2">Profile Page</h1>
                    <p className="text-blue-100">Manage your account information</p>
                </div>

                {/* Content Section */}
                <div className="p-6">
                    {loading ? (
                        // Loading State
                        <div className="text-center py-12">
                            <div className="relative w-24 h-24 mx-auto mb-6">
                                <div className="absolute inset-0 rounded-full border-4 border-gray-200"></div>
                                <div className="absolute inset-0 rounded-full border-4 border-blue-500 border-t-transparent animate-spin"></div>
                            </div>
                            <div className="space-y-4">
                                <h3 className="text-xl font-semibold text-gray-700">Loading Profile...</h3>
                                <p className="text-gray-500">Please wait while we fetch your information.</p>
                                
                                {/* Skeleton placeholders */}
                                <div className="max-w-md mx-auto space-y-4 mt-8">
                                    <div className="flex items-center space-x-4">
                                        <div className="w-16 h-16 bg-gray-200 rounded-full animate-pulse"></div>
                                        <div className="flex-1 space-y-2">
                                            <div className="h-4 bg-gray-200 rounded animate-pulse"></div>
                                            <div className="h-3 bg-gray-200 rounded w-2/3 animate-pulse"></div>
                                        </div>
                                    </div>
                                    
                                    <div className="grid grid-cols-2 gap-4 mt-6">
                                        <div className="h-20 bg-gray-200 rounded-lg animate-pulse"></div>
                                        <div className="h-20 bg-gray-200 rounded-lg animate-pulse"></div>
                                        <div className="h-20 bg-gray-200 rounded-lg animate-pulse"></div>
                                        <div className="h-20 bg-gray-200 rounded-lg animate-pulse"></div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    ) : user ? (
                        <div className="space-y-6">
                            {/* User Avatar Section */}
                            <div className="flex items-center space-x-4 mb-8">
                                <div className="w-20 h-20 bg-gradient-to-br from-blue-400 to-purple-500 rounded-full flex items-center justify-center">
                                    <span className="text-2xl font-bold text-white">
                                        {user.displayName ? user.displayName.charAt(0).toUpperCase() : 'U'}
                                    </span>
                                </div>
                                <div>
                                    <h2 className="text-2xl font-semibold text-gray-800">
                                        {user.displayName || 'Unknown User'}
                                    </h2>
                                    <p className="text-gray-600">{(() => {
                                        if (user.role === 'admin') {
                                            return 'Administrator';
                                        } else if (user.role === 'student') {
                                            return 'Student';
                                        } else {
                                            return 'Superior Admin';
                                        }
                                    })()}</p>
                                </div>
                            </div>

                            {/* User Information Cards */}
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                                <div className="bg-gray-50 rounded-lg p-4 border-l-4 border-blue-500">
                                    <h3 className="text-lg font-semibold text-gray-700 mb-2">Display Name</h3>
                                    <p className="text-gray-900 font-medium">
                                        {user.displayName || 'Not provided'}
                                    </p>
                                </div>

                                <div className="bg-gray-50 rounded-lg p-4 border-l-4 border-green-500">
                                    <h3 className="text-lg font-semibold text-gray-700 mb-2">University ID</h3>
                                    <p className="text-gray-900 font-medium">
                                        {user.universityId || 'Not assigned'}
                                    </p>
                                </div>

                                <div className="bg-gray-50 rounded-lg p-4 border-l-4 border-purple-500">
                                    <h3 className="text-lg font-semibold text-gray-700 mb-2">User ID</h3>
                                    <p className="text-gray-900 font-medium">
                                        {user.userId || 'Not available'}
                                    </p>
                                </div>

                                <div className="bg-gray-50 rounded-lg p-4 border-l-4 border-orange-500">
                                    <h3 className="text-lg font-semibold text-gray-700 mb-2">{user.role === 'student' ? 'Student ID' : 'Admin ID'}</h3>
                                    <p className="text-gray-900 font-medium">
                                        {user.studentId || user.adminId || 'Not assigned'}
                                    </p>
                                </div>
                            </div>

                            {/* Action Buttons */}
                            <div className="flex flex-wrap gap-3 pt-6 border-t border-gray-200">
                                <button className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-lg font-medium transition-colors duration-200 flex items-center space-x-2">
                                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                                    </svg>
                                    <span>Edit Profile</span>
                                </button>
                                
                                <button className="bg-gray-600 hover:bg-gray-700 text-white px-6 py-3 rounded-lg font-medium transition-colors duration-200 flex items-center space-x-2">
                                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                                    </svg>
                                    <span><Link href={go('settings')}>Settings</Link></span>
                                </button>
                                
                                <button className="bg-green-600 hover:bg-green-700 text-white px-6 py-3 rounded-lg font-medium transition-colors duration-200 flex items-center space-x-2">
                                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                                    </svg>
                                    <span>View Courses</span>
                                </button>
                            </div>
                        </div>
                    ) : (
                        <div className="text-center py-12">
                            <div className="w-24 h-24 bg-gray-200 rounded-full mx-auto mb-4 flex items-center justify-center">
                                <svg className="w-12 h-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                                </svg>
                            </div>
                            <h3 className="text-xl font-semibold text-gray-700 mb-2">No User Data Available</h3>
                            <p className="text-gray-500 mb-6">Unable to load profile information at this time.</p>
                            <button className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-lg font-medium transition-colors duration-200">
                                Refresh Profile
                            </button>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}