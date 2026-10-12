const API_URL = import.meta.env.VITE_API_URL ?? 'http://localhost:8000'
const HEALTH_TIMEOUT_MS = 5000

/** Returns whether the API answers its health endpoint in time. */
export async function checkApiHealth(): Promise<boolean> {
  try {
    const response = await fetch(`${API_URL}/health`, {
      signal: AbortSignal.timeout(HEALTH_TIMEOUT_MS),
    })
    return response.ok
  } catch {
    return false
  }
}
