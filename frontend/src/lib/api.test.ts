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

    await expect(
      generatePost({
        brief: 'hola',
        audience: 'tech-professionals',
        tone: 'professional',
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
    })

    const [, init] = fetchMock.mock.calls[0] as [string, RequestInit]
    expect(JSON.parse(init.body as string)).toEqual({
      brief: 'hola',
      audience: 'business-leaders',
      tone: 'inspiring',
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
      context: '  dirigido a startups  ',
    })

    const [, init] = fetchMock.mock.calls[0] as [string, RequestInit]
    expect(JSON.parse(init.body as string)).toEqual({
      brief: 'hola',
      audience: 'tech-professionals',
      tone: 'professional',
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
      context: '   ',
    })

    const [, init] = fetchMock.mock.calls[0] as [string, RequestInit]
    expect(JSON.parse(init.body as string)).toEqual({
      brief: 'hola',
      audience: 'tech-professionals',
      tone: 'professional',
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

  it('explains a connection failure', () => {
    expect(generationErrorMessage(new ApiError('x'))).toMatch(
      /conectar con la API/,
    )
  })
})
