import { describe, expect, it } from 'vitest'

import { DEV_API_URL, resolveApiUrl } from './api-url.ts'

describe('resolveApiUrl', () => {
  it('uses the configured URL without a trailing slash', () => {
    expect(resolveApiUrl('https://api.example.com/', { required: true })).toBe(
      'https://api.example.com',
    )
  })

  it('keeps a path prefix', () => {
    expect(
      resolveApiUrl('http://api.example.com/v1//', { required: true }),
    ).toBe('http://api.example.com/v1')
  })

  it('falls back to the local API when the URL is optional', () => {
    expect(resolveApiUrl(undefined, { required: false })).toBe(DEV_API_URL)
    expect(resolveApiUrl('  ', { required: false })).toBe(DEV_API_URL)
  })

  it.each([undefined, '', '   '])(
    'rejects a missing URL when required (%j)',
    (value) => {
      expect(() => resolveApiUrl(value, { required: true })).toThrow(
        /VITE_API_URL/,
      )
    },
  )

  it.each([
    '/api',
    'api.example.com',
    'ftp://api.example.com',
    'javascript:alert(1)',
  ])('rejects %j', (value) => {
    expect(() => resolveApiUrl(value, { required: true })).toThrow(
      /VITE_API_URL.*http/,
    )
  })

  it('rejects an invalid URL even when optional', () => {
    expect(() => resolveApiUrl('/api', { required: false })).toThrow(
      /VITE_API_URL/,
    )
  })
})
