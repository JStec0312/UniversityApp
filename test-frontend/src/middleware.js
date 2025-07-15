import { NextRequest, NextResponse } from 'next/server'
import { jwtVerify } from 'jose'

export async function middleware(req) {
  const token = req.cookies.get('access_token')?.value
  if (!token) return NextResponse.redirect(new URL('/', req.url))

  try {
    const { payload } = await jwtVerify(
      token,
      new TextEncoder().encode(process.env.JWT_SECRET)
    )
    if (payload.role != 'student' && payload.role!='admin') {
      return NextResponse.redirect(new URL('/', req.url))
    }
    return NextResponse.next()
  } catch {
    return NextResponse.redirect(new URL('/', req.url))
  }
}

export const config = { matcher: ['/dashboard/:path*'] }
