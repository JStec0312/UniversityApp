"use client";
import { useEffect, useState } from "react";
import instance from "@/lib/axiosInstance";
import ProfileSettingsContent from "@/components/ProfileSettingsContent";

export default function ProfilePageSettings() {
  const [email, setEmail] = useState(null);

  useEffect(() => {
    instance.get("/user/getEmail")
      .then(res => setEmail(res.data))
      .catch(console.error);
  }, []);

  return <ProfileSettingsContent email={email} />;
}
