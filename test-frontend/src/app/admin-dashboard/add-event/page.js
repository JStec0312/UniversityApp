"use client";
import { useEffect, useState } from "react";
import EventCard from "@/components/EventCard";
import EventDetailModal from "@/components/EventDetailModal";
import { useAdmin } from "@/app/context/AdminContext";
import { addEvent } from "@/api/addEntitiesApi";

export default function AddEventPage() {
  const { admin } = useAdmin();
  const [event, setEvent] = useState({
    description: "",
    end_date: "",
    id: 1,
    image_url: "",
    location: "",
    start_date: "",
    title: "",
    group_name: "...",
  });
  const [eventClicked, setEventClicked] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitMessage, setSubmitMessage] = useState("");

  useEffect(() => {
    if (admin) {
      setEvent((prevEvent) => ({
        ...prevEvent,
        group_name: admin.groupName,
      }));
    }
  }, [admin]);

  const handleAddEventSubmit = async () => {
    try {
      setIsSubmitting(true);
      setSubmitMessage("");
      const response = await addEvent(event);
      setSubmitMessage("✅ Event added successfully!");
      
      // Reset form after successful submission
      setTimeout(() => {
        setEvent({
          description: "",
          end_date: "",
          id: Date.now(), // Generate new ID
          image_url: "",
          location: "",
          start_date: "",
          title: "",
          group_name: admin?.groupName || "...",
        });
        setSubmitMessage("");
      }, 2000);
    } catch (error) {
      console.error("Error adding event:", error);
      setSubmitMessage("❌ Failed to add event. Please try again.");
    } finally {
      setIsSubmitting(false);
    }
  };

  const setEventOnInputChange = (e) => {
    const { name, value } = e.target;
    setEvent((prevEvent) => ({
      ...prevEvent,
      [name]: value,
    }));
  };
  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-blue-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="bg-gradient-to-r from-blue-600 via-purple-600 to-indigo-700 rounded-2xl shadow-xl p-8 mb-8">
          <h1 className="text-4xl font-bold text-white mb-2">Add New Event</h1>
          <p className="text-blue-100">Create and preview your event before publishing</p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Form Section */}
          <div className="bg-white rounded-2xl shadow-lg p-6">
            <h2 className="text-2xl font-bold text-gray-800 mb-6">Event Details</h2>
            
            {submitMessage && (
              <div className={`p-4 rounded-lg mb-6 ${
                submitMessage.includes('✅') 
                  ? 'bg-green-50 border border-green-200 text-green-700' 
                  : 'bg-red-50 border border-red-200 text-red-700'
              }`}>
                {submitMessage}
              </div>
            )}

            <form className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Event Title</label>
                <input
                  type="text"
                  placeholder="Enter event title"
                  value={event.title}
                  name="title"
                  onChange={setEventOnInputChange}
                  className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Description</label>
                <textarea
                  placeholder="Enter event description"
                  value={event.description}
                  name="description"
                  onChange={setEventOnInputChange}
                  rows={4}
                  className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Start Date & Time</label>
                  <input
                    type="datetime-local"
                    value={event.start_date}
                    name="start_date"
                    onChange={setEventOnInputChange}
                    className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">End Date & Time</label>
                  <input
                    type="datetime-local"
                    value={event.end_date}
                    name="end_date"
                    onChange={setEventOnInputChange}
                    className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Location</label>
                <input
                  type="text"
                  placeholder="Enter event location"
                  value={event.location}
                  name="location"
                  onChange={setEventOnInputChange}
                  className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Image URL</label>
                <input
                  type="url"
                  placeholder="Enter image URL"
                  value={event.image_url}
                  name="image_url"
                  onChange={setEventOnInputChange}
                  className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>

              <button
                type="button"
                onClick={handleAddEventSubmit}
                disabled={isSubmitting || !event.title.trim()}
                className={`w-full py-3 px-4 rounded-lg font-semibold transition-colors duration-200 ${
                  isSubmitting || !event.title.trim()
                    ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
                    : 'bg-gradient-to-r from-blue-600 to-purple-600 text-white hover:from-blue-700 hover:to-purple-700'
                }`}
              >
                {isSubmitting ? 'Adding Event...' : 'Add Event'}
              </button>
            </form>
          </div>

          {/* Preview Section */}
          <div className="space-y-6">
            <div className="bg-white rounded-2xl shadow-lg p-6">
              <h2 className="text-2xl font-bold text-gray-800 mb-6">Event Preview</h2>
              <div className="space-y-4">
                <EventCard 
                  event={event} 
                  onClick={() => setEventClicked(true)}
                />
                <p className="text-sm text-gray-600 text-center">
                  Click the preview to see the detailed view
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* Event Detail Modal */}
        <EventDetailModal 
          event={event} 
          isOpen={eventClicked}
          onClose={() => setEventClicked(false)}
        />
      </div>
    </div>
  );
}
