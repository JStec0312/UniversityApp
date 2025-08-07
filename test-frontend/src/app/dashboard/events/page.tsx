"use client";

import { getUpcomingEvents, getPastEvents, getEventsByName } from "@/api/eventsApi";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { Event } from "@/types/Event";
import EventCard from "@/components/EventCard";
import Group from "@/types/Group";
import { getGroups } from "@/api/groupsApi";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Badge } from "@/components/ui/badge";
import { 
  Search, 
  Filter, 
  Calendar, 
  Clock, 
  Users, 
  ChevronLeft, 
  ChevronRight,
  Sparkles 
} from "lucide-react";

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
    const [selectedGroup, setSelectedGroup] = useState<string>("");
    const [studentGroups, setStudentGroups] = useState<Group[]>([]);
    
    const eventsPerPage = 9;

    useEffect(() => {
        const fetchGroups = async () => {
            try {
                const groups = await getGroups();
                setStudentGroups(groups);
            } catch (error) {
                console.error("Error fetching groups:", error);
            }
        };
        fetchGroups();
    }, []);

    useEffect(() => {
        const fetchEvents = async () => {
            setEventsLoading(true);
            try {
                const fetchedEvents = viewMode === 'upcoming' 
                    ? await getUpcomingEvents(eventsPerPage, offset)
                    : await getPastEvents(eventsPerPage, offset);
                
                setEvents(fetchedEvents);
                setFilteredEvents(fetchedEvents);
                setHasMoreEvents(fetchedEvents.length === eventsPerPage);
            } catch (error) {
                console.error("Error fetching events:", error);
                setHasMoreEvents(false);
            } finally {
                setEventsLoading(false);
            }
        };
        fetchEvents();
    }, [offset, viewMode]);

    useEffect(() => {
        const searchEvents = async () => {
            if (searchTerm.trim()) {
                try {
                    const searchResults = await getEventsByName(searchTerm.trim());
                    const now = new Date();
                    const filteredResults = searchResults.filter((event: Event) => {
                        const eventDate = new Date(event.start_date);
                        const isUpcoming = eventDate > now;
                        const matchesViewMode = viewMode === 'upcoming' ? isUpcoming : !isUpcoming;
                        const matchesGroup = selectedGroup === "" || event.group_name === selectedGroup;
                        return matchesViewMode && matchesGroup;
                    });
                    
                    setFilteredEvents(filteredResults);
                } catch (error) {
                    console.error("Error searching events:", error);
                    setFilteredEvents([]);
                }
            } else {
                const groupFilteredEvents = selectedGroup === "" 
                    ? events 
                    : events.filter(event => event.group_name === selectedGroup);
                setFilteredEvents(groupFilteredEvents);
            }
        };

        const timeoutId = setTimeout(searchEvents, 300);
        return () => clearTimeout(timeoutId);
    }, [searchTerm, events, viewMode, selectedGroup]);

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

    const handleEventClick = (eventId?: number) => {
        if (eventId) {
            router.push(`/dashboard/events/${eventId}`);
        }
    };

    return (
        <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
            {/* Compact Header Bar */}
            <div className="bg-white shadow-sm border-b border-slate-200">
                <div className="max-w-7xl mx-auto px-6 py-6">
                    <div className="flex items-center justify-between">
                        <div className="flex items-center space-x-4">
                            <div className="w-12 h-12 bg-gradient-to-r from-blue-500 to-purple-600 rounded-xl flex items-center justify-center shadow-lg">
                                <Calendar className="w-6 h-6 text-white" />
                            </div>
                            <div>
                                <h1 className="text-2xl font-bold text-slate-900">Wydarzenia</h1>
                                <p className="text-slate-600 text-sm">Zarządzaj swoimi wydarzeniami</p>
                            </div>
                        </div>
                        <div className="hidden md:flex items-center space-x-3">
                            <div className="bg-blue-50 px-4 py-2 rounded-lg border border-blue-200">
                                <span className="text-blue-700 font-semibold text-sm">15 aktywnych</span>
                            </div>
                            <div className="bg-purple-50 px-4 py-2 rounded-lg border border-purple-200">
                                <span className="text-purple-700 font-semibold text-sm">3 w tym tygodniu</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            {/* Main Content Area */}
            <div className="max-w-7xl mx-auto px-6 py-6">
                <div className="grid lg:grid-cols-4 gap-6">
                    {/* Sidebar Filters */}
                    <div className="lg:col-span-1">
                        <div className="space-y-6">
                            {/* View Mode Card */}
                            <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
                                <h3 className="font-semibold text-slate-900 mb-4">Typ wydarzeń</h3>
                                <div className="space-y-2">
                                    <button
                                        onClick={() => {
                                            setViewMode('upcoming');
                                            setOffset(0);
                                            setCurrentPage(1);
                                            setSearchTerm("");
                                            setSelectedGroup("");
                                        }}
                                        className={`w-full text-left px-4 py-3 rounded-lg transition-all duration-200 ${
                                            viewMode === 'upcoming'
                                                ? 'bg-gradient-to-r from-blue-500 to-purple-600 text-white shadow-md'
                                                : 'bg-slate-50 text-slate-700 hover:bg-slate-100'
                                        }`}
                                    >
                                        <div className="flex items-center space-x-3">
                                            <Clock className="w-5 h-5" />
                                            <div>
                                                <div className="font-medium">Nadchodzące</div>
                                                <div className={`text-xs ${viewMode === 'upcoming' ? 'text-blue-100' : 'text-slate-500'}`}>
                                                    Przyszłe wydarzenia
                                                </div>
                                            </div>
                                        </div>
                                    </button>
                                    <button
                                        onClick={() => {
                                            setViewMode('past');
                                            setOffset(0);
                                            setCurrentPage(1);
                                            setSearchTerm("");
                                            setSelectedGroup("");
                                        }}
                                        className={`w-full text-left px-4 py-3 rounded-lg transition-all duration-200 ${
                                            viewMode === 'past'
                                                ? 'bg-gradient-to-r from-blue-500 to-purple-600 text-white shadow-md'
                                                : 'bg-slate-50 text-slate-700 hover:bg-slate-100'
                                        }`}
                                    >
                                        <div className="flex items-center space-x-3">
                                            <Calendar className="w-5 h-5" />
                                            <div>
                                                <div className="font-medium">Przeszłe</div>
                                                <div className={`text-xs ${viewMode === 'past' ? 'text-blue-100' : 'text-slate-500'}`}>
                                                    Archiwalne wydarzenia
                                                </div>
                                            </div>
                                        </div>
                                    </button>
                                </div>
                            </div>

                            {/* Search Card */}
                            <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
                                <h3 className="font-semibold text-slate-900 mb-4">Wyszukaj</h3>
                                <div className="space-y-4">
                                    <div className="relative">
                                        <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-black" />
                                        <Input
                                            placeholder="Nazwa wydarzenia..."
                                            value={searchTerm}
                                            onChange={(e) => setSearchTerm(e.target.value)}
                                            className="pl-10 border-slate-300 text-black focus:border-blue-500 focus:ring-blue-500"
                                        />
                                    </div>
                                    <Select value={selectedGroup} onValueChange={setSelectedGroup}>
                                        <SelectTrigger className="border-slate-300 text-black focus:border-blue-500 focus:ring-blue-500">
                                            <div className="flex items-center space-x-2">
                                                <Filter className="h-4 w-4 text-slate-400" />
                                                <SelectValue placeholder="Grupa" />
                                            </div>
                                        </SelectTrigger>
                                        <SelectContent className="">
                                            {studentGroups.map((group) => (
                                                <SelectItem key={group.group_id} className="text-black" value={group.group_name}>
                                                    {group.group_name}
                                                </SelectItem>
                                            ))}
                                        </SelectContent>
                                    </Select>
                                </div>
                            </div>

                            {/* Results Info Card */}
                            {(searchTerm || selectedGroup) && (
                                <div className="bg-gradient-to-r from-blue-500 to-purple-600 rounded-xl shadow-sm p-6 text-white">
                                    <div className="flex items-center space-x-2">
                                        <Sparkles className="w-5 h-5" />
                                        <div>
                                            <div className="font-semibold">Wyniki wyszukiwania</div>
                                            <div className="text-blue-100 text-sm">
                                                {filteredEvents.length} wydarzeń
                                                {searchTerm && ` dla "${searchTerm}"`}
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            )}
                        </div>
                    </div>

                    {/* Main Content */}
                    <div className="lg:col-span-3">
                        <div className="space-y-6">
                            {eventsLoading ? (
                                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                                    {[...Array(6)].map((_, i) => (
                                        <div key={i} className="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden animate-pulse">
                                            <div className="h-48 bg-gradient-to-r from-slate-200 to-slate-300"></div>
                                            <div className="p-6 space-y-3">
                                                <div className="h-5 bg-slate-200 rounded w-3/4"></div>
                                                <div className="h-4 bg-slate-200 rounded w-1/2"></div>
                                                <div className="h-8 bg-slate-200 rounded w-full"></div>
                                            </div>
                                        </div>
                                    ))}
                                </div>
                            ) : (
                                <>
                                    {filteredEvents.length > 0 ? (
                                        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                                            {filteredEvents.map((event, index) => (
                                                <EventCard
                                                    key={event.id || index}
                                                    event={event}
                                                    onClick={() => handleEventClick(event.id)}
                                                />
                                            ))}
                                        </div>
                                    ) : (
                                        <div className="text-center py-16">
                                            <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-12 max-w-md mx-auto">
                                                <div className="w-16 h-16 bg-gradient-to-r from-blue-500 to-purple-600 rounded-xl flex items-center justify-center mx-auto mb-6 shadow-lg">
                                                    <Calendar className="w-8 h-8 text-white" />
                                                </div>
                                                <h3 className="text-xl font-bold text-slate-900 mb-3">
                                                    Brak wydarzeń
                                                </h3>
                                                <p className="text-slate-600 mb-6 leading-relaxed">
                                                    {searchTerm || selectedGroup 
                                                        ? "Nie znaleziono wydarzeń spełniających kryteria wyszukiwania" 
                                                        : `Obecnie brak ${viewMode === 'upcoming' ? 'nadchodzących' : 'przeszłych'} wydarzeń`
                                                    }
                                                </p>
                                                {(searchTerm || selectedGroup) && (
                                                    <Button 
                                                        onClick={() => {
                                                            setSearchTerm("");
                                                            setSelectedGroup("");
                                                        }}
                                                        className="bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700 text-white shadow-lg"
                                                    >
                                                        Wyczyść filtry
                                                    </Button>
                                                )}
                                            </div>
                                        </div>
                                    )}
                                </>
                            )}

                            {/* Pagination */}
                            {!searchTerm && !selectedGroup && (
                                <div className="flex justify-center items-center space-x-4 pt-8">
                                    <Button
                                        variant="outline"
                                        onClick={goToPreviousPage}
                                        disabled={offset === 0}
                                        className="bg-white border-slate-300 hover:bg-slate-50 shadow-sm"
                                    >
                                        <ChevronLeft className="w-4 h-4 mr-2" />
                                        Poprzednia
                                    </Button>
                                    
                                    <div className="px-4 py-2 bg-gradient-to-r from-blue-500 to-purple-600 text-white rounded-lg shadow-lg font-semibold">
                                        Strona {currentPage}
                                    </div>
                                    
                                    <Button
                                        variant="outline"
                                        onClick={goToNextPage}
                                        disabled={!hasMoreEvents}
                                        className="bg-white border-slate-300 hover:bg-slate-50 shadow-sm"
                                    >
                                        Następna
                                        <ChevronRight className="w-4 h-4 ml-2" />
                                    </Button>
                                </div>
                            )}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}
