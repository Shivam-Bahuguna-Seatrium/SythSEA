export const apiRoot = import.meta.env.VITE_API_ROOT ?? "http://127.0.0.1:8000/api";

export async function api<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${apiRoot}${path}`, {
    ...init,
    headers: { "Content-Type": "application/json", ...init?.headers },
  });
  if (!response.ok) {
    const body = (await response.json().catch(() => ({}))) as { detail?: string };
    throw new Error(body.detail ?? `Request failed with ${response.status}`);
  }
  return (await response.json()) as T;
}