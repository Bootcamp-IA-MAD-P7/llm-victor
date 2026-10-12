import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { afterEach, describe, expect, it, vi } from 'vitest'

import { ApiStatus } from './api-status'

afterEach(() => {
  vi.unstubAllGlobals()
})

describe('ApiStatus', () => {
  it('shows the API as available when the health check succeeds', async () => {
    vi.stubGlobal(
      'fetch',
      vi.fn().mockResolvedValue(new Response('{"status":"ok"}')),
    )

    render(<ApiStatus />)

    expect(await screen.findByText('API disponible')).toBeInTheDocument()
  })

  it('shows the API as unavailable and retries on demand', async () => {
    const fetchMock = vi
      .fn()
      .mockRejectedValueOnce(new TypeError('Failed to fetch'))
      .mockResolvedValueOnce(new Response('{"status":"ok"}'))
    vi.stubGlobal('fetch', fetchMock)

    render(<ApiStatus />)

    expect(
      await screen.findByText('La API no está disponible'),
    ).toBeInTheDocument()
    await userEvent.click(screen.getByRole('button', { name: 'Reintentar' }))
    expect(await screen.findByText('API disponible')).toBeInTheDocument()
    expect(fetchMock).toHaveBeenCalledTimes(2)
  })
})
