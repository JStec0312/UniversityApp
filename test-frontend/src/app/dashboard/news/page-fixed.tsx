"use client";

import { useState, useEffect } from 'react';
import { getPaginatedNews } from '@/api/newsApi';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import { 
    Newspaper, 
    Search, 
    Calendar,
    ChevronLeft,
    ChevronRight,
    Loader2,
    Clock,
    MessageCircle,
    ArrowRight,
    Sparkles
} from 'lucide-react';
import Link from 'next/link';

type News = {
    title: string;
    content: string;
    image_url?: string;
    created_at: string;
    id: number;
}

export default function NewsPage() {
    const [news, setNews] = useState<News[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [searchTerm, setSearchTerm] = useState("");
    const [currentPage, setCurrentPage] = useState(1);
    const [hasNextPage, setHasNextPage] = useState(false);
    const limit = 6;

    const fetchNews = async (page: number) => {
        try {
            setLoading(true);
            const response = await getPaginatedNews(page, limit);
            setNews(response);
            setHasNextPage(response.hasNextPage || false);
            setError(null);
        } catch (err) {
            console.error("Error fetching news:", err);
            setError("Failed to load news. Please try again.");
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchNews(currentPage);
    }, [currentPage]);

    const filteredNews = news.filter(item =>
        item.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
        item.content.toLowerCase().includes(searchTerm.toLowerCase())
    );

    const handlePreviousPage = () => {
        if (currentPage > 1) {
            setCurrentPage(prev => prev - 1);
        }
    };

    const handleNextPage = () => {
        if (hasNextPage) {
            setCurrentPage(prev => prev + 1);
        }
    };

    const formatDate = (dateString: string) => {
        return new Date(dateString).toLocaleDateString('pl-PL', {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        });
    };

    const getTimeAgo = (dateString: string) => {
        const now = new Date();
        const date = new Date(dateString);
        const diffInHours = Math.floor((now.getTime() - date.getTime()) / (1000 * 60 * 60));
        
        if (diffInHours < 1) return "Przed chwilą";
        if (diffInHours < 24) return `${diffInHours}h temu`;
        const diffInDays = Math.floor(diffInHours / 24);
        if (diffInDays < 7) return `${diffInDays} dni temu`;
        return formatDate(dateString);
    };

    return (
        <div className="space-y-8">
            {/* Header */}
            <div className="text-center space-y-4">
                <div className="inline-flex items-center space-x-2 bg-white/80 backdrop-blur-sm rounded-full px-6 py-2 shadow-lg border border-white/20">
                    <Newspaper className="w-5 h-5 text-blue-600" />
                    <span className="text-sm font-medium text-gray-700">Ogłoszenia</span>
                </div>
                <h1 className="text-4xl md:text-5xl font-bold bg-gradient-to-r from-blue-600 via-purple-600 to-indigo-600 bg-clip-text text-transparent">
                    Najnowsze Ogłoszenia
                </h1>
                <p className="text-xl text-gray-600 max-w-2xl mx-auto">
                    Bądź na bieżąco z najważniejszymi informacjami uniwersyteckimi
                </p>
            </div>

            {/* Search Bar */}
            <Card className="bg-white/70 backdrop-blur-sm border-white/20">
                <CardContent className="p-6">
                    <div className="relative max-w-md mx-auto">
                        <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
                        <Input
                            type="text"
                            placeholder="Szukaj ogłoszeń..."
                            value={searchTerm}
                            onChange={(e) => setSearchTerm(e.target.value)}
                            className="pl-10 bg-white/90 backdrop-blur-sm border-white/20"
                        />
                    </div>
                    {searchTerm && (
                        <div className="flex justify-center mt-4">
                            <Badge variant="secondary" className="bg-blue-50 text-blue-700 border-blue-200">
                                <Sparkles className="w-3 h-3 mr-1" />
                                Znaleziono {filteredNews.length} ogłoszeń dla "{searchTerm}"
                            </Badge>
                        </div>
                    )}
                </CardContent>
            </Card>

            {/* Error State */}
            {error && (
                <Card className="bg-red-50 border-red-200">
                    <CardContent className="p-6 text-center">
                        <div className="text-red-600 mb-4">
                            <MessageCircle className="w-12 h-12 mx-auto mb-2" />
                            <p className="font-semibold">Błąd ładowania</p>
                            <p className="text-sm">{error}</p>
                        </div>
                        <Button onClick={() => fetchNews(currentPage)} variant="outline">
                            Spróbuj ponownie
                        </Button>
                    </CardContent>
                </Card>
            )}

            {/* Loading State */}
            {loading && (
                <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
                    {[...Array(6)].map((_, i) => (
                        <Card key={i} className="bg-white/70 backdrop-blur-sm border-white/20 animate-pulse">
                            <div className="h-48 bg-gray-200 rounded-t-xl"></div>
                            <CardContent className="p-6 space-y-3">
                                <div className="h-4 bg-gray-200 rounded w-3/4"></div>
                                <div className="h-3 bg-gray-200 rounded w-1/2"></div>
                                <div className="h-3 bg-gray-200 rounded w-full"></div>
                            </CardContent>
                        </Card>
                    ))}
                </div>
            )}

            {/* News Grid */}
            {!loading && !error && (
                <>
                    {filteredNews.length > 0 ? (
                        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
                            {filteredNews.map((item) => (
                                <Card 
                                    key={item.id} 
                                    className="group cursor-pointer overflow-hidden bg-white/70 backdrop-blur-sm border-white/20 hover:bg-white/80 hover:shadow-xl transition-all duration-300 hover:scale-[1.02]"
                                >
                                    {/* Image */}
                                    <div className="relative h-48 overflow-hidden">
                                        <img
                                            src={item.image_url || "https://via.placeholder.com/400x200?text=News"}
                                            alt={item.title}
                                            className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-110"
                                        />
                                        <div className="absolute top-4 left-4">
                                            <Badge className="bg-blue-500 text-white border-0 shadow-lg">
                                                Ogłoszenie
                                            </Badge>
                                        </div>
                                    </div>

                                    <CardContent className="p-6 space-y-4">
                                        {/* Title */}
                                        <h3 className="text-xl font-bold text-gray-900 group-hover:text-blue-600 transition-colors line-clamp-2">
                                            {item.title}
                                        </h3>

                                        {/* Content Preview */}
                                        <p className="text-gray-600 text-sm line-clamp-3">
                                            {item.content}
                                        </p>

                                        {/* Date */}
                                        <div className="flex items-center justify-between text-sm text-gray-500">
                                            <div className="flex items-center space-x-2">
                                                <Calendar className="w-4 h-4" />
                                                <span>{formatDate(item.created_at)}</span>
                                            </div>
                                            <div className="flex items-center space-x-2">
                                                <Clock className="w-4 h-4" />
                                                <span>{getTimeAgo(item.created_at)}</span>
                                            </div>
                                        </div>

                                        {/* Read More Button */}
                                        <Link href={`/dashboard/news/${item.id}`}>
                                            <Button 
                                                variant="ghost" 
                                                className="w-full justify-between text-blue-600 hover:text-blue-700 hover:bg-blue-50 group/button"
                                            >
                                                <span>Czytaj więcej</span>
                                                <ArrowRight className="w-4 h-4 transition-transform group-hover/button:translate-x-1" />
                                            </Button>
                                        </Link>
                                    </CardContent>
                                </Card>
                            ))}
                        </div>
                    ) : (
                        <Card className="bg-white/70 backdrop-blur-sm border-white/20">
                            <CardContent className="p-12 text-center">
                                <Newspaper className="w-16 h-16 mx-auto text-gray-400 mb-4" />
                                <h3 className="text-lg font-semibold text-gray-900 mb-2">
                                    Brak ogłoszeń
                                </h3>
                                <p className="text-gray-600">
                                    {searchTerm 
                                        ? "Nie znaleziono ogłoszeń spełniających kryteria" 
                                        : "Obecnie brak dostępnych ogłoszeń"
                                    }
                                </p>
                            </CardContent>
                        </Card>
                    )}
                </>
            )}

            {/* Pagination */}
            {!searchTerm && !loading && !error && (
                <div className="flex justify-center items-center space-x-4">
                    <Button
                        variant="outline"
                        onClick={handlePreviousPage}
                        disabled={currentPage === 1}
                        className="bg-white/70 backdrop-blur-sm border-white/20"
                    >
                        <ChevronLeft className="w-4 h-4 mr-2" />
                        Poprzednia
                    </Button>
                    
                    <Badge variant="secondary" className="bg-blue-50 text-blue-700 border-blue-200 px-4 py-2">
                        Strona {currentPage}
                    </Badge>
                    
                    <Button
                        variant="outline"
                        onClick={handleNextPage}
                        disabled={!hasNextPage}
                        className="bg-white/70 backdrop-blur-sm border-white/20"
                    >
                        Następna
                        <ChevronRight className="w-4 h-4 ml-2" />
                    </Button>
                </div>
            )}
        </div>
    );
}
