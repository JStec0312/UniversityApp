"use client";

import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import { Event } from "@/types/Event";
import { fetchEventById } from "@/api/eventsApi";

export default function EventDetailPage() {
    const params = useParams();
    const router = useRouter();
    const [event, setEvent] = useState<Event | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const fetchEvent = async () => {
            try {
                setLoading(true);
                setError(null);
                
                if (params.id) {
                    const eventData = await fetchEventById(Number(params.id));
                    setEvent(eventData);
                }
            } catch (err) {
                console.error("Error fetching event:", err);
                setError("Failed to load event details");
            } finally {
                setLoading(false);
            }
        };

        fetchEvent();
    }, [params.id]);

    // Format date string to a more readable format
    const formatDate = (dateString: string) => {
        const options: Intl.DateTimeFormatOptions = { 
            year: 'numeric', 
            month: 'long', 
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        };
        return new Date(dateString).toLocaleDateString(undefined, options);
    };

    if (loading) {
        return (
            <div className="min-h-screen bg-gradient-to-br from-gray-50 to-blue-50 flex items-center justify-center">
                <div className="text-center">
                    <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-blue-600 mx-auto mb-4"></div>
                    <p className="text-gray-600 font-medium">Loading event details...</p>
                </div>
            </div>
        );
    }

    if (error || !event) {
        return (
            <div className="min-h-screen bg-gradient-to-br from-gray-50 to-blue-50 flex items-center justify-center">
                <div className="text-center">
                    <div className="text-6xl mb-4">😕</div>
                    <h1 className="text-2xl font-bold text-gray-800 mb-2">Event Not Found</h1>
                    <p className="text-gray-600 mb-6">{error || "The event you're looking for doesn't exist."}</p>
                    <button
                        onClick={() => router.push('/dashboard/events')}
                        className="bg-blue-600 text-white px-6 py-3 rounded-lg font-medium hover:bg-blue-700 transition-colors"
                    >
                        ← Back to Events
                    </button>
                </div>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-gradient-to-br from-gray-50 to-blue-50">
            <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                {/* Back Button */}
                <button
                    onClick={() => router.push('/dashboard/events')}
                    className="mb-6 inline-flex items-center gap-2 text-blue-600 hover:text-blue-800 font-medium transition-colors"
                >
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
                    </svg>
                    Back to Events
                </button>

                {/* Event Detail Card */}
                <div className="bg-white rounded-2xl shadow-xl overflow-hidden">
                    {/* Hero Image */}
                    <div className="relative h-64 sm:h-96">
                        <img 
                            src={event.image_url || "https://via.placeholder.com/1200x600?text=No+Image"} 
                            alt={event.title}
                            className="w-full h-full object-cover"
                        />
                        <div className="absolute inset-0 bg-gradient-to-t from-black/50 to-transparent"></div>
                        <div className="absolute bottom-6 left-6 right-6">
                            <h1 className="text-3xl sm:text-4xl font-bold text-white mb-2">{event.title}</h1>
                            <h2 className="text-xl sm:text-2xl font-semibold text-white mb-4">{event.group_name}</h2>
                            <div className="flex flex-wrap gap-2">
                                <span className="bg-white/20 backdrop-blur-sm text-white text-sm px-3 py-1 rounded-full">
                                    Event
                                </span>
                                {event.location && (
                                    <span className="bg-white/20 backdrop-blur-sm text-white text-sm px-3 py-1 rounded-full">
                                        📍 {event.location}
                                    </span>
                                )}
                            </div>
                        </div>
                    </div>

                    {/* Event Content */}
                    <div className="p-8">
                        {/* Date and Time Information */}
                        <div className="bg-gradient-to-r from-blue-50 to-purple-50 rounded-xl p-6 mb-8">
                            <h2 className="text-xl font-bold text-gray-800 mb-4 flex items-center gap-2">
                                <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                                </svg>
                                Event Schedule
                            </h2>
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                                <div className="bg-white rounded-lg p-4 border border-blue-100">
                                    <h3 className="font-semibold text-gray-700 mb-2">Start Date & Time</h3>
                                    <p className="text-gray-600">{formatDate(event.start_date)}</p>
                                </div>
                                {event.end_date && (
                                    <div className="bg-white rounded-lg p-4 border border-purple-100">
                                        <h3 className="font-semibold text-gray-700 mb-2">End Date & Time</h3>
                                        <p className="text-gray-600">{formatDate(event.end_date)}</p>
                                    </div>
                                )}
                            </div>
                        </div>

                        {/* Description */}
                        <div className="mb-8">
                            <h2 className="text-2xl font-bold text-gray-800 mb-4 flex items-center gap-2">
                                <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                                </svg>
                                About This Event
                            </h2>
                            <div className="bg-gray-50 rounded-xl p-6">
                                <p className="text-gray-700 leading-relaxed whitespace-pre-line">{event.description}</p>
                            </div>
                        </div>

                        {/* Location Information */}
                        {event.location && (
                            <div className="mb-8">
                                <h2 className="text-xl font-bold text-gray-800 mb-4 flex items-center gap-2">
                                    <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                                    </svg>
                                    Location
                                </h2>
                                <div className="bg-blue-50 border border-blue-200 rounded-xl p-4">
                                    <p className="text-blue-800 font-medium">{event.location}</p>
                                </div>
                            </div>
                        )}

                        {/* Action Buttons */}
                        <div className="flex flex-col sm:flex-row gap-4 pt-6 border-t border-gray-200">
                            <button className="flex-1 bg-gradient-to-r from-blue-600 to-purple-600 text-white px-6 py-3 rounded-xl font-semibold hover:from-blue-700 hover:to-purple-700 transition-colors duration-200 flex items-center justify-center gap-2">
                                <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                                </svg>
                                Register for Event
                            </button>
                            <button className="flex-1 bg-gray-100 text-gray-700 px-6 py-3 rounded-xl font-semibold hover:bg-gray-200 transition-colors duration-200 flex items-center justify-center gap-2">
                                <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m0 2.684l6.632 3.316m-6.632-6l6.632-3.316m0 0a3 3 0 105.367-2.684 3 3 0 00-5.367 2.684zm0 9.316a3 3 0 105.367 2.684 3 3 0 00-5.367-2.684z" />
                                </svg>
                                Share Event
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}
