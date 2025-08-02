"use client";

import { useState, useEffect } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { getNewsById } from '@/api/newsApi';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { 
    ArrowLeft, 
    Calendar,
    Newspaper,
    Loader2,
    AlertCircle
} from 'lucide-react';

type News = {
    title: string;
    content: string;
    image_url?: string;
    created_at: string;
    id: number;
}

export default function NewsDetailPage() {
    const params = useParams();
    const router = useRouter();
    const [news, setNews] = useState<News | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const fetchNews = async () => {
            try {
                setLoading(true);
                const newsData = await getNewsById(params.id as string);
                setNews(newsData);
                setError(null);
            } catch (err) {
                console.error("Error fetching news:", err);
                setError("Failed to load news article. Please try again.");
            } finally {
                setLoading(false);
            }
        };

        if (params.id) {
            fetchNews();
        }
    }, [params.id]);

    const formatDate = (dateString: string) => {
        return new Date(dateString).toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'long',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
    };

    if (loading) {
        return (
            <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
                <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                    <Card className="shadow-md">
                        <CardContent className="flex flex-col items-center justify-center py-16">
                            <Loader2 className="h-8 w-8 animate-spin text-blue-600 mb-4" />
                            <p className="text-gray-900 font-medium">Loading article...</p>
                            <p className="text-gray-700 text-sm">Please wait while we fetch the details</p>
                        </CardContent>
                    </Card>
                </div>
            </div>
        );
    }

    if (error || !news) {
        return (
            <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
                <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                    <Card className="shadow-md border-red-200">
                        <CardContent className="flex flex-col items-center justify-center py-16 text-center">
                            <AlertCircle className="h-12 w-12 text-red-600 mb-4" />
                            <h3 className="text-xl font-semibold text-gray-900 mb-2">Article Not Found</h3>
                            <p className="text-gray-700 mb-6">{error || "The requested news article could not be found."}</p>
                            <div className="flex gap-3">
                                <Button onClick={() => router.back()} variant="outline">
                                    <ArrowLeft className="h-4 w-4 mr-2" />
                                    Go Back
                                </Button>
                                <Button onClick={() => router.push('/dashboard/news')} className="bg-blue-600 hover:bg-blue-700">
                                    Browse News
                                </Button>
                            </div>
                        </CardContent>
                    </Card>
                </div>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
            <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                {/* Back Button */}
                <div className="mb-6">
                    <Button 
                        onClick={() => router.push('/dashboard/news')} 
                        variant="outline" 
                        className="flex items-center gap-2 hover:bg-blue-50"
                    >
                        <ArrowLeft className="h-4 w-4" />
                        Back to News
                    </Button>
                </div>

                {/* Article Card */}
                <Card className="shadow-lg border-0 overflow-hidden">
                    {/* Hero Image */}
                    {news.image_url && (
                        <div className="aspect-video lg:aspect-[21/9] overflow-hidden">
                            <img
                                src={news.image_url}
                                alt={news.title}
                                className="w-full h-full object-cover"
                            />
                        </div>
                    )}

                    {/* Article Header */}
                    <CardHeader className="bg-gradient-to-r from-blue-600 to-purple-600 text-white">
                        <div className="flex items-center gap-3 mb-4">
                            <div className="bg-white/20 p-2 rounded-lg">
                                <Newspaper className="h-5 w-5" />
                            </div>
                            <Badge variant="secondary" className="bg-white/20 text-white border-white/30">
                                University News
                            </Badge>
                        </div>
                        <CardTitle className="text-2xl lg:text-3xl font-bold leading-tight mb-4">
                            {news.title}
                        </CardTitle>
                        <div className="flex items-center gap-2 text-blue-100">
                            <Calendar className="h-4 w-4" />
                            <span>Published on {formatDate(news.created_at)}</span>
                        </div>
                    </CardHeader>

                    {/* Article Content */}
                    <CardContent className="prose prose-lg max-w-none p-8">
                        <div className="text-gray-900 leading-relaxed whitespace-pre-wrap">
                            {news.content}
                        </div>
                    </CardContent>

                    {/* Article Footer */}
                    <div className="border-t border-gray-200 p-6 bg-gray-50">
                        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
                            <div className="text-sm text-gray-700">
                                <p className="font-medium">University Communications</p>
                                <p>Stay informed with the latest university updates</p>
                            </div>
                            <div className="flex gap-3">
                                <Button 
                                    onClick={() => router.back()} 
                                    variant="outline"
                                    className="border-gray-300 hover:bg-gray-100"
                                >
                                    <ArrowLeft className="h-4 w-4 mr-2" />
                                    Previous Page
                                </Button>
                                <Button 
                                    onClick={() => router.push('/dashboard/news')} 
                                    className="bg-blue-600 hover:bg-blue-700"
                                >
                                    More News
                                </Button>
                            </div>
                        </div>
                    </div>
                </Card>
            </div>
        </div>
    );
}
