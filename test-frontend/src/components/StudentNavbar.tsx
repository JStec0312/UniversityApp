"use client";

import { useRouter, usePathname } from 'next/navigation';
import Link from 'next/link';
import { logout } from '@/api/authApi';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { useUser } from '@/app/context/UserContext';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { searchUsers, getUserById } from '@/api/userSearchApi';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';
import UserSearchBar from './UserSearchBar';
import instance from "@/lib/axiosInstance";
import { 
  GraduationCap, 
  Calendar, 
  User, 
  Megaphone,
  Home,
  LogOut,
  Bell,
  Menu,
  ChevronDown
} from 'lucide-react';
import { useState } from 'react';

interface User {
  id: number;
  display_name: string;
  avatar_image_url?: string;
}



export default function StudentNavbar() {
    const router = useRouter();
    const pathname = usePathname();
    const { user } = useUser();

    const handleLogout = async () => {
        await logout();
        router.push('/');
    };

    const navItems = [
        { href: '/dashboard', label: 'Dashboard', icon: Home },
        { href: '/dashboard/events', label: 'Wydarzenia', icon: Calendar },
        { href: '/dashboard/news', label: 'Ogłoszenia', icon: Megaphone },
        { href: '/dashboard/profile', label: 'Profil', icon: User },
    ];

    // Real API search function
    const handleUserSearch = async (query: string): Promise<User[]> => {
        try {
            const users = await searchUsers(query);
            console.log(users);
            return users;
        } catch (error) {
            console.error("Error searching users:", error);
            return [];
        }
    };

    const handleUserSelect = async (selectedUser: User) => {
        try {
            // Navigate to the user's profile page
            router.push(`/dashboard/profile/${selectedUser.id}`);
        } catch (error) {
            console.error("Error navigating to user profile:", error);
        }
    };

    const isActive = (href: string) => pathname === href;

    return (
        <nav className="bg-white border-b border-slate-200 shadow-sm sticky top-0 z-50">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div className="flex justify-between items-center h-16">
                    {/* Logo */}
                    <Link href="/dashboard" className="flex items-center space-x-3 group">
                        <div className="p-2 bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg shadow-sm group-hover:shadow-md transition-shadow">
                            <GraduationCap className="w-5 h-5 text-white" />
                        </div>
                        <span className="font-bold text-slate-900 hidden sm:block">Portal Studencki</span>
                    </Link>

                    {/* Search Bar - Prominent */}
                    <div className="flex-1 max-w-md mx-8">
                        <UserSearchBar
                            onSearch={handleUserSearch}
                            onUserSelect={handleUserSelect}
                            placeholder="Szukaj użytkowników..."
                            className='text-gray-800'
                        />
                    </div>

                    {/* Right Side - Navigation & User */}
                    <div className="flex items-center space-x-2">
                        {/* Navigation Dropdown */}
                        <DropdownMenu>
                            <DropdownMenuTrigger asChild>
                                <Button variant="ghost" size="sm" className="text-slate-700 hover:text-blue-600">
                                    <Menu className="w-4 h-4 mr-1" />
                                    <span className="hidden sm:inline">Menu</span>
                                    <ChevronDown className="w-3 h-3 ml-1" />
                                </Button>
                            </DropdownMenuTrigger>
                            <DropdownMenuContent align="end" className="w-48 bg-white border border-slate-200 shadow-lg">
                                {navItems.map((item) => (
                                    <DropdownMenuItem key={item.href} asChild>
                                        <Link href={item.href} className={`flex items-center space-x-2 px-3 py-2 text-slate-700 hover:bg-slate-50 hover:text-blue-600 ${isActive(item.href) ? 'bg-blue-50 text-blue-600' : ''}`}>
                                            <item.icon className="w-4 h-4" />
                                            <span>{item.label}</span>
                                        </Link>
                                    </DropdownMenuItem>
                                ))}
                            </DropdownMenuContent>
                        </DropdownMenu>
                        
                        {/* Notifications */}
                        <Button variant="ghost" size="sm" className="relative text-slate-700 hover:text-blue-600">
                            <Bell className="w-4 h-4" />
                            <Badge className="absolute -top-1 -right-1 h-4 w-4 text-xs bg-red-500 hover:bg-red-500 flex items-center justify-center">
                                3
                            </Badge>
                        </Button>

                        {/* User Dropdown */}
                        <DropdownMenu>
                            <DropdownMenuTrigger asChild>
                                <Button variant="ghost" size="sm" className="flex items-center space-x-2 text-slate-700 hover:text-blue-600">
                                    <Avatar className="w-6 h-6">
                                        <AvatarImage src={user?.avatarUrl} alt="Profile" />
                                        <AvatarFallback className="text-xs bg-gradient-to-r from-blue-600 to-purple-600 text-white">
                                            {user?.displayName?.charAt(0)?.toUpperCase() || 'U'}
                                        </AvatarFallback>
                                    </Avatar>
                                    <span className="hidden md:inline">{user?.displayName || 'Student'}</span>
                                    <ChevronDown className="w-3 h-3" />
                                </Button>
                            </DropdownMenuTrigger>
                            <DropdownMenuContent align="end" className="w-48 bg-white border border-slate-200 shadow-lg">
                                <DropdownMenuItem asChild>
                                    <Link href="/dashboard/profile" className="flex items-center space-x-2 px-3 py-2 text-slate-700 hover:bg-slate-50 hover:text-blue-600">
                                        <User className="w-4 h-4" />
                                        <span>Mój Profil</span>
                                    </Link>
                                </DropdownMenuItem>
                                <DropdownMenuSeparator className="bg-slate-200" />
                                <DropdownMenuItem onClick={handleLogout} className="px-3 py-2 text-red-600 hover:text-red-700 hover:bg-red-50 cursor-pointer">
                                    <LogOut className="w-4 h-4 mr-2" />
                                    <span>Wyloguj</span>
                                </DropdownMenuItem>
                            </DropdownMenuContent>
                        </DropdownMenu>
                    </div>
                </div>
            </div>
        </nav>
    );
}
