import { ReactNode } from 'react';

interface UserProfileLayoutProps {
    children: ReactNode;
}

export default function UserProfileLayout({ children }: UserProfileLayoutProps) {
    return (
        <div className="min-h-screen bg-gradient-to-br from-blue-50 to-purple-50">
            {children}
        </div>
    );
}
