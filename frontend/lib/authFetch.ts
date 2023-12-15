import { Session } from 'next-auth';
import CredentialsProvider from 'next-auth/providers/credentials';
import GoogleProvider from 'next-auth/providers/google';
import GithubProvider from 'next-auth/providers/github';

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
		CredentialsProvider({
			name: 'Sign In',
			credentials: {
				username: { label: 'Username', type: 'text', placeholder: 'John Doe' },
				password: { label: 'Password', type: 'password' },
			},
			async authorize(credentials) {
				if (!credentials || !credentials.username || !credentials.password) {
					return null;
				}
				if (dbUser && dbUser.password === credentials.password) {
					return dbUser;
				}
				return null;
			},
		}),
		GoogleProvider({
			clientId: process.env.GOOGLE_CLIENT_ID as string,
			clientSecret: process.env.GOOGLE_CLIENT_SECRET as string,
		}),
		GithubProvider({
			clientId: process.env.GITHUB_CLIENT_ID as string,
			clientSecret: process.env.GITHUB_CLIENT_SECRET as string,
		}),
	]
};
