"use client";

import UserSearchBar from './UserSearchBar';

interface User {
  id: number;
  displayName: string;
  avatarUrl?: string;
  email?: string;
  role?: string;
}

export default function TopSearchBar() {
  // Placeholder search function - you'll implement this with your API
  const handleUserSearch = async (query: string): Promise<User[]> => {
    // TODO: Replace with your actual API call
    console.log('Searching for:', query);
    
    // Placeholder - remove this when you implement your API
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve([
          {
            id: 1,
            displayName: `User matching "${query}"`,
            email: 'user@example.com',
            role: 'student'
          }
        ]);
      }, 500);
    });
  };

  // Handle when a user is selected from search results
  const handleUserSelect = (user: User) => {
    console.log('Selected user:', user);
    // TODO: Implement what happens when user is selected
    // e.g., navigate to profile, open chat, etc.
  };

  return (
    <div className="flex-1 max-w-md mx-auto">
      <UserSearchBar
        onSearch={handleUserSearch}
        onUserSelect={handleUserSelect}
        placeholder="Szukaj użytkowników..."
      />
    </div>
  );
}
