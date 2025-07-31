"use client";
import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { getAllEvents, getUpcomingEvents, getPastEvents, getEventsByName } from '@/api/eventsApi';
import EditEventModal from '@/components/EditEventModal.jsx';
import DeleteConfirmationModal from '@/components/DeleteConfirmationEventModal.jsx';
import { Event } from '@/types/Event';
import { Eye} from 'lucide-react';
import Link from 'next/link';
export default function EditEventPageView() {
    const router = useRouter();
    const [events, setEvents] = useState<Event[]>([]);
    const [filteredEvents, setFilteredEvents] = useState<Event[]>([]);
    const [loading, setLoading] = useState(true);
    const [searchTerm, setSearchTerm] = useState("");
    const [filterType, setFilterType] = useState("all"); // "all", "upcoming", "past"
    const [selectedEvent, setSelectedEvent] = useState<Event | null>(null);
    const [showEditModal, setShowEditModal] = useState(false);
    const [showDeleteModal, setShowDeleteModal] = useState(false);
    const [eventToDelete, setEventToDelete] = useState(null);
    const [currentPage, setCurrentPage] = useState(1);
    const [totalEvents, setTotalEvents] = useState(0);
    const [hasMoreEvents, setHasMoreEvents] = useState(true);
    const eventsPerPage = 10;
    const date = new Date();
    const warsawTime = new Intl.DateTimeFormat('pl-PL', {
        timeZone: 'Europe/Warsaw',
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
        }).format(date);
    useEffect(() => {
        const fetchEvents = async () => {
            setLoading(true);
            try {
                const offset = (currentPage - 1) * eventsPerPage;
                let fetchedEvents;

                // Use appropriate API call based on filter type
                if (filterType === "upcoming") {
                    fetchedEvents = await getUpcomingEvents(eventsPerPage, offset);
                } else if (filterType === "past") {
                    fetchedEvents = await getPastEvents(eventsPerPage, offset);
                } else {
                    fetchedEvents = await getAllEvents(eventsPerPage, offset);
                }

                setEvents(fetchedEvents);
                setFilteredEvents(fetchedEvents);
                
                // Check if there are more events
                setHasMoreEvents(fetchedEvents.length === eventsPerPage);
                
                // If this is the first page, get total count (approximate)
                if (currentPage === 1) {
                    setTotalEvents(fetchedEvents.length);
                }
            } catch (error) {
                console.error("Error fetching events:", error);
            } finally {
                setLoading(false);
            }
        };

        fetchEvents();
    }, [currentPage, filterType]);

    // Handle search functionality
    useEffect(() => {
        const searchEvents = async () => {
            if (searchTerm.trim()) {
                try {
                    const searchResults = await getEventsByName(searchTerm.trim());
                    // Filter search results by type if a filter is applied
                    let filteredResults = searchResults;
                    
                    if (filterType !== "all") {
                        const now = new Date();
                        filteredResults = searchResults.filter(event => {
                            const eventDate = new Date(event.start_date);
                            const isUpcoming = eventDate > now;
                            return filterType === "upcoming" ? isUpcoming : !isUpcoming;
                        });
                    }
                    
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
    }, [searchTerm, events, filterType]);

    // Reset to first page when search term or filter changes
    useEffect(() => {
        setCurrentPage(1);
    }, [searchTerm, filterType]);

    // Pagination functions
    const goToNextPage = () => {
        if (hasMoreEvents) {
            setCurrentPage(currentPage + 1);
        }
    };

    const goToPreviousPage = () => {
        if (currentPage > 1) {
            setCurrentPage(currentPage - 1);
        }
    };

    const goToPage = (pageNumber: number) => {
        setCurrentPage(pageNumber);
    };

    // Calculate total pages (approximate)
    const totalPages = Math.ceil(totalEvents / eventsPerPage);

    const handleEditEvent = (event) => {
        setSelectedEvent(event);
        setShowEditModal(true);
    };

    const handleDeleteEvent = (event) => {
        setEventToDelete(event);
        setShowDeleteModal(true);
    };

    const confirmDelete = () => {
        if (eventToDelete) {
            setEvents(events.filter(event => event.id !== eventToDelete.id));
            setShowDeleteModal(false);
            setEventToDelete(null);
        }
    };

    const handleSaveEvent = (updatedEvent) => {
        setEvents(events.map(event => 
            event.id === updatedEvent.id ? updatedEvent : event
        ));
        setShowEditModal(false);
        setSelectedEvent(null);
    };

    const formatDate = (dateString: string) => {
        const options: Intl.DateTimeFormatOptions = { 
            year: 'numeric', 
            month: 'short', 
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        };
        return new Date(dateString).toLocaleDateString(undefined, options);
    };

    if (loading) {
        return (
            <div className="flex justify-center items-center min-h-screen">
                <div className="animate-pulse flex flex-col items-center">
                    <div className="h-16 w-16 border-4 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
                    <p className="mt-4 text-gray-700 font-medium">Loading events...</p>
                </div>
            </div>
        );
    }

    return (
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
            {/* Header */}
            <div className="bg-gradient-to-r from-blue-600 to-indigo-700 rounded-lg shadow-lg p-6 mb-8">
                <h1 className="text-3xl font-bold text-white">Manage Events</h1>
                <p className="text-blue-100 mt-2">Search, edit, and manage all university events</p>
            </div>

            {/* Search and Filter Controls */}
            <div className="bg-white rounded-lg shadow-md p-6 mb-6">
                <div className="flex flex-col md:flex-row gap-4">
                    {/* Search Bar */}
                    <div className="flex-1">
                        <label className="block text-sm font-medium text-black mb-2">Search Events</label>
                        <div className="relative">
                            <input
                                type="text"
                                placeholder="Search by title, description, location, or group..."
                                value={searchTerm}
                                onChange={(e) => setSearchTerm(e.target.value)}
                                className="w-full pl-10 pr-4 py-2 border border-gray-300 text-black rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                            />
                            <svg className="absolute left-3 top-2.5 h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                            </svg>
                        </div>
                    </div>

                    {/* Filter Dropdown */}
                    <div className="md:w-48">
                        <label className="block text-sm font-medium text-gray-700 mb-2">Filter by Type</label>
                        <select
                            value={filterType}
                            onChange={(e) => setFilterType(e.target.value)}
                            className="w-full py-2 px-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent text-black"
                        >
                            <option value="all">All Events</option>
                            <option value="upcoming">Upcoming</option>
                            <option value="past">Past</option>
                        </select>
                    </div>

                    {/* Add New Event Button */}
                    <div className="md:w-48">
                        <label className="block text-sm font-medium text-gray-700 mb-2">&nbsp;</label>
                        <button
                            onClick={() => router.push('/admin-dashboard/add-event')}
                            className="w-full bg-green-600 text-white py-2 px-4 rounded-md hover:bg-green-700 transition-colors"
                        >
                            + Add New Event
                        </button>
                    </div>
                </div>

                {/* Results Count */}
                <div className="mt-4 text-sm text-gray-600">
                    {searchTerm ? (
                        <>
                            Found {filteredEvents.length} events matching "{searchTerm}"
                            {filterType !== "all" && ` (${filterType} only)`}
                        </>
                    ) : (
                        <>
                            Page {currentPage} - Showing {filteredEvents.length} {filterType !== "all" ? filterType : ""} events
                        </>
                    )}
                </div>
            </div>

            {/* Events List */}
            <div className="bg-white rounded-lg shadow-md overflow-hidden">
                {filteredEvents.length === 0 ? (
                    <div className="p-8 text-center">
                        <svg className="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                        </svg>
                        <h3 className="mt-4 text-lg font-medium text-gray-900">No events found</h3>
                        <p className="mt-1 text-gray-500">Try adjusting your search or filter criteria.</p>
                    </div>
                ) : (
                    <div className="overflow-x-auto">
                        <table className="min-w-full divide-y divide-gray-200">
                            <thead className="bg-gray-50">
                                <tr>
                                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Event</th>
                                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Date & Time</th>
                                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Location</th>
                                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Group</th>
                                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
                                </tr>
                            </thead>
                            <tbody className="bg-white divide-y divide-gray-200">
                                {filteredEvents.map((event, index) => {
                                    const eventStatus = new Date(event.start_date) > new Date() ? 'upcoming' : 'past';
                                    return (
                                        <tr key={index} className="hover:bg-gray-50">
                                            <td className='px-6 py-4 whitespace-nowrap text-sm text-gray-500'>
                                                <Link href={`/dashboard/events/${event.id}`}><Eye /></Link>
                                            </td>
                                            <td className="px-6 py-4 whitespace-nowrap">
                                                <div>
                                                    <div className="text-sm font-medium text-gray-900">{event.title}</div>
                                                    <div className="text-sm text-gray-500">{event.description.substring(0, 50)}...</div>
                                                </div>
                                            </td>
                                            <td className="px-6 py-4 whitespace-nowrap">
                                                <div className="text-sm text-gray-900">{formatDate(event.start_date)}</div>
                                                <div className="text-sm text-gray-500">to {formatDate(event.end_date)}</div>
                                            </td>
                                            <td className="px-6 py-4 whitespace-nowrap">
                                                <div className="text-sm text-gray-900">{event.location}</div>
                                            </td>
                                            <td className="px-6 py-4 whitespace-nowrap">
                                                <div className="text-sm text-gray-900">{event.group_name}</div>
                                            </td>
                                            <td className="px-6 py-4 whitespace-nowrap">
                                                <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                                                    eventStatus === 'upcoming' 
                                                        ? 'bg-green-100 text-green-800'
                                                        : 'bg-gray-100 text-gray-800'
                                                }`}>
                                                    {eventStatus === 'upcoming' ? 'Upcoming' : 'Past'}
                                                </span>
                                            </td>
                                            <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                                                <div className="flex space-x-2">
                                                    <button
                                                        onClick={() => handleEditEvent(event)}
                                                        className="text-blue-600 hover:text-blue-900"
                                                    >
                                                        Edit
                                                    </button>
                                                    <button
                                                        onClick={() => handleDeleteEvent(event)}
                                                        className="text-red-600 hover:text-red-900"
                                                    >
                                                        Delete
                                                    </button>
                                                </div>
                                            </td>
                                        </tr>
                                    );
                                })}
                            </tbody>
                        </table>
                    </div>
                )}
                
                {/* Pagination Controls - Only show when not searching */}
                {!searchTerm && filteredEvents.length > 0 && (
                    <div className="bg-white px-4 py-3 border-t border-gray-200 sm:px-6">
                        <div className="flex items-center justify-between">
                            <div className="flex-1 flex justify-between sm:hidden">
                                {/* Mobile pagination */}
                                <button
                                    onClick={goToPreviousPage}
                                    disabled={currentPage === 1}
                                    className={`relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md ${
                                        currentPage === 1
                                            ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
                                            : 'bg-white text-gray-700 hover:bg-gray-50'
                                    }`}
                                >
                                    Previous
                                </button>
                                <button
                                    onClick={goToNextPage}
                                    disabled={!hasMoreEvents}
                                    className={`ml-3 relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md ${
                                        !hasMoreEvents
                                            ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
                                            : 'bg-white text-gray-700 hover:bg-gray-50'
                                    }`}
                                >
                                    Next
                                </button>
                            </div>
                            <div className="hidden sm:flex-1 sm:flex sm:items-center sm:justify-between">
                                <div>
                                    <p className="text-sm text-gray-700">
                                        Showing page <span className="font-medium">{currentPage}</span>
                                        {filterType !== "all" && ` of ${filterType} events`}
                                    </p>
                                </div>
                                <div>
                                    <nav className="relative z-0 inline-flex rounded-md shadow-sm -space-x-px" aria-label="Pagination">
                                        <button
                                            onClick={goToPreviousPage}
                                            disabled={currentPage === 1}
                                            className={`relative inline-flex items-center px-2 py-2 rounded-l-md border border-gray-300 text-sm font-medium ${
                                                currentPage === 1
                                                    ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
                                                    : 'bg-white text-gray-500 hover:bg-gray-50'
                                            }`}
                                        >
                                            <span className="sr-only">Previous</span>
                                            &#8592;
                                        </button>

                                        {/* Current Page Display */}
                                        <span className="relative inline-flex items-center px-4 py-2 border border-gray-300 bg-white text-sm font-medium text-gray-700">
                                            {currentPage}
                                        </span>

                                        <button
                                            onClick={goToNextPage}
                                            disabled={!hasMoreEvents}
                                            className={`relative inline-flex items-center px-2 py-2 rounded-r-md border border-gray-300 text-sm font-medium ${
                                                !hasMoreEvents
                                                    ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
                                                    : 'bg-white text-gray-500 hover:bg-gray-50'
                                            }`}
                                        >
                                            <span className="sr-only">Next</span>
                                            &#8594;
                                        </button>
                                    </nav>
                                </div>
                            </div>
                        </div>
                    </div>
                )}
            </div>

            {/* Edit Modal */}
            {showEditModal && selectedEvent && (
                <EditEventModal 
                    event={selectedEvent}
                    onSave={handleSaveEvent}
                    onClose={() => {
                        setShowEditModal(false);
                        setSelectedEvent(null);
                    }}
                />
            )}

            {/* Delete Confirmation Modal */}
            {showDeleteModal && eventToDelete && (
                <DeleteConfirmationModal
                    event={eventToDelete}
                    onConfirm={confirmDelete}
                    onCancel={() => {
                        setShowDeleteModal(false);
                        setEventToDelete(null);
                    }}
                />
            )}
        </div>
    );
}

// Edit Event Modal Component


// Delete Confirmation Modal Component
