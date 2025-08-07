import { cookies } from 'next/headers';
import ChatClient from "@/components/ChatClient";
type Msg = {
    from: string;
    message: string;
    ts?: number;
}



export default async function DMPage({ params }: { params: Promise<{ id: string }> }) {
    const targetId = (await params).id;
    const backend = process.env.SERVER_URL;
    let initial: Msg[] = [];

  const cookieHeader = (await cookies()).toString();
    try{
        const res = await fetch(`${backend}/api/user/dm?with=${targetId}`, {
            headers: {
                cookie: cookieHeader
            },
            cache: 'no-store'
        });
        if(res.ok){
            initial = await res.json();
        }
    } catch (e) {
        console.error("Failed to fetch messages:", e);
        initial = [];
    }
    return(
        <div>
            <h1>dm {targetId}</h1>
            <ChatClient targetId={targetId} backend={backend} initialMessages={initial} />
        </div>
    )
}