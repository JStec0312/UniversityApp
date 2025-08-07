"use client";

import { Event } from "@/types/Event";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Calendar, MapPin, Users, Clock, ArrowRight, Sparkles } from "lucide-react";

interface EventCardProps {
    event: Event;
    onClick?: () => void;
}

export default function EventCard({ event, onClick }: EventCardProps) {
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
        return new Date(dateString).toLocaleDateString('pl-PL', options);
    };

    const formatTime = (dateString: string) => {
        if (!dateString) return "";
        return new Date(dateString).toLocaleTimeString('pl-PL', { 
            hour: '2-digit', 
            minute: '2-digit' 
        });
    };

    const getEventStatus = () => {
        const now = new Date();
        const eventDate = new Date(event.start_date);
        
        if (eventDate > now) {
            return { label: "Nadchodzące", variant: "default" as const, color: "bg-emerald-500" };
        } else {
            return { label: "Zakończone", variant: "secondary" as const, color: "bg-slate-500" };
        }
    };

    const status = getEventStatus();

    return (
        <div 
            className="group cursor-pointer bg-white rounded-2xl shadow-lg hover:shadow-2xl transition-all duration-300 border border-slate-200 hover:border-blue-300 overflow-hidden"
            onClick={onClick}
        >
            {/* Event Image with overlay */}
            <div className="relative h-56 overflow-hidden">
                <img
                    src={event.image_url || "https://via.placeholder.com/400x250?text=Event+Image"}
                    alt={event.title || "Event"}
                    className="w-full h-full object-cover transition-transform duration-700 group-hover:scale-105"
                />
                {/* Gradient overlay */}
                <div className="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-transparent" />
                
                {/* Status badge */}
                <div className="absolute top-4 left-4">
                    <Badge className={`${status.color} text-white border-0 shadow-lg px-3 py-1`}>
                        <Sparkles className="w-3 h-3 mr-1" />
                        {status.label}
                    </Badge>
                </div>
                
                {/* Group badge */}
                <div className="absolute top-4 right-4">
                    <Badge className="bg-white/90 text-slate-800 border-0 shadow-lg backdrop-blur-sm">
                        <Users className="w-3 h-3 mr-1" />
                        {event.group_name}
                    </Badge>
                </div>

                {/* Title overlay */}
                <div className="absolute bottom-4 left-4 right-4">
                    <h3 className="text-white text-xl font-bold line-clamp-2 mb-2">
                        {event.title || "Untitled Event"}
                    </h3>
                </div>
            </div>

            {/* Content Section */}
            <div className="p-6 space-y-4">
                {/* Description */}
                <p className="text-slate-600 text-sm line-clamp-2 leading-relaxed">
                    {event.description || "No description provided"}
                </p>

                {/* Event Details Grid */}
                <div className="grid grid-cols-2 gap-3">
                    <div className="flex items-center space-x-2 text-slate-600 text-sm">
                        <div className="p-1.5 bg-blue-100 rounded-lg">
                            <Calendar className="w-3.5 h-3.5 text-blue-600" />
                        </div>
                        <div>
                            <div className="font-medium text-slate-800">{new Date(event.start_date).toLocaleDateString('pl-PL', { day: 'numeric', month: 'short' })}</div>
                            <div className="text-xs">{new Date(event.start_date).getFullYear()}</div>
                        </div>
                    </div>
                    
                    {event.start_date && (
                        <div className="flex items-center space-x-2 text-slate-600 text-sm">
                            <div className="p-1.5 bg-emerald-100 rounded-lg">
                                <Clock className="w-3.5 h-3.5 text-emerald-600" />
                            </div>
                            <div>
                                <div className="font-medium text-slate-800">{formatTime(event.start_date)}</div>
                                <div className="text-xs">Godzina</div>
                            </div>
                        </div>
                    )}
                </div>

                {/* Location */}
                {event.location && (
                    <div className="flex items-center space-x-2 p-3 bg-slate-50 rounded-xl border border-slate-200">
                        <MapPin className="w-4 h-4 text-red-500" />
                        <span className="text-slate-700 text-sm font-medium line-clamp-1">{event.location}</span>
                    </div>
                )}

                {/* Action Button */}
                <div className="pt-2">
                    <Button 
                        className="w-full bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white shadow-lg hover:shadow-xl transition-all duration-300 group/button"
                    >
                        <span>Zobacz szczegóły</span>
                        <ArrowRight className="w-4 h-4 ml-2 transition-transform group-hover/button:translate-x-1" />
                    </Button>
                </div>
            </div>
        </div>
    );
}
