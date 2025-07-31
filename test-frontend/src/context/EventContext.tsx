"use client";

import React, { createContext, useContext, useState, ReactNode } from 'react';
import { Event } from '@/types/Event';

interface EventContextType {
    selectedEvent: Event | null;
    setSelectedEvent: (event: Event | null) => void;
}

const EventContext = createContext<EventContextType | undefined>(undefined);

export function EventProvider({ children }: { children: ReactNode }) {
    const [selectedEvent, setSelectedEvent] = useState<Event | null>(null);

    return (
        <EventContext.Provider value={{ selectedEvent, setSelectedEvent }}>
            {children}
        </EventContext.Provider>
    );
}

export function useEvent() {
    const context = useContext(EventContext);
    if (context === undefined) {
        throw new Error('useEvent must be used within an EventProvider');
    }
    return context;
}
