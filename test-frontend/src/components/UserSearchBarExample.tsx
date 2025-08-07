// Example usage of UserSearchBar component

import UserSearchBar from '@/components/UserSearchBar';

// Example component showing how to use the UserSearchBar
export default function ExampleUsage() {
  
  // Your search function - replace this with your actual API call
  const handleUserSearch = async (query: string) => {
    try {
      // Replace with your actual API endpoint
      const response = await fetch(`/api/users/search?q=${encodeURIComponent(query)}`);
      const users = await response.json();
      return users;
    } catch (error) {
      console.error('Error searching users:', error);
      return [];
    }
  };

  // Handle when a user is selected
  const handleUserSelect = (user: any) => {
    console.log('Selected user:', user);
    // Do something with the selected user
    // e.g., navigate to their profile, add them to a group, etc.
  };

  return (
    <div className="p-6">
      <h2 className="text-lg font-semibold mb-4">Search Users</h2>
      
      <UserSearchBar
        onSearch={handleUserSearch}
        onUserSelect={handleUserSelect}
        placeholder="Search for users..."
        className="mb-4"
      />
      
      {/* Rest of your component */}
    </div>
  );
}

// Example API response format (for reference):
// [
//   {
//     id: 1,
//     displayName: "John Doe",
//     avatarUrl: "https://example.com/avatar.jpg",
//     email: "john@example.com",
//     role: "student"
//   },
//   {
//     id: 2,
//     displayName: "Jane Smith",
//     avatarUrl: null,
//     email: "jane@example.com", 
//     role: "teacher"
//   }
// ]
