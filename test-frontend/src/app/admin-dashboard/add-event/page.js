"use client";
import { useState } from "react";
import EventWindow from "@/components/EventWindow";
import EventWindowDetailed from "@/components/EventWindowDetailed";
import { useAdmin } from "@/app/AdminContext";
import { addEvent } from "@/api/addEntitiesApi";

export default function AddEventPage() {
  // This page is for adding a new event
  const {admin } = useAdmin();
  const [event, setEvent] = useState({
    description: "",
    end_date: "",
    id: 1,
    image_url: "",
    location: "",
    start_date: "",
    title: "",
    group_name: "test",
  });

  const handleAddEventSubmit = async () => {
    try {
      const response = await addEvent(event);

    } catch (error) {
      console.error("Error adding event:", error);
    }
  }
    

  const [eventClicked, setEventClicked] = useState(false);

  const setEventOnInputChange = (e) => {
    const { name, value } = e.target;
    setEvent((prevEvent) => ({
      ...prevEvent,
      [name]: value,
    }));
  };

  return (
    <>
      <h1 className="text-2xl font-bold mb-4">Add Event</h1>
      <div className="flex flex-row  items-center justify-around min-h-screen">
        <form className="flex flex-col gap-4 w-full max-w-md">
          <input
            placeholder="Title"
            value={event.title}
            name="title"
            onChange={setEventOnInputChange}
            className="border p-2 rounded"
          />
          <input
            placeholder="Description"
            value={event.description}
            name="description"
            onChange={setEventOnInputChange}
            className="border p-2 rounded"
          />
          <input
            type="datetime-local"
            placeholder="Start Date"
            value={event.start_date}
            name="start_date"
            onChange={setEventOnInputChange}
            className="border p-2 rounded"
          />
          <input
            type="datetime-local"
            placeholder="End Date"
            value={event.end_date}
            name="end_date"
            onChange={setEventOnInputChange}
            className="border p-2 rounded"
          />
          <input
            placeholder="Location"
            value={event.location}
            name="location"
            onChange={setEventOnInputChange}
            className="border p-2 rounded"
          />
          <input
            placeholder="Image URL"
            value={event.image_url}
            name="image_url"
            onChange={setEventOnInputChange}
            className="border p-2 rounded"
          />
          <button
            type="button"
            onClick={handleAddEventSubmit}
            className="bg-blue-500 text-white p-2 rounded hover:bg-blue-600">
            Add Event
          </button>
        </form>

        {/* Podgląd wydarzenia */}
        <div className="mt-8 w-full max-w-2xl">
          <EventWindow event={event} onClick={() => setEventClicked(true)}/>
          {eventClicked && <EventWindowDetailed event={event} onClick={() => setEventClicked(false)} />}
        </div>
      </div>
    </>
  );
}
