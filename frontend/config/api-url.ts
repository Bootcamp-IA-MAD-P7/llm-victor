// URL de la API que la web fija al compilar (ARCHITECTURE §6). Solo el servidor de
// desarrollo y los tests pueden recurrir a la API local; un build de producción la exige.
export const DEV_API_URL = 'http://localhost:8000'

export function resolveApiUrl(
  value: string | undefined,
  { required }: { required: boolean },
) {
  const raw = value?.trim()
  if (!raw) {
    if (required) {
      throw new Error(
        'Define VITE_API_URL con la URL pública de la API, p. ej. https://api.example.com',
      )
    }
    return DEV_API_URL
  }

  let url: URL | undefined
  try {
    url = new URL(raw)
  } catch {
    url = undefined
  }
  if (!url || (url.protocol !== 'http:' && url.protocol !== 'https:')) {
    throw new Error(
      `VITE_API_URL debe ser una URL http o https absoluta; se recibió "${raw}"`,
    )
  }
  return raw.replace(/\/+$/, '')
}
