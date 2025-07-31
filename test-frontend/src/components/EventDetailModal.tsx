"use client";

import { Event } from "@/types/Event";

interface EventDetailModalProps {
    event: Event;
    isOpen: boolean;
    onClose: () => void;
}

export default function EventDetailModal({ event, isOpen, onClose }: EventDetailModalProps) {
    // Format date string to a more readable format
    const formatDate = (dateString: string) => {
        if (!dateString) return "No date set";
        const options: Intl.DateTimeFormatOptions = { 
            year: 'numeric', 
            month: 'long', 
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        };
        return new Date(dateString).toLocaleDateString(undefined, options);
    };

    if (!isOpen) return null;

    return (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
            <div className="bg-white rounded-lg shadow-xl max-w-3xl w-full max-h-[90vh] overflow-y-auto">
                <div className="relative h-64 sm:h-80">
                    <img 
                        src={event.image_url || "https://via.placeholder.com/800x400?text=No+Image"} 
                        alt={event.title || "Event"}
                        className="w-full h-full object-cover"
                    />
                    <button 
                        onClick={onClose}
                        className="absolute top-4 right-4 bg-black bg-opacity-50 text-white p-2 rounded-full hover:bg-opacity-70"
                    >
                        <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                        </svg>
                    </button>
                </div>
                <div className="p-6">
                    <h2 className="text-2xl font-bold text-gray-800 mb-2">
                        {event.title || "Untitled Event"}
                    </h2>
                    
                    <div className="flex flex-wrap gap-2 mb-4">
                        <span className="bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded-full uppercase font-semibold">
                            Event
                        </span>
                        {event.location && (
                            <span className="bg-green-100 text-green-800 text-xs px-2 py-1 rounded-full uppercase font-semibold">
                                📍 {event.location}
                            </span>
                        )}
                    </div>
                    
                    <div className="border-t border-b border-gray-200 py-4 my-4">
                        <div className="flex items-center mb-2">
                            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 text-gray-500 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                            </svg>
                            <span className="text-gray-700">
                                <strong>Starts:</strong> {formatDate(event.start_date)}
                            </span>
                        </div>
                        {event.end_date && (
                            <div className="flex items-center">
                                <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 text-gray-500 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                                </svg>
                                <span className="text-gray-700">
                                    <strong>Ends:</strong> {formatDate(event.end_date)}
                                </span>
                            </div>
                        )}
                    </div>
                    
                    <div className="prose max-w-none">
                        <h3 className="text-lg font-semibold mb-2">Description</h3>
                        <p className="text-gray-700 whitespace-pre-line">
                            {event.description || "No description provided"}
                        </p>
                    </div>
                    
                    <div className="mt-6 flex justify-end space-x-3">
                        <button 
                            onClick={onClose}
                            className="px-4 py-2 border border-gray-300 rounded-md text-gray-700 bg-white hover:bg-gray-50"
                        >
                            Close
                        </button>
                        <button className="px-4 py-2 border border-transparent rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700">
                            Register for Event
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
}
