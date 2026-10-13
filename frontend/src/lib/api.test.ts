import { afterEach, describe, expect, it, vi } from 'vitest'

import {
  ApiError,
  fetchModels,
  generatePost,
  generationErrorMessage,
} from './api'

const MODEL = 'llama-3.1-8b-instant'

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

    await expect(
      generatePost({
        brief: 'hola',
        audience: 'tech-professionals',
        tone: 'professional',
        language: 'es',
        model: MODEL,
      }),
    ).resolves.toEqual({
      text: 'x',
      provider: 'groq',
      model: 'test',
    })
  })

  it('sends the audience and tone in the request body', async () => {
    const fetchMock = vi
      .fn()
      .mockResolvedValue(
        new Response(
          JSON.stringify({ text: 'x', provider: 'groq', model: 'test' }),
        ),
      )
    vi.stubGlobal('fetch', fetchMock)

    await generatePost({
      brief: 'hola',
      audience: 'business-leaders',
      tone: 'inspiring',
      language: 'en',
      model: MODEL,
    })

    const [, init] = fetchMock.mock.calls[0] as [string, RequestInit]
    expect(JSON.parse(init.body as string)).toEqual({
      brief: 'hola',
      audience: 'business-leaders',
      tone: 'inspiring',
      language: 'en',
      model: MODEL,
    })
  })

  it('sends the language in the request body', async () => {
    const fetchMock = vi
      .fn()
      .mockResolvedValue(
        new Response(
          JSON.stringify({ text: 'x', provider: 'groq', model: 'test' }),
        ),
      )
    vi.stubGlobal('fetch', fetchMock)

    await generatePost({
      brief: 'hola',
      audience: 'tech-professionals',
      tone: 'professional',
      language: 'fr',
      model: MODEL,
    })

    const [, init] = fetchMock.mock.calls[0] as [string, RequestInit]
    expect(JSON.parse(init.body as string)).toMatchObject({
      language: 'fr',
    })
  })

  it('sends the selected model in the request body', async () => {
    const fetchMock = vi
      .fn()
      .mockResolvedValue(
        new Response(
          JSON.stringify({ text: 'x', provider: 'groq', model: 'test' }),
        ),
      )
    vi.stubGlobal('fetch', fetchMock)

    await generatePost({
      brief: 'hola',
      audience: 'tech-professionals',
      tone: 'professional',
      language: 'es',
      model: 'llama-3.3-70b',
    })

    const [, init] = fetchMock.mock.calls[0] as [string, RequestInit]
    expect(JSON.parse(init.body as string)).toMatchObject({
      model: 'llama-3.3-70b',
    })
  })

  it('sends the context in the request body when provided', async () => {
    const fetchMock = vi
      .fn()
      .mockResolvedValue(
        new Response(
          JSON.stringify({ text: 'x', provider: 'groq', model: 'test' }),
        ),
      )
    vi.stubGlobal('fetch', fetchMock)

    await generatePost({
      brief: 'hola',
      audience: 'tech-professionals',
      tone: 'professional',
      language: 'es',
      model: MODEL,
      context: '  dirigido a startups  ',
    })

    const [, init] = fetchMock.mock.calls[0] as [string, RequestInit]
    expect(JSON.parse(init.body as string)).toEqual({
      brief: 'hola',
      audience: 'tech-professionals',
      tone: 'professional',
      language: 'es',
      model: MODEL,
      context: 'dirigido a startups',
    })
  })

  it('omits an empty context from the request body', async () => {
    const fetchMock = vi
      .fn()
      .mockResolvedValue(
        new Response(
          JSON.stringify({ text: 'x', provider: 'groq', model: 'test' }),
        ),
      )
    vi.stubGlobal('fetch', fetchMock)

    await generatePost({
      brief: 'hola',
      audience: 'tech-professionals',
      tone: 'professional',
      language: 'es',
      model: MODEL,
      context: '   ',
    })

    const [, init] = fetchMock.mock.calls[0] as [string, RequestInit]
    expect(JSON.parse(init.body as string)).toEqual({
      brief: 'hola',
      audience: 'tech-professionals',
      tone: 'professional',
      language: 'es',
      model: MODEL,
    })
  })

  it('throws an ApiError with the status on a server error', async () => {
    vi.stubGlobal(
      'fetch',
      vi.fn().mockResolvedValue(new Response('nope', { status: 500 })),
    )

    const error = await generatePost({
      brief: 'hola',
      audience: 'tech-professionals',
      tone: 'professional',
      language: 'es',
      model: MODEL,
    }).catch((e: unknown) => e)

    expect(error).toBeInstanceOf(ApiError)
    expect((error as ApiError).status).toBe(500)
  })

  it('throws an ApiError without status on a network failure', async () => {
    vi.stubGlobal(
      'fetch',
      vi.fn().mockRejectedValue(new TypeError('Failed to fetch')),
    )

    const error = await generatePost({
      brief: 'hola',
      audience: 'tech-professionals',
      tone: 'professional',
      language: 'es',
      model: MODEL,
    }).catch((e: unknown) => e)

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

  it('explains that the selected model is no longer available', () => {
    expect(generationErrorMessage(new ApiError('x', 409))).toMatch(
      /ya no está disponible/,
    )
  })

  it('explains a connection failure', () => {
    expect(generationErrorMessage(new ApiError('x'))).toMatch(
      /conectar con la API/,
    )
  })
})

describe('fetchModels', () => {
  it('returns the models from the API', async () => {
    const fetchMock = vi.fn().mockResolvedValue(
      new Response(
        JSON.stringify({
          models: [{ id: 'llama-3.1-8b-instant', label: 'Llama 3.1 8B' }],
        }),
      ),
    )
    vi.stubGlobal('fetch', fetchMock)

    await expect(fetchModels()).resolves.toEqual([
      { id: 'llama-3.1-8b-instant', label: 'Llama 3.1 8B' },
    ])
    expect(fetchMock.mock.calls[0][0]).toBe('http://localhost:8000/models')
  })

  it('throws an ApiError with the status on a server error', async () => {
    vi.stubGlobal(
      'fetch',
      vi.fn().mockResolvedValue(new Response('nope', { status: 500 })),
    )

    const error = await fetchModels().catch((e: unknown) => e)

    expect(error).toBeInstanceOf(ApiError)
    expect((error as ApiError).status).toBe(500)
  })

  it('throws an ApiError without status on a network failure', async () => {
    vi.stubGlobal(
      'fetch',
      vi.fn().mockRejectedValue(new TypeError('Failed to fetch')),
    )

    const error = await fetchModels().catch((e: unknown) => e)

    expect(error).toBeInstanceOf(ApiError)
    expect((error as ApiError).status).toBeUndefined()
  })
})
