import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

/**
 * Extracts the JWT token from the Better Auth session
 * @param session - The Better Auth session object
 * @returns The JWT token string or null if not available
 */
export function extractJwtToken(session: any): string | null {
  if (!session) {
    return null;
  }

  // Try different possible token properties based on Better Auth structure
  return session?.token || session?.accessToken || session?.jwt || null;
}