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
    Loader2
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
        return new Date(dateString).toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        });
    };

    return (
        <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                {/* Header */}
                <div className="bg-gradient-to-r from-blue-600 to-purple-600 rounded-2xl p-8 mb-8 text-white">
                    <div className="flex items-center gap-4 mb-4">
                        <div className="bg-white/20 p-3 rounded-xl">
                            <Newspaper className="h-8 w-8" />
                        </div>
                        <div>
                            <h1 className="text-3xl font-bold">University News</h1>
                            <p className="text-blue-100 text-lg">
                                Stay updated with the latest university announcements and news
                            </p>
                        </div>
                    </div>
                </div>

                {/* Search Bar */}
                <div className="flex flex-col sm:flex-row gap-4 mb-8">
                    <div className="relative flex-1">
                        <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-4 w-4" />
                        <Input
                            placeholder="Search news articles..."
                            value={searchTerm}
                            onChange={(e) => setSearchTerm(e.target.value)}
                            className="pl-10 h-12 border-gray-200 focus:border-blue-500 focus:ring-blue-500"
                        />
                    </div>
                    <div className="flex items-center gap-2">
                        <Badge variant="outline" className="bg-blue-50 text-blue-700 border-blue-200">
                            <Calendar className="h-3 w-3 mr-1" />
                            Page {currentPage}
                        </Badge>
                    </div>
                </div>

                {/* Loading State */}
                {loading ? (
                    <Card className="shadow-md">
                        <CardContent className="flex flex-col items-center justify-center py-16">
                            <Loader2 className="h-8 w-8 animate-spin text-blue-600 mb-4" />
                            <p className="text-gray-900 font-medium">Loading latest news...</p>
                            <p className="text-gray-700 text-sm">Please wait while we fetch the articles</p>
                        </CardContent>
                    </Card>
                ) : error ? (
                    <Card className="shadow-md border-red-200">
                        <CardContent className="flex flex-col items-center justify-center py-16 text-center">
                            <div className="text-red-600 mb-4">
                                <Newspaper className="h-12 w-12 mx-auto opacity-50" />
                            </div>
                            <h3 className="text-xl font-semibold text-gray-900 mb-2">Error Loading News</h3>
                            <p className="text-gray-700 mb-6">{error}</p>
                            <Button onClick={() => fetchNews(currentPage)} className="bg-blue-600 hover:bg-blue-700">
                                Try Again
                            </Button>
                        </CardContent>
                    </Card>
                ) : filteredNews.length > 0 ? (
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
                        {filteredNews.map((article) => (
                            <Link key={article.id} href={`/dashboard/news/${article.id}`}>
                                <Card className="cursor-pointer transition-all duration-200 hover:shadow-lg hover:scale-105 border-gray-200 h-full">
                                    {article.image_url && (
                                        <div className="aspect-video overflow-hidden rounded-t-lg">
                                            <img
                                                src={article.image_url}
                                                alt={article.title}
                                                className="w-full h-full object-cover transition-transform duration-200 hover:scale-110"
                                            />
                                        </div>
                                    )}
                                    <CardHeader className="pb-4">
                                        <div className="flex items-start justify-between gap-2">
                                            <CardTitle className="text-lg font-semibold text-gray-900 line-clamp-2">
                                                {article.title}
                                            </CardTitle>
                                        </div>
                                        <div className="flex items-center gap-2 text-sm text-gray-700">
                                            <Calendar className="h-4 w-4" />
                                            <span>{formatDate(article.created_at)}</span>
                                        </div>
                                    </CardHeader>
                                    <CardContent className="pt-0">
                                        <CardDescription className="text-gray-700 font-medium line-clamp-3">
                                            {article.content.length > 150 
                                                ? `${article.content.substring(0, 150)}...` 
                                                : article.content
                                            }
                                        </CardDescription>
                                    </CardContent>
                                </Card>
                            </Link>
                        ))}
                    </div>
                ) : (
                    <Card>
                        <CardContent className="flex flex-col items-center justify-center py-12 text-center">
                            <div className="text-6xl mb-6 opacity-20">
                                {searchTerm ? (
                                    <Search className="h-16 w-16 mx-auto" />
                                ) : (
                                    <Newspaper className="h-16 w-16 mx-auto" />
                                )}
                            </div>
                            <h3 className="text-xl font-semibold mb-4 text-gray-900">
                                {searchTerm
                                    ? `No news found matching "${searchTerm}"`
                                    : "No news articles available"
                                }
                            </h3>
                            <p className="text-gray-700 mb-6">
                                {searchTerm
                                    ? "Try adjusting your search terms or browse all articles"
                                    : "Check back later for new announcements and updates"
                                }
                            </p>
                            {searchTerm && (
                                <Button
                                    onClick={() => setSearchTerm("")}
                                    variant="outline"
                                    className="border-gray-300 hover:bg-gray-50"
                                >
                                    Clear Search
                                </Button>
                            )}
                        </CardContent>
                    </Card>
                )}

                {/* Pagination */}
                {!loading && !error && news.length > 0 && (
                    <div className="flex justify-center items-center gap-4 mt-8">
                        <Button
                            onClick={handlePreviousPage}
                            disabled={currentPage === 1}
                            variant="outline"
                            className="flex items-center gap-2"
                        >
                            <ChevronLeft className="h-4 w-4" />
                            Previous
                        </Button>
                        
                        <div className="flex items-center gap-2 px-4">
                            <span className="text-sm text-gray-700 font-medium">
                                Page {currentPage}
                            </span>
                        </div>
                        
                        <Button
                            onClick={handleNextPage}
                            disabled={!hasNextPage}
                            variant="outline"
                            className="flex items-center gap-2"
                        >
                            Next
                            <ChevronRight className="h-4 w-4" />
                        </Button>
                    </div>
                )}
            </div>
        </div>
    );
}
