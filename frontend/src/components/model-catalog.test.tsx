import { render, screen, within } from '@testing-library/react'
import { afterEach, describe, expect, it, vi } from 'vitest'

import { ModelCatalog } from './model-catalog'

afterEach(() => {
  vi.unstubAllGlobals()
})

describe('ModelCatalog', () => {
  it('shows the models offered by the API', async () => {
    vi.stubGlobal(
      'fetch',
      vi.fn().mockResolvedValue(
        new Response(
          JSON.stringify({
            models: [
              { id: 'llama-3.1-8b-instant', label: 'Llama 3.1 8B Instant' },
              { id: 'llama-3.3-70b', label: 'Llama 3.3 70B' },
            ],
          }),
        ),
      ),
    )

    render(<ModelCatalog />)

    const list = await screen.findByRole('list')
    expect(within(list).getAllByRole('listitem')).toHaveLength(2)
    expect(screen.getByText('Llama 3.1 8B Instant')).toBeInTheDocument()
    expect(screen.getByText('Llama 3.3 70B')).toBeInTheDocument()
  })

  it('communicates when the catalog cannot be loaded', async () => {
    vi.stubGlobal(
      'fetch',
      vi.fn().mockRejectedValue(new TypeError('Failed to fetch')),
    )

    render(<ModelCatalog />)

    expect(await screen.findByRole('alert')).toHaveTextContent(
      'No se pudieron cargar los modelos',
    )
  })
})
