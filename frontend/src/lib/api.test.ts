import { afterEach, describe, expect, it, vi } from 'vitest'

import { ApiError, generatePost, generationErrorMessage } from './api'

afterEach(() => {
  vi.unstubAllGlobals()
})

describe('generatePost', () => {
  it('returns the parsed response on success', async () => {
    vi.stubGlobal(
      'fetch',
      vi
        .fn()
        .mockResolvedValue(
          new Response(
            JSON.stringify({ text: 'x', provider: 'groq', model: 'test' }),
          ),
        ),
    )

    await expect(generatePost({ brief: 'hola' })).resolves.toEqual({
      text: 'x',
      provider: 'groq',
      model: 'test',
    })
  })

  it('throws an ApiError with the status on a server error', async () => {
    vi.stubGlobal(
      'fetch',
      vi.fn().mockResolvedValue(new Response('nope', { status: 500 })),
    )

    const error = await generatePost({ brief: 'hola' }).catch((e: unknown) => e)

    expect(error).toBeInstanceOf(ApiError)
    expect((error as ApiError).status).toBe(500)
  })

  it('throws an ApiError without status on a network failure', async () => {
    vi.stubGlobal(
      'fetch',
      vi.fn().mockRejectedValue(new TypeError('Failed to fetch')),
    )

    const error = await generatePost({ brief: 'hola' }).catch((e: unknown) => e)

    expect(error).toBeInstanceOf(ApiError)
    expect((error as ApiError).status).toBeUndefined()
  })
})

describe('generationErrorMessage', () => {
  it('explains a generation failure', () => {
    expect(generationErrorMessage(new ApiError('x', 500))).toMatch(
      /Vuelve a intentarlo/,
    )
  })

  it('explains an invalid request', () => {
    expect(generationErrorMessage(new ApiError('x', 422))).toMatch(
      /solicitud no es válida/,
    )
  })

  it('explains a connection failure', () => {
    expect(generationErrorMessage(new ApiError('x'))).toMatch(
      /conectar con la API/,
    )
  })
})
