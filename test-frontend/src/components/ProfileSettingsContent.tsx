"use client";
import { useUser } from "@/app/UserContext";
import { useState } from "react";

export default function ProfileSettingsContent({email}) {
    const { user } = useUser();
    const [activeTab, setActiveTab] = useState("general");
    const [formData, setFormData] = useState({
        displayName: user?.displayName || "",
        email: email || "",
        password: "",
        confirmPassword: "",
        theme: "dark",
        notifications: true
    });
    const [isEditing, setIsEditing] = useState(false);
    const [successMessage, setSuccessMessage] = useState("");

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const { name, value, type, checked } = e.target;
        setFormData(prev => ({
            ...prev,
            [name]: type === "checkbox" ? checked : value
        }));
    };

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        // Here you would submit the form data to your API
        
        // Show success message
        setSuccessMessage("Settings updated successfully!");
        setTimeout(() => setSuccessMessage(""), 3000);
        
        // Exit edit mode
        setIsEditing(false);
    };

    return (
        <div className="max-w-4xl mx-auto p-6">
            <div className="bg-white shadow-lg rounded-lg overflow-hidden">
                {/* Header Section */}
                <div className="bg-gradient-to-r from-blue-500 to-purple-600 px-6 py-8">
                    <h1 className="text-3xl font-bold text-white mb-2">Profile Settings</h1>
                    <p className="text-blue-100">Manage your account preferences and information</p>
                </div>

                {/* Success Message */}
                {successMessage && (
                    <div className="bg-green-100 border-l-4 border-green-500 text-green-700 p-4 mb-4" role="alert">
                        <p className="font-bold">Success</p>
                        <p>{successMessage}</p>
                    </div>
                )}

                {/* Tabs Section */}
                <div className="flex border-b border-gray-200">
                    <button
                        className={`px-6 py-3 font-medium ${activeTab === "general" ? "text-blue-600 border-b-2 border-blue-600" : "text-gray-500 hover:text-gray-700"}`}
                        onClick={() => setActiveTab("general")}
                    >
                        General
                    </button>
                    <button
                        className={`px-6 py-3 font-medium ${activeTab === "security" ? "text-blue-600 border-b-2 border-blue-600" : "text-gray-500 hover:text-gray-700"}`}
                        onClick={() => setActiveTab("security")}
                    >
                        Security
                    </button>
                    <button
                        className={`px-6 py-3 font-medium ${activeTab === "preferences" ? "text-blue-600 border-b-2 border-blue-600" : "text-gray-500 hover:text-gray-700"}`}
                        onClick={() => setActiveTab("preferences")}
                    >
                        Preferences
                    </button>
                </div>

                <div className="p-6">
                    {/* General Settings */}
                    {activeTab === "general" && (
                        <div>
                            <div className="flex justify-between items-center mb-6">
                                <h2 className="text-xl font-semibold text-gray-800">Profile Information</h2>
                                <button 
                                    onClick={() => setIsEditing(!isEditing)}
                                    className="text-blue-600 hover:text-blue-800"
                                >
                                    {isEditing ? "Cancel" : "Edit"}
                                </button>
                            </div>

                            <form onSubmit={handleSubmit}>
                                <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
                                    {/* Display Name */}
                                    <div>
                                        <label className="block text-sm font-medium text-gray-700 mb-1">
                                            Display Name
                                        </label>
                                        {isEditing ? (
                                            <input
                                                type="text"
                                                name="displayName"
                                                value={formData.displayName}
                                                onChange={handleChange}
                                                className="w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                                            />
                                        ) : (
                                            <div className="p-2 bg-gray-50 rounded-md border border-gray-200">
                                                {user?.displayName || "Not set"}
                                            </div>
                                        )}
                                    </div>

                                    {/* Email */}
                                    <div>
                                        <label className="block text-sm font-medium text-gray-700 mb-1">
                                            Email Address
                                        </label>
                                        <div className="p-2 bg-gray-50 rounded-md border border-gray-200">
                                            {email || user?.email || "Not available"}
                                        </div>
                                        <p className="text-xs text-gray-500 mt-1">
                                            Your email cannot be changed
                                        </p>
                                    </div>

                                    {/* User ID */}
                                    <div>
                                        <label className="block text-sm font-medium text-gray-700 mb-1">
                                            User ID
                                        </label>
                                        <div className="p-2 bg-gray-50 rounded-md border border-gray-200">
                                            {user?.userId || "Not available"}
                                        </div>
                                    </div>

                                    {/* Role */}
                                    <div>
                                        <label className="block text-sm font-medium text-gray-700 mb-1">
                                            Role
                                        </label>
                                        <div className="p-2 bg-gray-50 rounded-md border border-gray-200">
                                            {user?.role ? (
                                                <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                                                    {user.role.charAt(0).toUpperCase() + user.role.slice(1)}
                                                </span>
                                            ) : (
                                                "Not assigned"
                                            )}
                                        </div>
                                    </div>
                                </div>

                                {isEditing && (
                                    <div className="flex justify-end">
                                        <button
                                            type="submit"
                                            className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-md font-medium"
                                        >
                                            Save Changes
                                        </button>
                                    </div>
                                )}
                            </form>
                        </div>
                    )}

                    {/* Security Settings */}
                    {activeTab === "security" && (
                        <div>
                            <h2 className="text-xl font-semibold text-gray-800 mb-6">Password & Security</h2>
                            
                            <form onSubmit={handleSubmit}>
                                <div className="space-y-4 mb-6">
                                    <div>
                                        <label className="block text-sm font-medium text-gray-700 mb-1">
                                            Current Password
                                        </label>
                                        <input
                                            type="password"
                                            name="currentPassword"
                                            className="w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                                            placeholder="Enter your current password"
                                        />
                                    </div>
                                    
                                    <div>
                                        <label className="block text-sm font-medium text-gray-700 mb-1">
                                            New Password
                                        </label>
                                        <input
                                            type="password"
                                            name="password"
                                            value={formData.password}
                                            onChange={handleChange}
                                            className="w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                                            placeholder="Enter new password"
                                        />
                                    </div>
                                    
                                    <div>
                                        <label className="block text-sm font-medium text-gray-700 mb-1">
                                            Confirm New Password
                                        </label>
                                        <input
                                            type="password"
                                            name="confirmPassword"
                                            value={formData.confirmPassword}
                                            onChange={handleChange}
                                            className="w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                                            placeholder="Confirm new password"
                                        />
                                    </div>
                                </div>
                                
                                <div className="flex justify-end">
                                    <button
                                        type="submit"
                                        className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-md font-medium"
                                    >
                                        Update Password
                                    </button>
                                </div>
                            </form>
                        </div>
                    )}

                    {/* Preferences Settings */}
                    {activeTab === "preferences" && (
                        <div>
                            <h2 className="text-xl font-semibold text-gray-800 mb-6">Application Preferences</h2>
                            
                            <form onSubmit={handleSubmit}>
                                <div className="space-y-6 mb-6">
                                    <div>
                                        <label className="block text-sm font-medium text-gray-700 mb-2">
                                            Theme
                                        </label>
                                        <div className="flex space-x-4">
                                            <label className="inline-flex items-center">
                                                <input
                                                    type="radio"
                                                    name="theme"
                                                    value="light"
                                                    checked={formData.theme === "light"}
                                                    onChange={() => setFormData({...formData, theme: "light"})}
                                                    className="h-4 w-4 text-blue-600 focus:ring-blue-500"
                                                />
                                                <span className="ml-2 text-gray-700">Light</span>
                                            </label>
                                            <label className="inline-flex items-center">
                                                <input
                                                    type="radio"
                                                    name="theme"
                                                    value="dark"
                                                    checked={formData.theme === "dark"}
                                                    onChange={() => setFormData({...formData, theme: "dark"})}
                                                    className="h-4 w-4 text-blue-600 focus:ring-blue-500"
                                                />
                                                <span className="ml-2 text-gray-700">Dark</span>
                                            </label>
                                            <label className="inline-flex items-center">
                                                <input
                                                    type="radio"
                                                    name="theme"
                                                    value="system"
                                                    checked={formData.theme === "system"}
                                                    onChange={() => setFormData({...formData, theme: "system"})}
                                                    className="h-4 w-4 text-blue-600 focus:ring-blue-500"
                                                />
                                                <span className="ml-2 text-gray-700">System</span>
                                            </label>
                                        </div>
                                    </div>
                                    
                                    <div>
                                        <label className="flex items-center">
                                            <input
                                                type="checkbox"
                                                name="notifications"
                                                checked={formData.notifications}
                                                onChange={handleChange}
                                                className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                                            />
                                            <span className="ml-2 text-gray-700">
                                                Enable email notifications
                                            </span>
                                        </label>
                                    </div>
                                </div>
                                
                                <div className="flex justify-end">
                                    <button
                                        type="submit"
                                        className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-md font-medium"
                                    >
                                        Save Preferences
                                    </button>
                                </div>
                            </form>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}