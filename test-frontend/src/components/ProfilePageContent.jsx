"use client";
import { usePathname, useRouter } from "next/navigation";
import Link from "next/link";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Badge } from "@/components/ui/badge";
import { 
  User, 
  Settings, 
  BookOpen, 
  Edit3, 
  Shield, 
  GraduationCap,
  Mail,
  Calendar,
  MapPin
} from "lucide-react";

export default function ProfilePageContent({ user, loading = false }) {
    const here = usePathname();
    const router = useRouter();
    const go = (sub) => `${here}/${sub}`;

    const getRoleInfo = (role) => {
        switch (role) {
            case 'admin':
                return { label: 'Administrator', icon: Shield, color: 'bg-red-500' };
            case 'student':
                return { label: 'Student', icon: GraduationCap, color: 'bg-blue-500' };
            default:
                return { label: 'Superior Admin', icon: Shield, color: 'bg-purple-500' };
        }
    };


    if (loading) {
        return (
            <div className="space-y-8">
                <div className="text-center space-y-4">
                    <div className="inline-flex items-center space-x-2 bg-white/80 backdrop-blur-sm rounded-full px-6 py-2 shadow-lg border border-white/20">
                        <User className="w-5 h-5 text-blue-600" />
                        <span className="text-sm font-medium text-gray-700">Profil</span>
                    </div>
                    <h1 className="text-4xl md:text-5xl font-bold bg-gradient-to-r from-blue-600 via-purple-600 to-indigo-600 bg-clip-text text-transparent">
                        Ładowanie profilu...
                    </h1>
                </div>

                <div className="grid md:grid-cols-2 gap-6">
                    {[...Array(4)].map((_, i) => (
                        <Card key={i} className="bg-white/70 backdrop-blur-sm border-white/20 animate-pulse">
                            <CardContent className="p-6 space-y-3">
                                <div className="h-4 bg-gray-200 rounded w-3/4"></div>
                                <div className="h-3 bg-gray-200 rounded w-1/2"></div>
                            </CardContent>
                        </Card>
                    ))}
                </div>
            </div>
        );
    }

    if (!user) {
        return (
            <div className="space-y-8">
                <div className="text-center space-y-4">
                    <div className="inline-flex items-center space-x-2 bg-white/80 backdrop-blur-sm rounded-full px-6 py-2 shadow-lg border border-white/20">
                        <User className="w-5 h-5 text-blue-600" />
                        <span className="text-sm font-medium text-gray-700">Profil</span>
                    </div>
                    <h1 className="text-4xl md:text-5xl font-bold bg-gradient-to-r from-blue-600 via-purple-600 to-indigo-600 bg-clip-text text-transparent">
                        Brak danych użytkownika
                    </h1>
                </div>

                <Card className="bg-white/70 backdrop-blur-sm border-white/20">
                    <CardContent className="p-12 text-center">
                        <User className="w-16 h-16 mx-auto text-gray-400 mb-4" />
                        <h3 className="text-lg font-semibold text-gray-900 mb-2">
                            Nie można załadować profilu
                        </h3>
                        <p className="text-gray-600 mb-6">
                            Wystąpił problem z ładowaniem danych użytkownika
                        </p>
                        <Button onClick={() => window.location.reload()}>
                            Odśwież profil
                        </Button>
                    </CardContent>
                </Card>
            </div>
        );
    }

    const roleInfo = getRoleInfo(user.role);

    return (
        <div className="space-y-8">
            {/* Header */}
            <div className="text-center space-y-4">
                <div className="inline-flex items-center space-x-2 bg-white/80 backdrop-blur-sm rounded-full px-6 py-2 shadow-lg border border-white/20">
                    <User className="w-5 h-5 text-blue-600" />
                    <span className="text-sm font-medium text-gray-700">Profil</span>
                </div>
                <h1 className="text-4xl md:text-5xl font-bold bg-gradient-to-r from-blue-600 via-purple-600 to-indigo-600 bg-clip-text text-transparent">
                    Twój Profil
                </h1>
                <p className="text-xl text-gray-600 max-w-2xl mx-auto">
                    Zarządzaj swoimi danymi i ustawieniami
                </p>
            </div>

            {/* Profile Overview */}
            <Card className="bg-white/70 backdrop-blur-sm border-white/20">
                <CardContent className="p-8">
                    <div className="flex flex-col md:flex-row items-center md:items-start space-y-6 md:space-y-0 md:space-x-8">
                        <div className="flex flex-col items-center space-y-4">
                            <Avatar className="w-24 h-24">
                                <AvatarImage src={user.avatarUrl || '/default-avatar.png'} alt="User Avatar" />
                                <AvatarFallback className={`${roleInfo.color} text-white text-2xl font-bold`}>
                                    {user.displayName ? user.displayName.charAt(0).toUpperCase() : 'U'}
                                </AvatarFallback>
                            </Avatar>
                            <Badge variant="secondary" className="bg-blue-50 text-blue-700 border-blue-200">
                                <roleInfo.icon className="w-3 h-3 mr-1" />
                                {roleInfo.label}
                            </Badge>
                        </div>
                        
                        <div className="flex-1 text-center md:text-left space-y-2">
                            <h2 className="text-3xl font-bold text-gray-900">
                                {user.displayName || 'Unknown User'}
                            </h2>
                            <p className="text-gray-600 text-lg">
                                {user.role === 'student' ? 'Student uniwersytetu' : 'Administrator systemu'}
                            </p>
                            
                            {/* Quick stats */}
                            <div className="flex flex-wrap justify-center md:justify-start gap-4 pt-4">
                                <div className="flex items-center space-x-2 text-gray-600">
                                    <Calendar className="w-4 h-4" />
                                    <span className="text-sm">Aktywny</span>
                                </div>
                                <div className="flex items-center space-x-2 text-gray-600">
                                    <MapPin className="w-4 h-4" />
                                    <span className="text-sm">Campus główny</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </CardContent>
            </Card>

            {/* User Information Cards */}
            <div className="grid md:grid-cols-2 gap-6">
                <Card className="bg-white/70 backdrop-blur-sm border-white/20">
                    <CardHeader className="pb-3">
                        <CardTitle className="flex items-center space-x-2 text-lg">
                            <User className="w-5 h-5 text-blue-600" />
                            <span>Nazwa wyświetlana</span>
                        </CardTitle>
                    </CardHeader>
                    <CardContent>
                        <p className="text-xl font-semibold text-gray-900">
                            {user.displayName || 'Nie podano'}
                        </p>
                    </CardContent>
                </Card>

                <Card className="bg-white/70 backdrop-blur-sm border-white/20">
                    <CardHeader className="pb-3">
                        <CardTitle className="flex items-center space-x-2 text-lg">
                            <GraduationCap className="w-5 h-5 text-green-600" />
                            <span>ID Uniwersytecki</span>
                        </CardTitle>
                    </CardHeader>
                    <CardContent>
                        <p className="text-xl font-semibold text-gray-900">
                            {user.universityId || 'Nie przypisano'}
                        </p>
                    </CardContent>
                </Card>

                <Card className="bg-white/70 backdrop-blur-sm border-white/20">
                    <CardHeader className="pb-3">
                        <CardTitle className="flex items-center space-x-2 text-lg">
                            <Shield className="w-5 h-5 text-purple-600" />
                            <span>ID Użytkownika</span>
                        </CardTitle>
                    </CardHeader>
                    <CardContent>
                        <p className="text-xl font-semibold text-gray-900">
                            {user.userId || 'Niedostępny'}
                        </p>
                    </CardContent>
                </Card>

                <Card className="bg-white/70 backdrop-blur-sm border-white/20">
                    <CardHeader className="pb-3">
                        <CardTitle className="flex items-center space-x-2 text-lg">
                            <BookOpen className="w-5 h-5 text-orange-600" />
                            <span>{user.role === 'student' ? 'ID Studenta' : 'ID Administratora'}</span>
                        </CardTitle>
                    </CardHeader>
                    <CardContent>
                        <p className="text-xl font-semibold text-gray-900">
                            {user.studentId || user.adminId || 'Nie przypisano'}
                        </p>
                    </CardContent>
                </Card>
            </div>

            {/* Action Buttons */}
            <Card className="bg-white/70 backdrop-blur-sm border-white/20">
                <CardHeader>
                    <CardTitle>Akcje</CardTitle>
                    <CardDescription>
                        Zarządzaj swoim profilem i ustawieniami
                    </CardDescription>
                </CardHeader>
                <CardContent>
                    <div className="flex flex-wrap gap-4">
                        <Button className="bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700">
                            <Edit3 className="w-4 h-4 mr-2" />
                            Edytuj profil
                        </Button>
                        
                        <Link href={go('/settings')}>
                            <Button variant="outline" className="bg-white/70 backdrop-blur-sm border-white/20">
                                <Settings className="w-4 h-4 mr-2" />
                                Ustawienia
                            </Button>
                        </Link>
                        
                        <Button variant="outline" className="bg-white/70 backdrop-blur-sm border-white/20">
                            <BookOpen className="w-4 h-4 mr-2" />
                            Zobacz kursy
                        </Button>
                    </div>
                </CardContent>
            </Card>
        </div>
    );
}