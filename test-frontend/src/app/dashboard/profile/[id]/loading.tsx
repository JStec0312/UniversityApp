import { Card, CardContent } from '@/components/ui/card';

export default function Loading() {
    return (
        <div className="min-h-screen bg-gradient-to-br from-blue-50 to-purple-50 p-6">
            <div className="max-w-4xl mx-auto">
                {/* Back button loading */}
                <div className="mb-6">
                    <div className="h-9 w-20 mb-4 bg-slate-200 animate-pulse rounded" />
                </div>

                {/* Profile Header Card Loading */}
                <Card className="mb-6 border-0 shadow-lg bg-white/80 backdrop-blur-sm">
                    <CardContent className="p-8">
                        <div className="flex flex-col md:flex-row items-start md:items-center gap-6">
                            <div className="w-24 h-24 rounded-full bg-slate-200 animate-pulse" />
                            
                            <div className="flex-1 space-y-3">
                                <div className="h-8 w-64 bg-slate-200 animate-pulse rounded" />
                                <div className="h-4 w-96 bg-slate-200 animate-pulse rounded" />
                                <div className="flex flex-wrap gap-4">
                                    <div className="h-4 w-48 bg-slate-200 animate-pulse rounded" />
                                    <div className="h-4 w-32 bg-slate-200 animate-pulse rounded" />
                                    <div className="h-4 w-40 bg-slate-200 animate-pulse rounded" />
                                </div>
                            </div>
                            
                            <div className="flex gap-3">
                                <div className="h-9 w-32 bg-slate-200 animate-pulse rounded" />
                            </div>
                        </div>
                    </CardContent>
                </Card>

                <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                    {/* Academic Information Loading */}
                    <Card className="border-0 shadow-lg bg-white/80 backdrop-blur-sm">
                        <CardContent className="p-6 space-y-4">
                            <div className="h-6 w-48 bg-slate-200 animate-pulse rounded" />
                            <div className="space-y-3">
                                <div className="h-4 w-full bg-slate-200 animate-pulse rounded" />
                                <div className="h-4 w-3/4 bg-slate-200 animate-pulse rounded" />
                                <div className="h-4 w-1/2 bg-slate-200 animate-pulse rounded" />
                            </div>
                        </CardContent>
                    </Card>

                    {/* Achievements Loading */}
                    <Card className="border-0 shadow-lg bg-white/80 backdrop-blur-sm">
                        <CardContent className="p-6 space-y-4">
                            <div className="h-6 w-32 bg-slate-200 animate-pulse rounded" />
                            <div className="space-y-3">
                                <div className="h-16 w-full bg-slate-200 animate-pulse rounded-lg" />
                                <div className="h-16 w-full bg-slate-200 animate-pulse rounded-lg" />
                            </div>
                        </CardContent>
                    </Card>

                    {/* Statistics Loading */}
                    <Card className="border-0 shadow-lg bg-white/80 backdrop-blur-sm">
                        <CardContent className="p-6 space-y-4">
                            <div className="h-6 w-24 bg-slate-200 animate-pulse rounded" />
                            <div className="space-y-3">
                                <div className="h-20 w-full bg-slate-200 animate-pulse rounded-lg" />
                                <div className="h-20 w-full bg-slate-200 animate-pulse rounded-lg" />
                            </div>
                        </CardContent>
                    </Card>
                </div>
            </div>
        </div>
    );
}
