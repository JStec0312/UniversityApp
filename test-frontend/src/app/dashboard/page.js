"use client";

import { useRouter, usePathname } from "next/navigation";
import Link from "next/link";
import { logout } from "@/api/authApi";
import { useSetUser } from "@/app/context/UserContext";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { 
  Calendar, 
  Users, 
  Megaphone, 
  User, 
  BookOpen,
  TrendingUp,
  Clock,
  MapPin
} from "lucide-react";

export default function DashboardPage() {
  const router = useRouter();
  const pathname = usePathname();
  const base = pathname.endsWith("/") ? pathname.slice(0, -1) : pathname;
  const setUser = useSetUser();

  const handleLogout = async () => {
    try {
      await logout();
      setUser(null);
      router.push("/");
    } catch (error) {
      console.error("Logout error:", error);
    }
  };

  const go = (sub) => `${base}${sub}`;

  const dashboardCards = [
    {
      title: "Wydarzenia",
      description: "Przeglądaj nadchodzące i przeszłe wydarzenia",
      icon: Calendar,
      href: go("/events"),
      color: "bg-gradient-to-br from-blue-500 to-blue-600",
      stats: "15 nadchodzących"
    },
    {
      title: "Ogłoszenia", 
      description: "Najnowsze informacje i komunikaty",
      icon: Megaphone,
      href: go("/news"),
      color: "bg-gradient-to-br from-green-500 to-green-600",
      stats: "8 nowych"
    },
    {
      title: "Grupy",
      description: "Twoje grupy studenckie i organizacje",
      icon: Users,
      href: go("/groups"),
      color: "bg-gradient-to-br from-purple-500 to-purple-600", 
      stats: "3 członkostwa"
    },
    {
      title: "Profil",
      description: "Zarządzaj swoim kontem i ustawieniami",
      icon: User,
      href: go("/profile"),
      color: "bg-gradient-to-br from-orange-500 to-orange-600",
      stats: "Kompletny profil"
    }
  ];

  const quickStats = [
    { label: "Najbliższe wydarzenie", value: "Za 2 dni", icon: Clock },
    { label: "Aktywne grupy", value: "3", icon: Users },
    { label: "Ukończone wydarzenia", value: "12", icon: TrendingUp },
    { label: "Campus", value: "Główny", icon: MapPin }
  ];

  return (
    <div className="space-y-8">
      {/* Welcome Header */}
      <div className="text-center space-y-4">
        <div className="inline-flex items-center space-x-2 bg-white/90 backdrop-blur-sm rounded-full px-6 py-2 shadow-lg border border-blue-200">
          <BookOpen className="w-5 h-5 text-blue-600" />
          <span className="text-sm font-medium text-slate-800">Student Portal</span>
        </div>
        <h1 className="text-4xl md:text-5xl font-bold bg-gradient-to-r from-blue-600 via-purple-600 to-indigo-600 bg-clip-text text-transparent">
          Witaj w portalu studenckim
        </h1>
        <p className="text-xl text-slate-700 max-w-2xl mx-auto">
          Zarządzaj swoją uniwersytecką podróżą w jednym miejscu
        </p>
      </div>

      {/* Quick Stats - Only show on smaller screens since sidebar has them */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 lg:hidden">
        {quickStats.map((stat, index) => (
          <Card key={index} className="bg-white/80 backdrop-blur-sm border-blue-100 hover:bg-white/90 transition-colors shadow-md">
            <CardContent className="p-4 text-center">
              <stat.icon className="w-8 h-8 mx-auto mb-2 text-blue-600" />
              <p className="text-2xl font-bold text-slate-900">{stat.value}</p>
              <p className="text-sm text-slate-700">{stat.label}</p>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Main Navigation Cards */}
      <div className="grid md:grid-cols-2 gap-6">
        {dashboardCards.map((card, index) => (
          <Link key={index} href={card.href} className="group">
            <Card className="h-full bg-white/80 backdrop-blur-sm border-blue-100 hover:bg-white/90 hover:shadow-xl transition-all duration-300 group-hover:scale-[1.02] shadow-md">
              <CardHeader className="pb-3">
                <div className="flex items-center justify-between">
                  <div className={`p-3 rounded-xl ${card.color} shadow-lg`}>
                    <card.icon className="w-6 h-6 text-white" />
                  </div>
                  <Badge variant="secondary" className="bg-blue-50 text-blue-700 border-blue-200">
                    {card.stats}
                  </Badge>
                </div>
                <CardTitle className="text-xl font-bold text-slate-900 group-hover:text-blue-600 transition-colors">
                  {card.title}
                </CardTitle>
                <CardDescription className="text-slate-700">
                  {card.description}
                </CardDescription>
              </CardHeader>
            </Card>
          </Link>
        ))}
      </div>

      {/* Recent Activity */}
      <Card className="bg-white/80 backdrop-blur-sm border-blue-100 shadow-md">
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <TrendingUp className="w-5 h-5 text-blue-600" />
            <span>Ostatnia aktywność</span>
          </CardTitle>
          <CardDescription className="text-slate-700">
            Twoje najnowsze działania w portalu
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="space-y-3">
            <div className="flex items-center space-x-3 p-3 rounded-lg bg-blue-50 border border-blue-200">
              <Calendar className="w-5 h-5 text-blue-600" />
              <div className="flex-1">
                <p className="font-medium text-slate-900">Zapisałeś się na wydarzenie</p>
                <p className="text-sm text-slate-700">Konferencja IT - wczoraj</p>
              </div>
            </div>
            <div className="flex items-center space-x-3 p-3 rounded-lg bg-green-50 border border-green-200">
              <Megaphone className="w-5 h-5 text-green-600" />
              <div className="flex-1">
                <p className="font-medium text-slate-900">Nowe ogłoszenie</p>
                <p className="text-sm text-slate-700">Zmiana harmonogramu zajęć - 2 dni temu</p>
              </div>
            </div>
            <div className="flex items-center space-x-3 p-3 rounded-lg bg-purple-50 border border-purple-200">
              <Users className="w-5 h-5 text-purple-600" />
              <div className="flex-1">
                <p className="font-medium text-slate-900">Dołączyłeś do grupy</p>
                <p className="text-sm text-slate-700">Koło Naukowe Informatyków - tydzień temu</p>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Logout Button */}
      <div className="flex justify-center pt-4">
        <Button 
          onClick={handleLogout} 
          variant="outline"
          className="bg-white/80 backdrop-blur-sm border-red-200 text-red-600 hover:bg-red-50 hover:border-red-300"
        >
          Wyloguj się
        </Button>
      </div>
    </div>
  );
}
