"use client";

import { useState, useEffect, useRef } from 'react';
import { Input } from '@/components/ui/input';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { Badge } from '@/components/ui/badge';
import { Search, X, Users } from 'lucide-react';

interface User {
  id: number;
  display_name: string;
  avatar_image_url?: string;

}

interface UserSearchBarProps {
  onSearch: (query: string) => Promise<User[]> | User[];
  onUserSelect: (user: User) => void;
  placeholder?: string;
  className?: string;
}

export default function UserSearchBar({ 
  onSearch, 
  onUserSelect, 
  placeholder = "Szukaj użytkowników...",
  className = ""
}: UserSearchBarProps) {
  const [query, setQuery] = useState('');
  const [users, setUsers] = useState<User[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [isOpen, setIsOpen] = useState(false);
  const [selectedIndex, setSelectedIndex] = useState(-1);
  
  const searchRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  // Handle search with debouncing
  useEffect(() => {
    if (query.trim().length < 2) {
      setUsers([]);
      setIsOpen(false);
      return;
    }

    const timeoutId = setTimeout(async () => {
      setIsLoading(true);
      try {
        const results = await onSearch(query.trim());
        setUsers(results);
        setIsOpen(true);
        setSelectedIndex(-1);
      } catch (error) {
        console.error('Search error:', error);
        setUsers([]);
      } finally {
        setIsLoading(false);
      }
    }, 300);

    return () => clearTimeout(timeoutId);
  }, [query, onSearch]);

  // Close dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (searchRef.current && !searchRef.current.contains(event.target as Node)) {
        setIsOpen(false);
        setSelectedIndex(-1);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  // Handle keyboard navigation
  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (!isOpen) return;

    switch (e.key) {
      case 'ArrowDown':
        e.preventDefault();
        setSelectedIndex(prev => (prev < users.length - 1 ? prev + 1 : prev));
        break;
      case 'ArrowUp':
        e.preventDefault();
        setSelectedIndex(prev => (prev > 0 ? prev - 1 : prev));
        break;
      case 'Enter':
        e.preventDefault();
        if (selectedIndex >= 0 && users[selectedIndex]) {
          handleUserSelect(users[selectedIndex]);
        }
        break;
      case 'Escape':
        setIsOpen(false);
        setSelectedIndex(-1);
        inputRef.current?.blur();
        break;
    }
  };

  const handleUserSelect = (user: User) => {
    onUserSelect(user);
    setQuery('');
    setUsers([]);
    setIsOpen(false);
    setSelectedIndex(-1);
    inputRef.current?.blur();
  };

  const clearSearch = () => {
    setQuery('');
    setUsers([]);
    setIsOpen(false);
    setSelectedIndex(-1);
    inputRef.current?.focus();
  };

  return (
    <div ref={searchRef} className={`relative w-full max-w-md ${className}`}>
      {/* Search Input */}
      <div className="relative">
        <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-slate-400" />
        <Input
          ref={inputRef}
          type="text"
          placeholder={placeholder}
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={handleKeyDown}
          className="pl-10 pr-10 bg-white border-slate-300 focus:border-blue-500 focus:ring-blue-500 shadow-sm"
        />
        {query && (
          <button
            onClick={clearSearch}
            className="absolute right-3 top-1/2 transform -translate-y-1/2 text-slate-400 hover:text-slate-600 transition-colors"
          >
            <X className="h-4 w-4" />
          </button>
        )}
        {isLoading && (
          <div className="absolute right-3 top-1/2 transform -translate-y-1/2">
            <div className="animate-spin rounded-full h-4 w-4 border-2 border-blue-500 border-t-transparent"></div>
          </div>
        )}
      </div>

      {/* Search Results Dropdown */}
      {isOpen && (
        <div className="absolute top-full left-0 right-0 mt-1 bg-white border border-slate-200 rounded-lg shadow-xl z-50 max-h-80 overflow-y-auto">
          {users.length > 0 ? (
            <div className="py-2">
              {users.map((user, index) => (
                <button
                  key={user.id}
                  onClick={() => handleUserSelect(user)}
                  className={`w-full px-4 py-3 text-left hover:bg-slate-50 transition-colors flex items-center space-x-3 ${
                    selectedIndex === index ? 'bg-blue-50 border-r-2 border-blue-500' : ''
                  }`}
                >
                  <Avatar className="w-8 h-8">
                    <AvatarImage src={user.avatar_image_url} alt={user.display_name} />
                    <AvatarFallback className="text-xs">
                      {user.display_name.charAt(0).toUpperCase()}
                    </AvatarFallback>
                  </Avatar>
                  <div className="flex-1 min-w-0">
                    <div className="font-medium text-slate-900 truncate">
                      {user.display_name}
                    </div>
                  </div>
                </button>
              ))}
            </div>
          ) : query.trim().length >= 2 && !isLoading ? (
            <div className="py-8 text-center text-slate-500">
              <Users className="w-8 h-8 mx-auto mb-2 text-slate-300" />
              <p className="text-sm">Nie znaleziono użytkowników</p>
              <p className="text-xs text-slate-400">Spróbuj innej frazy</p>
            </div>
          ) : null}
        </div>
      )}
    </div>
  );
}
