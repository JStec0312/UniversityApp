import React, { useState } from 'react';
export default function EditEventModal({ event, onSave, onClose }) {
    const [formData, setFormData] = useState({
        ...event,
        start_date: event.start_date.slice(0, 16),
        end_date: event.end_date.slice(0, 16)
    });

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => ({
            ...prev,
            [name]: value
        }));
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        onSave(formData);
    };

    return (
        <div className="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
            <div className="relative top-20 mx-auto p-5 border w-full max-w-2xl shadow-lg rounded-md bg-white">
                <div className="mt-3">
                    <h3 className="text-lg font-medium text-gray-900 mb-4">Edit Event</h3>
                    <form onSubmit={handleSubmit} className="space-y-4">
                        <div>
                            <label className="block text-sm font-medium text-gray-700">Title</label>
                            <input
                                type="text"
                                name="title"
                                value={formData.title}
                                onChange={handleInputChange}
                                className="mt-1 block w-full text-black border border-black rounded-md px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                                required
                            />
                        </div>

                        <div>
                            <label className="block text-sm font-medium text-black">Description</label>
                            <textarea
                                name="description"
                                value={formData.description}
                                onChange={handleInputChange}
                                rows={3}
                                className="mt-1 block w-full text-black border border-black rounded-md px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                                required
                            />
                        </div>

                        <div className="grid grid-cols-2 gap-4">
                            <div>
                                <label className="block text-sm font-medium text-gray-700">Start Date & Time</label>
                                <input
                                    type="datetime-local"
                                    name="start_date"
                                    value={formData.start_date}
                                    onChange={handleInputChange}
                                    className="mt-1 block w-full text-black border border-gray-300 rounded-md px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                                    required
                                />
                            </div>

                            <div>
                                <label className="block text-sm font-medium text-gray-700">End Date & Time</label>
                                <input
                                    type="datetime-local"
                                    name="end_date"
                                    value={formData.end_date}
                                    onChange={handleInputChange}
                                    className="mt-1 block w-full border text-black border-gray-300 rounded-md px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                                    required
                                />
                            </div>
                        </div>

                        <div>
                            <label className="block text-sm font-medium text-gray-700">Location</label>
                            <input
                                type="text"
                                name="location"
                                value={formData.location}
                                onChange={handleInputChange}
                                className="mt-1 block w-full text-black border border-gray-300 rounded-md px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                                required
                            />
                        </div>

                        <div>
                            <label className="block text-sm font-medium text-gray-700">Group Name</label>
                            <input
                                type="text"
                                name="group_name"
                                value={formData.group_name}
                                onChange={handleInputChange}
                                className="mt-1 block text-black w-full border border-gray-300 rounded-md px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                                required
                            />
                        </div>

                        <div>
                            <label className="block text-sm font-medium text-gray-700">Image URL</label>
                            <input
                                type="url"
                                name="image_url"
                                value={formData.image_url}
                                onChange={handleInputChange}
                                className="mt-1  text-black block w-full border border-gray-300 rounded-md px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                            />
                        </div>

                        <div className="flex justify-end space-x-3 pt-4">
                            <button
                                type="button"
                                onClick={onClose}
                                className="px-4 py-2 text-black border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50"
                            >
                                Cancel
                            </button>
                            <button
                                type="submit"
                                className="px-4 py-2  text-black bg-blue-600 text-white rounded-md hover:bg-blue-700"
                            >
                                Save Changes
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    );
}