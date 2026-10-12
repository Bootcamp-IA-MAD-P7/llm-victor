const API_URL = import.meta.env.VITE_API_URL ?? 'http://localhost:8000'
const HEALTH_TIMEOUT_MS = 5000
const GENERATE_TIMEOUT_MS = 30000

export interface GenerateRequest {
  brief: string
}

export interface GenerateResponse {
  text: string
  provider: string
  model: string
}

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

export async function generatePost(
  req: GenerateRequest,
): Promise<GenerateResponse> {
  const response = await fetch(`${API_URL}/generate`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(req),
    signal: AbortSignal.timeout(GENERATE_TIMEOUT_MS),
  })
  if (!response.ok) {
    throw new Error('Failed to generate post')
  }
  return (await response.json()) as GenerateResponse
}
