import { createAuthClient } from "better-auth/react";

export const authClient = createAuthClient({
  // No JWT plugin needed - we handle JWT creation server-side
});
export const { signIn, signUp, useSession } = authClient;