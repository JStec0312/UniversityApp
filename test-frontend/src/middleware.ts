// src/middleware.ts
import { NextRequest, NextResponse } from 'next/server';
import { jwtVerify } from 'jose';

const SECRET = new TextEncoder().encode(process.env.JWT_SECRET);
const ROLES            = ['admin', 'student', 'superior_admin'];
const ADMIN_ROLES_ONLY = ['admin', 'superior_admin'];

/** Zwraca payload lub null (bez rzucania błędów) */
async function getPayload(token?: string | null) {
  if (!token) return null;
  try {
    const { payload } = await jwtVerify(token, SECRET);
    return payload as { role?: string };
  } catch {
    return null;            // token błędny / wygasły
  }
}

export async function middleware(req: NextRequest) {
  const token   = req.cookies.get('access_token')?.value ?? null;
  const payload = await getPayload(token);
  const { pathname } = req.nextUrl;

  /* — 1. Automatyczne przerzucenie ze strony logowania — */
  if (pathname === '/' && payload?.role && ROLES.includes(String(payload.role))) {
    return NextResponse.redirect(new URL('/dashboard', req.url));
  }

  if (pathname.startsWith('/dashboard')) {
    if (!payload?.role || !ROLES.includes(String(payload.role))) {
      return NextResponse.redirect(new URL('/', req.url));  // wróć do logowania
    }
  }

  if (pathname.startsWith('/admin-dashboard')) {
    if (!payload?.role || !ADMIN_ROLES_ONLY.includes(String(payload.role))) {
      return NextResponse.redirect(new URL('/', req.url));
    }
  }

  return NextResponse.next();
}


export const config = {
  matcher: ['/', '/dashboard/:path*', '/admin-dashboard/:path*'],
};
