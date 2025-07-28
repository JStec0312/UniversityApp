"use client";

import { getUpcomingEvents } from "@/api/eventsApi";
import { useEffect, useState } from "react";

export default  function EventsPage() {
    const [events, setEvents] = useState([]);
    useEffect(() => {
        const fetchEvents = async () => {
            try {
                const events = await getUpcomingEvents();
                setEvents(events);
                console.log("Fetched events:", events);
            } catch (error) {
                console.error("Error fetching events:", error);
            }
        };
        fetchEvents();
    }, []);

    return (
        <>
            {events.map((event) => (
                <div key={event.id} className="p-4 border-b">
                    <h2 className="text-xl font-semibold">{event.title}</h2>
                    <p className="text-gray-600">{event.description}</p>
                    <p className="text-sm text-gray-500">Date: {new Date(event.date).toLocaleDateString()}</p>
                </div>
            ))}     
        </>
    );
}
