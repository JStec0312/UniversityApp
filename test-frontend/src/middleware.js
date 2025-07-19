// src/middleware.ts
import { NextRequest, NextResponse } from 'next/server';
import { jwtVerify } from 'jose';

async function verifyToken(token) {
  if (!token) throw new Error('no token');
  return jwtVerify(token, new TextEncoder().encode(process.env.JWT_SECRET));
}

export async function middleware(req) {
  try {
    const token = req.cookies.get('access_token')?.value;
    const { payload } = await verifyToken(token);
    const { pathname } = req.nextUrl;

    if (pathname.startsWith('/admin-dashboard')) {
      if (payload.role !== 'admin' && payload.role !== 'superior_admin')
        return NextResponse.redirect(new URL('/', req.url));
    }

    if (pathname.startsWith('/dashboard')) {
      if (!['admin', 'student', 'superior_admin'].includes(String(payload.role)))
        return NextResponse.redirect(new URL('/', req.url));
    }

    // OK
    return NextResponse.next();
  } catch {
    return NextResponse.redirect(new URL('/', req.url));
  }
}

// Działa tylko na / dashboard i / admin
export const config = {
  matcher: ['/dashboard/:path*', '/admin/:path*'],
};
