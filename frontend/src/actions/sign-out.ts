'use server'

import { auth } from '@/lib/auth'
import { headers } from 'next/headers'
import { redirect } from 'next/navigation'

export async function signOutAction() {
  // Sign out the user using better-auth
  await auth.api.signOut({
    headers: await headers(),
  })

  // Redirect to homepage after sign out
  redirect('/')
}