"use client";

import { getUpcomingEvents } from "@/api/eventsApi";
import { useEffect, useState } from "react";
import { Event } from "@/types/Event";
import EventWindow from "@/components/EventWindow.tsx";
import EventWindowDetailed from "@/components/EventWindowDetailed.tsx";
export default function EventsPage() {
    const [events, setEvents] = useState<Event[]>([]);
    const [eventsLoading, setEventsLoading] = useState(true);
    const [selectedEvent, setSelectedEvent] = useState<Event | null>(null);
    
    useEffect(() => {
        const fetchEvents = async () => {
            try {
                const events = await getUpcomingEvents();
                setEvents(events);
            } catch (error) {
                console.error("Error fetching events:", error);
            } finally {
                setEventsLoading(false);
            }
        };
        fetchEvents();
    }, []);

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
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
            <div className="bg-gradient-to-r from-blue-600 to-indigo-700 rounded-lg shadow-lg p-6 mb-8">
                <h1 className="text-3xl font-bold text-white">Upcoming Events</h1>
                <p className="text-blue-100 mt-2">Discover and participate in the latest university events</p>
            </div>

            {eventsLoading ? (
                <div className="flex justify-center items-center h-64">
                    <div className="animate-pulse flex flex-col items-center">
                        <div className="h-16 w-16 border-4 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
                        <p className="mt-4 text-gray-700 font-medium">Loading events...</p>
                    </div>
                </div>
            ) : events.length > 0 ? (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    {events.map((event) => (
                        <EventWindow onClick={() => setSelectedEvent(event)} key={event.id} event={event} />
                    ))}
                </div>
            ) : (
                <div className="bg-gray-50 border border-gray-200 rounded-lg p-8 text-center">
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-12 w-12 mx-auto text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                    </svg>
                    <h3 className="mt-4 text-lg font-medium text-gray-900">No upcoming events</h3>
                    <p className="mt-1 text-gray-500">Check back later for new events and activities.</p>
                </div>
            )}

            {/* Event Detail Modal */}
            {selectedEvent && (
                <EventWindowDetailed 
                    event={selectedEvent} 
                    onClick={() => setSelectedEvent(null)} 
                />
            )}
        </div>
    );

}
