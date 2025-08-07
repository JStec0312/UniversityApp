// app/dashboard/profile/[id]/page.tsx
import { cookies } from 'next/headers';
import { notFound } from 'next/navigation';
import UserProfileContent from '@/components/UserProfileContent';
import { getUserById } from '@/api/userSearchApi';

interface PageProps {
  //  ⬇️  params to obietnica
  params: Promise<{ id: string }>;
}

export default async function Page({ params }: PageProps) {
  // najpierw wyciągamy id z obietnicy
  const { id } = await params;

  const userId = Number(id);
  if (Number.isNaN(userId)) notFound();

  // cookies() też jest async, patrz poprzedni fix
  const cookieHeader = (await cookies()).toString();

  const user = await getUserById(userId, cookieHeader);
  if (!user) notFound();

  return <UserProfileContent user={user} />;
}
