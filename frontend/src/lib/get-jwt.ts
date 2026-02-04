// lib/get-jwt.ts
import { headers } from 'next/headers';
import { auth } from './auth';
import { SignJWT } from 'jose';

export async function getJWT(): Promise<string | null> {
  try {
    // Get the session to verify user is authenticated
    const sessionData = await auth.api.getSession({
      headers: await headers()
    });

    if (!sessionData?.user) {
      console.error('No session user found');
      return null;
    }

    // Create our own JWT token using the shared BETTER_AUTH_SECRET
    // The backend expects HS256 algorithm with 'sub' field containing user ID
    const secret = new TextEncoder().encode(process.env.BETTER_AUTH_SECRET!);

    const token = await new SignJWT({
      sub: sessionData.user.id, // User ID - backend expects this in 'sub' field
      email: sessionData.user.email,
      name: sessionData.user.name,
    })
      .setProtectedHeader({ alg: 'HS256', typ: 'JWT' })
      .setIssuedAt()
      .setExpirationTime('24h') // Token valid for 24 hours
      .sign(secret);

    console.log('Successfully created JWT token for user:', sessionData.user.id);
    return token;
  } catch (error) {
    console.error("Error creating JWT:", error);
    return null;
  }
}