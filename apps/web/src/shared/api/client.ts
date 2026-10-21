// Dev: Vite-прокси. Prod: задайте VITE_API_URL=https://api.example.com
export const API_URL = import.meta.env.VITE_API_URL ?? ''

export async function api<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${API_URL}${path}`, init)
  if (!res.ok) throw new Error(`${res.status} ${res.statusText}`)
  return res.json() as Promise<T>
}
