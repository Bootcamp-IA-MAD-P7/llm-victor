const API_URL = import.meta.env.VITE_API_URL ?? 'http://localhost:8000'
const HEALTH_TIMEOUT_MS = 5000
const GENERATE_TIMEOUT_MS = 30000

export type Audience =
  | 'tech-professionals'
  | 'ai-specialists'
  | 'business-leaders'
  | 'general-audience'

export type Tone = 'professional' | 'friendly' | 'inspiring' | 'educational'

export type Language = 'es' | 'en' | 'fr' | 'it'

export interface GenerateRequest {
  brief: string
  audience: Audience
  tone: Tone
  language: Language
  context?: string
}

export interface GenerateResponse {
  text: string
  provider: string
  model: string
}

/** Error from a request to the API, with the HTTP status when there was a response. */
export class ApiError extends Error {
  readonly status: number | undefined

  constructor(message: string, status?: number) {
    super(message)
    this.name = 'ApiError'
    this.status = status
  }
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

/** Translates a generation error into a message the user can understand. */
export function generationErrorMessage(error: unknown): string {
  if (error instanceof ApiError && error.status !== undefined) {
    if (error.status >= 500) {
      return 'No se pudo generar el contenido. Vuelve a intentarlo en unos momentos.'
    }
    if (error.status >= 400) {
      return 'La solicitud no es válida. Revisa el briefing e inténtalo de nuevo.'
    }
  }
  return 'No se pudo conectar con la API. Comprueba que esté disponible e inténtalo de nuevo.'
}

export async function generatePost(
  req: GenerateRequest,
): Promise<GenerateResponse> {
  const context = req.context?.trim()
  const body: GenerateRequest = {
    brief: req.brief,
    audience: req.audience,
    tone: req.tone,
    language: req.language,
    ...(context ? { context } : {}),
  }
  let response: Response
  try {
    response = await fetch(`${API_URL}/generate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
      signal: AbortSignal.timeout(GENERATE_TIMEOUT_MS),
    })
  } catch {
    throw new ApiError('Failed to reach the API')
  }
  if (!response.ok) {
    throw new ApiError(
      `Generation failed with status ${response.status}`,
      response.status,
    )
  }
  return (await response.json()) as GenerateResponse
}
