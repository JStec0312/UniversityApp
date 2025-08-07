"use client";

import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { Badge } from '@/components/ui/badge';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Separator } from '@/components/ui/separator';
import { 
    Mail, 
    User, 
    Calendar, 
    MapPin, 
    Phone, 
    GraduationCap,
    BookOpen,
    Award,
    MessageCircle,
    ArrowLeft
} from 'lucide-react';
import { useRouter } from 'next/navigation';

interface UserProfileProps {
    user: {
        id: number;
        display_name: string;
        email?: string;
        avatar_image_url?: string;
        role?: string;
        university_id?: number;
        phone?: string;
        location?: string;
        bio?: string;
        join_date?: string;
        study_program?: string;
        year_of_study?: number;
        achievements?: string[];
    };
}

export default function UserProfileContent({ user }: UserProfileProps) {
    const router = useRouter();

    const getRoleBadgeColor = (role?: string) => {
        switch (role?.toLowerCase()) {
            case 'student':
                return 'bg-blue-100 text-blue-800 hover:bg-blue-100';
            case 'professor':
                return 'bg-purple-100 text-purple-800 hover:bg-purple-100';
            case 'lecturer':
                return 'bg-green-100 text-green-800 hover:bg-green-100';
            case 'admin':
                return 'bg-red-100 text-red-800 hover:bg-red-100';
            default:
                return 'bg-slate-100 text-slate-800 hover:bg-slate-100';
        }
    };

    const formatDate = (dateString?: string) => {
        if (!dateString) return 'Nieznana';
        return new Date(dateString).toLocaleDateString('pl-PL', {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        });
    };

    return (
        <div className="min-h-screen bg-gradient-to-br from-blue-50 to-purple-50 p-6">
            <div className="max-w-4xl mx-auto">
                {/* Header with back button */}
                <div className="mb-6">
                    <Button 
                        variant="ghost" 
                        onClick={() => router.back()}
                        className="mb-4 text-slate-700 hover:text-blue-600"
                    >
                        <ArrowLeft className="w-4 h-4 mr-2" />
                        Powrót
                    </Button>
                </div>

                {/* Profile Header Card */}
                <Card className="mb-6 border-0 shadow-lg bg-white/80 backdrop-blur-sm">
                    <CardContent className="p-8">
                        <div className="flex flex-col md:flex-row items-start md:items-center gap-6">
                            <Avatar className="w-24 h-24 border-4 border-white shadow-lg">
                                <AvatarImage src={user.avatar_image_url} alt={user.display_name} />
                                <AvatarFallback className="text-2xl bg-gradient-to-r from-blue-600 to-purple-600 text-white">
                                    {user.display_name?.charAt(0)?.toUpperCase() || 'U'}
                                </AvatarFallback>
                            </Avatar>
                            
                            <div className="flex-1">
                                <div className="flex flex-col md:flex-row md:items-center gap-3 mb-3">
                                    <h1 className="text-3xl font-bold text-slate-900">{user.display_name}</h1>
                                    {user.role && (
                                        <Badge className={getRoleBadgeColor(user.role)}>
                                            {user.role === 'student' ? 'Student' : 
                                             user.role === 'professor' ? 'Profesor' :
                                             user.role === 'lecturer' ? 'Wykładowca' :
                                             user.role === 'admin' ? 'Administrator' : user.role}
                                        </Badge>
                                    )}
                                </div>
                                
                                {user.bio && (
                                    <p className="text-slate-600 mb-4 leading-relaxed">{user.bio}</p>
                                )}
                                
                                <div className="flex flex-wrap gap-4 text-sm text-slate-600">
                                    {user.email && (
                                        <div className="flex items-center gap-2">
                                            <Mail className="w-4 h-4" />
                                            <span>{user.email}</span>
                                        </div>
                                    )}
                                    {user.phone && (
                                        <div className="flex items-center gap-2">
                                            <Phone className="w-4 h-4" />
                                            <span>{user.phone}</span>
                                        </div>
                                    )}
                                    {user.location && (
                                        <div className="flex items-center gap-2">
                                            <MapPin className="w-4 h-4" />
                                            <span>{user.location}</span>
                                        </div>
                                    )}
                                </div>
                            </div>
                            
                            <div className="flex gap-3">
                                <Button variant="outline" size="sm">
                                    <MessageCircle className="w-4 h-4 mr-2" />
                                    Wyślij wiadomość
                                </Button>
                            </div>
                        </div>
                    </CardContent>
                </Card>

                <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                    {/* Academic Information */}
                    <Card className="border-0 shadow-lg bg-white/80 backdrop-blur-sm">
                        <CardHeader>
                            <CardTitle className="flex items-center gap-2 text-slate-900">
                                <GraduationCap className="w-5 h-5 text-blue-600" />
                                Informacje akademickie
                            </CardTitle>
                        </CardHeader>
                        <CardContent className="space-y-4">
                            {user.study_program && (
                                <div>
                                    <div className="flex items-center gap-2 mb-1">
                                        <BookOpen className="w-4 h-4 text-slate-500" />
                                        <span className="text-sm font-medium text-slate-700">Kierunek studiów</span>
                                    </div>
                                    <p className="text-slate-900 ml-6">{user.study_program}</p>
                                </div>
                            )}
                            
                            {user.year_of_study && (
                                <div>
                                    <div className="flex items-center gap-2 mb-1">
                                        <Calendar className="w-4 h-4 text-slate-500" />
                                        <span className="text-sm font-medium text-slate-700">Rok studiów</span>
                                    </div>
                                    <p className="text-slate-900 ml-6">{user.year_of_study}</p>
                                </div>
                            )}
                            
                            {user.university_id && (
                                <div>
                                    <div className="flex items-center gap-2 mb-1">
                                        <User className="w-4 h-4 text-slate-500" />
                                        <span className="text-sm font-medium text-slate-700">ID Uczelni</span>
                                    </div>
                                    <p className="text-slate-900 ml-6">{user.university_id}</p>
                                </div>
                            )}
                            
                            <Separator />
                            
                            <div>
                                <div className="flex items-center gap-2 mb-1">
                                    <Calendar className="w-4 h-4 text-slate-500" />
                                    <span className="text-sm font-medium text-slate-700">Data dołączenia</span>
                                </div>
                                <p className="text-slate-900 ml-6">{formatDate(user.join_date)}</p>
                            </div>
                        </CardContent>
                    </Card>

                    {/* Achievements */}
                    <Card className="border-0 shadow-lg bg-white/80 backdrop-blur-sm">
                        <CardHeader>
                            <CardTitle className="flex items-center gap-2 text-slate-900">
                                <Award className="w-5 h-5 text-purple-600" />
                                Osiągnięcia
                            </CardTitle>
                        </CardHeader>
                        <CardContent>
                            {user.achievements && user.achievements.length > 0 ? (
                                <div className="space-y-3">
                                    {user.achievements.map((achievement, index) => (
                                        <div key={index} className="flex items-start gap-3 p-3 bg-slate-50 rounded-lg">
                                            <Award className="w-4 h-4 text-yellow-500 mt-0.5 flex-shrink-0" />
                                            <span className="text-slate-900 text-sm">{achievement}</span>
                                        </div>
                                    ))}
                                </div>
                            ) : (
                                <div className="text-center py-8 text-slate-500">
                                    <Award className="w-12 h-12 mx-auto mb-3 text-slate-300" />
                                    <p>Brak osiągnięć do wyświetlenia</p>
                                </div>
                            )}
                        </CardContent>
                    </Card>

                    {/* Activity/Statistics */}
                    <Card className="border-0 shadow-lg bg-white/80 backdrop-blur-sm">
                        <CardHeader>
                            <CardTitle className="flex items-center gap-2 text-slate-900">
                                <User className="w-5 h-5 text-green-600" />
                                Statystyki
                            </CardTitle>
                        </CardHeader>
                        <CardContent className="space-y-4">
                            <div className="bg-gradient-to-r from-blue-50 to-blue-100 p-4 rounded-lg">
                                <div className="text-2xl font-bold text-blue-700">ID: {user.id}</div>
                                <div className="text-sm text-blue-600">Identyfikator użytkownika</div>
                            </div>
                            
                            <div className="bg-gradient-to-r from-purple-50 to-purple-100 p-4 rounded-lg">
                                <div className="text-2xl font-bold text-purple-700">
                                    {user.role === 'student' ? 'Student' :
                                     user.role === 'professor' ? 'Profesor' :
                                     user.role === 'lecturer' ? 'Wykładowca' : 'Użytkownik'}
                                </div>
                                <div className="text-sm text-purple-600">Rola w systemie</div>
                            </div>
                        </CardContent>
                    </Card>
                </div>
            </div>
        </div>
    );
}
