export default function EventWindow({ event, onClick }) {
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
        <div
            key={event.id}
            className="bg-white rounded-xl shadow-md overflow-hidden hover:shadow-lg transition-shadow duration-300 cursor-pointer"
            onClick={onClick}
        >
            <div className="h-48 overflow-hidden">
                <img
                    src={event.image_url || "https://via.placeholder.com/400x200?text=No+Image"}
                    alt={event.title}
                    className="w-full h-full object-cover transition-transform duration-500 hover:scale-110"
                />
            </div>
            <div className="p-6">
                <div className="flex items-center mb-2">
                    <span className="inline-block bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded-full uppercase font-semibold tracking-wide">
                        Event
                    </span>
                    <span>
                        
                    </span>
                    <span className="ml-2 text-sm text-gray-500">
                        {formatDate(event.start_date)}
                    </span>
                </div>
                <span className="text-green-800 font-bold">{event.group_name}</span>
                <h2 className="text-xl font-bold text-gray-800 mb-2 line-clamp-1">{event.title}</h2>
                <p className="text-gray-600 mb-4 line-clamp-2">{event.description}</p>
                <button
                    className="mt-2 text-blue-600 hover:text-blue-800 font-medium flex items-center"
                >
                    Learn more
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4 ml-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                    </svg>
                </button>
            </div>
        </div>
    );
}