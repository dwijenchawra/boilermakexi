import { NextResponse } from "next/server";

export function middleware(request) {
  if (request.cookies.has("sessionID")) {
    return NextResponse.redirect(new URL("/homepage", request.url));
  }
}

// See "Matching Paths" below to learn more
export const config = {
  matcher: ["/"],
};
