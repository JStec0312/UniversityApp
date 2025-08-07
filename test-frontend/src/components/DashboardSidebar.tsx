"use client";

import { AvatarFallback, Avatar, AvatarImage } from '@/components/ui/avatar';
import { useUser } from '@/app/context/UserContext';
import { useState, useEffect } from 'react';

export default function DashboardSidebar() {
  const { user } = useUser();
  const [isLoaded, setIsLoaded] = useState(false);

  useEffect(() => {
    // Small delay to prevent flash, then mark as loaded
    const timer = setTimeout(() => {
      setIsLoaded(true);
    }, 100);

    return () => clearTimeout(timer);
  }, []);

  return (
    <aside className="hidden lg:block w-64 min-h-screen bg-white/60 backdrop-blur-lg border-r border-blue-100 shadow-lg">
      <div className="p-6">
        <div className="space-y-4">
          {/* User Profile Section */}
          <div className="bg-gradient-to-r from-blue-500 to-purple-600 rounded-xl p-4 text-white">
            <div className="flex items-center space-x-3">
              <div className="relative">
                {!isLoaded && (
                  <div className="w-12 h-12 bg-white/20 rounded-full animate-pulse" />
                )}
                <Avatar className={`w-12 h-12 transition-opacity duration-300 ${isLoaded ? 'opacity-100' : 'opacity-0 absolute top-0'}`}>
                  <AvatarImage 
                    src={user?.avatarUrl} 
                    alt="Profile Picture"
                    onLoad={() => setIsLoaded(true)}
                  />
                  <AvatarFallback className="bg-white/20 text-white font-semibold">
                    {user?.displayName?.charAt(0)?.toUpperCase() || 'U'}
                  </AvatarFallback>
                </Avatar>
              </div>
              <div>
                <h3 className="font-semibold">
                  {user?.displayName || 'Student'}
                </h3>
                <p className="text-blue-100 text-sm">Portal Studencki</p>
              </div>
            </div>
          </div>

          {/* Quick Stats */}
          <div className="space-y-3">
            <h4 className="text-slate-800 font-semibold text-sm uppercase tracking-wide">Szybkie statystyki</h4>
            <div className="space-y-2">
              <div className="bg-blue-50 rounded-lg p-3 border border-blue-100">
                <div className="text-2xl font-bold text-blue-600">15</div>
                <div className="text-slate-700 text-sm">Nadchodzące wydarzenia</div>
              </div>
              <div className="bg-green-50 rounded-lg p-3 border border-green-100">
                <div className="text-2xl font-bold text-green-600">8</div>
                <div className="text-slate-700 text-sm">Nowe ogłoszenia</div>
              </div>
              <div className="bg-purple-50 rounded-lg p-3 border border-purple-100">
                <div className="text-2xl font-bold text-purple-600">3</div>
                <div className="text-slate-700 text-sm">Aktywne grupy</div>
              </div>
            </div>
          </div>

          {/* Recent Activity */}
          <div className="space-y-3">
            <h4 className="text-slate-800 font-semibold text-sm uppercase tracking-wide">Ostatnia aktywność</h4>
            <div className="space-y-2">
              <div className="text-slate-700 text-sm p-2 bg-slate-50 rounded border border-slate-200">
                Zapisano na konferencję IT
              </div>
              <div className="text-slate-700 text-sm p-2 bg-slate-50 rounded border border-slate-200">
                Nowe ogłoszenie w grupie
              </div>
            </div>
          </div>
        </div>
      </div>
    </aside>
  );
}
