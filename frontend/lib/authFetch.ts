import { Session } from 'next-auth';
import CredentialsProvider from 'next-auth/providers/credentials';
import GoogleProvider from 'next-auth/providers/google';

type FetchWithToken = (url: string, options?: RequestInit, session?: Session | null) => Promise<Response>;

export const getToken = (session: Session | null) => {
  return session?.accessToken || null;
};

export const fetchWithToken: FetchWithToken = async (url, options = {}, session) => {
  const token = await getToken(session);

  if (!token) {
    throw new Error('Token not available');
  }

  const headers = {
    ...options.headers,
    Authorization: `Bearer ${token}`,
  };

  return fetch(url, { ...options, headers });
};

export const authConfig = {
	providers: [
		GoogleProvider({
			clientId: process.env.GOOGLE_ID as string,
			clientSecret: process.env.GOOGLE_SECRET as string,
		}),
	]
};
