"use client";

import { getUpcomingEvents, getPastEvents, getEventsByName, getAllEvents } from "@/api/eventsApi";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { Event } from "@/types/Event";
import EventCard from "@/components/EventCard";
import EventDetailModal from "@/components/EventDetailModal";

export default function EventsPage() {
    const router = useRouter();
    const [events, setEvents] = useState<Event[]>([]);
    const [filteredEvents, setFilteredEvents] = useState<Event[]>([]);
    const [eventsLoading, setEventsLoading] = useState(true);
    const [offset, setOffset] = useState(0);
    const [currentPage, setCurrentPage] = useState(1);
    const [hasMoreEvents, setHasMoreEvents] = useState(true);
    const [viewMode, setViewMode] = useState<'upcoming' | 'past'>('upcoming');
    const [searchTerm, setSearchTerm] = useState("");
    const [selectedEvent, setSelectedEvent] = useState<Event | null>(null);
    const eventsPerPage = 10;
    
    useEffect(() => {
        const fetchEvents = async () => {
            setEventsLoading(true);
            try {
                const fetchedEvents = viewMode === 'upcoming' 
                    ? await getUpcomingEvents(eventsPerPage, offset)
                    : await getPastEvents(eventsPerPage, offset);
                
                setEvents(fetchedEvents);
                setFilteredEvents(fetchedEvents);
                
                // Check if there are more events
                setHasMoreEvents(fetchedEvents.length === eventsPerPage);
            } catch (error) {
                console.error("Error fetching events:", error);
                setHasMoreEvents(false);
            } finally {
                setEventsLoading(false);
            }
        };
        fetchEvents();
    }, [offset, viewMode, eventsPerPage]);

    // Handle search functionality
    useEffect(() => {
        const searchEvents = async () => {
            if (searchTerm.trim()) {
                try {
                    const searchResults = await getEventsByName(searchTerm.trim());
                    // Filter search results by view mode
                    const now = new Date();
                    const filteredResults = searchResults.filter((event: Event) => {
                        const eventDate = new Date(event.start_date);
                        const isUpcoming = eventDate > now;
                        return viewMode === 'upcoming' ? isUpcoming : !isUpcoming;
                    });
                    
                    setFilteredEvents(filteredResults);
                } catch (error) {
                    console.error("Error searching events:", error);
                    setFilteredEvents([]);
                }
            } else {
                // If no search term, use the events from the main fetch
                setFilteredEvents(events);
            }
        };

        // Debounce search to avoid too many API calls
        const timeoutId = setTimeout(() => {
            if (searchTerm.trim()) {
                searchEvents();
            } else {
                setFilteredEvents(events);
            }
        }, 300);

        return () => clearTimeout(timeoutId);
    }, [searchTerm, events, viewMode]);

    // Function to switch between view modes
    const switchViewMode = (mode: 'upcoming' | 'past') => {
        setViewMode(mode);
        setOffset(0);
        setCurrentPage(1);
        setHasMoreEvents(true);
        setSearchTerm(""); // Clear search when switching modes
    };

    // Navigation functions
    const goToNextPage = () => {
        if (hasMoreEvents) {
            const newOffset = offset + eventsPerPage;
            setOffset(newOffset);
            setCurrentPage(currentPage + 1);
        }
    };

    const goToPreviousPage = () => {
        if (offset > 0) {
            const newOffset = Math.max(0, offset - eventsPerPage);
            setOffset(newOffset);
            setCurrentPage(Math.max(1, currentPage - 1));
        }
    };

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

    return (
        <div className="min-h-screen bg-gradient-to-br from-gray-50 to-blue-50">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                {/* Enhanced Header */}
                <div className="bg-gradient-to-r from-blue-600 via-purple-600 to-indigo-700 rounded-2xl shadow-xl p-8 mb-8 relative overflow-hidden">
                    <div className="absolute inset-0 bg-white/5 backdrop-blur-sm"></div>
                    <div className="absolute top-0 left-0 w-full h-full opacity-10">
                        <div className="absolute top-4 left-4 w-32 h-32 bg-white rounded-full mix-blend-overlay"></div>
                        <div className="absolute bottom-4 right-4 w-24 h-24 bg-white rounded-full mix-blend-overlay"></div>
                    </div>
                    
                    <div className="relative flex flex-col md:flex-row justify-between items-start md:items-center gap-6">
                        <div className="flex-1">
                            <h1 className="text-4xl md:text-5xl font-bold text-white mb-3 tracking-tight">
                                {viewMode === 'upcoming' ? '🎯 Upcoming Events' : '📚 Past Events'}
                            </h1>
                            <p className="text-blue-100 text-lg leading-relaxed">
                                {viewMode === 'upcoming' 
                                    ? 'Discover amazing events and expand your university experience' 
                                    : 'Explore the memorable events from our university history'
                                }
                            </p>
                        </div>
                        
                        <div className="flex flex-col sm:flex-row gap-3">
                            <button
                                onClick={() => switchViewMode('upcoming')}
                                className={`px-6 py-3 rounded-xl font-semibold transition-colors duration-200 ${
                                    viewMode === 'upcoming'
                                        ? 'bg-white text-blue-600 shadow-lg ring-2 ring-white/50'
                                        : 'bg-white/20 text-white hover:bg-white/30 backdrop-blur-sm'
                                }`}
                            >
                                ⏰ Upcoming
                            </button>
                            <button
                                onClick={() => switchViewMode('past')}
                                className={`px-6 py-3 rounded-xl font-semibold transition-colors duration-200 ${
                                    viewMode === 'past'
                                        ? 'bg-white text-blue-600 shadow-lg ring-2 ring-white/50'
                                        : 'bg-white/20 text-white hover:bg-white/30 backdrop-blur-sm'
                                }`}
                            >
                                📖 Past
                            </button>
                        </div>
                    </div>
                </div>

                {/* Enhanced Search Bar */}
                <div className="bg-white/80 backdrop-blur-lg rounded-2xl shadow-lg border border-white/20 p-6 mb-8">
                    <div className="flex flex-col sm:flex-row gap-6 items-end">
                        <div className="flex-1 w-full">
                            <label className="flex text-sm font-semibold text-gray-700 mb-3 items-center gap-2">
                                🔍 Search Events
                            </label>
                            <div className="relative group">
                                <input
                                    type="text"
                                    placeholder="Search by event name..."
                                    value={searchTerm}
                                    onChange={(e) => setSearchTerm(e.target.value)}
                                    className="w-full pl-12 pr-4 py-4 border-2 border-gray-200 text-gray-800 rounded-xl focus:ring-4 focus:ring-blue-500/20 focus:border-blue-500 transition-colors duration-200 bg-white/90 backdrop-blur-sm"
                                />
                                <div className="absolute left-4 top-1/2 transform -translate-y-1/2">
                                    <svg className="h-5 w-5 text-gray-400 group-focus-within:text-blue-500 transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                                    </svg>
                                </div>
                                {searchTerm && (
                                    <button
                                        onClick={() => setSearchTerm("")}
                                        className="absolute right-4 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600 transition-colors"
                                    >
                                        ✕
                                    </button>
                                )}
                            </div>
                        </div>
                        {searchTerm && (
                            <div className="bg-blue-50 border border-blue-200 rounded-xl px-4 py-3 text-blue-700 font-medium flex items-center gap-2">
                                <span className="text-blue-500">📊</span>
                                Found {filteredEvents.length} events matching "{searchTerm}"
                            </div>
                        )}
                    </div>
                </div>

                {/* Loading State */}
                {eventsLoading ? (
                    <div className="flex justify-center items-center h-64">
                        <div className="animate-pulse flex flex-col items-center">
                            <div className="h-16 w-16 border-4 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
                            <p className="mt-4 text-gray-700 font-medium">Loading events...</p>
                        </div>
                    </div>
                ) : filteredEvents.length > 0 ? (
                    <div className="bg-white/80 backdrop-blur-lg rounded-2xl shadow-lg border border-white/20 overflow-hidden mb-8">
                        <div className="p-6 bg-gradient-to-r from-blue-50 to-purple-50 border-b border-gray-100">
                            <h2 className="text-xl font-bold text-gray-800 flex items-center gap-3">
                                <span className="w-2 h-8 bg-gradient-to-b from-blue-500 to-purple-500 rounded-full"></span>
                                {viewMode === 'upcoming' ? 'Upcoming Events' : 'Past Events'}
                                <span className="ml-auto bg-blue-100 text-blue-700 px-3 py-1 rounded-full text-sm font-semibold">
                                    {filteredEvents.length} events
                                </span>
                            </h2>
                        </div>
                        <div className="p-6">
                            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                                {filteredEvents.map((event) => (
                                    <EventCard 
                                        onClick={() => setSelectedEvent(event)} 
                                        key={event.id} 
                                        event={event} 
                                    />
                                ))}
                            </div>
                        </div>
                    </div>
                ) : (
                    <div className="bg-white/80 backdrop-blur-lg rounded-2xl shadow-lg border border-white/20 p-12 text-center mb-8">
                        <div className="text-8xl mb-6 opacity-20">
                            {searchTerm ? '🔍' : '📭'}
                        </div>
                        <h3 className="text-2xl font-bold text-gray-600 mb-4">
                            {searchTerm 
                                ? `No events found matching "${searchTerm}"` 
                                : `No ${viewMode} events available`
                            }
                        </h3>
                        <p className="text-gray-500 mb-6">
                            {searchTerm 
                                ? "Try adjusting your search terms or browse all events" 
                                : `Check back later for new ${viewMode} events`
                            }
                        </p>
                        {searchTerm && (
                            <button
                                onClick={() => setSearchTerm("")}
                                className="bg-gradient-to-r from-blue-500 to-purple-600 text-white px-6 py-3 rounded-lg font-semibold hover:from-blue-600 hover:to-purple-700 transition-colors duration-200"
                            >
                                Clear Search
                            </button>
                        )}
                    </div>
                )}

                {/* Pagination - Only show when not searching */}
                {!searchTerm && filteredEvents.length > 0 && (
                    <div className="bg-white/80 backdrop-blur-lg rounded-2xl shadow-lg border border-white/20 p-6">
                        <div className="flex justify-between items-center">
                            <div className="text-sm text-gray-600 bg-gray-50 px-4 py-2 rounded-lg">
                                Page {currentPage}
                            </div>
                            <div className="flex items-center space-x-3">
                                <button
                                    onClick={goToPreviousPage}
                                    disabled={offset === 0}
                                    className={`flex items-center gap-2 px-6 py-3 rounded-xl font-semibold transition-colors duration-200 ${
                                        offset === 0
                                            ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
                                            : 'bg-gradient-to-r from-blue-500 to-purple-600 text-white hover:from-blue-600 hover:to-purple-700 shadow-md'
                                    }`}
                                >
                                    ← Previous
                                </button>
                                <button
                                    onClick={goToNextPage}
                                    disabled={!hasMoreEvents || filteredEvents.length === 0}
                                    className={`flex items-center gap-2 px-6 py-3 rounded-xl font-semibold transition-colors duration-200 ${
                                        !hasMoreEvents || filteredEvents.length === 0
                                            ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
                                            : 'bg-gradient-to-r from-blue-500 to-purple-600 text-white hover:from-blue-600 hover:to-purple-700 shadow-md'
                                    }`}
                                >
                                    Next →
                                </button>
                            </div>
                        </div>
                    </div>
                )}
            </div>

            {/* Event Detail Modal */}
            {selectedEvent && (
                <EventDetailModal 
                    event={selectedEvent} 
                    isOpen={!!selectedEvent}
                    onClose={() => setSelectedEvent(null)}
                />
            )}
        </div>
    );

}
