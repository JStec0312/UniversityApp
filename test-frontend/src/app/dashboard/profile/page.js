"use client";
import {useUser} from '@/context/UserContext';
import { useState, useEffect } from 'react';
import ProfilePageContent from "@/components/ProfilePageContent";
export default function ProfilePage() {
    const { user } = useUser();
    const [loader, setLoader] = useState(true);
    useEffect(() => {
        if (user) {
            setLoader(false);
        }
    }, [user]);
    return (
        <ProfilePageContent user={user} loading= {loader} />
    );
}