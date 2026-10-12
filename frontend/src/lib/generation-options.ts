import type { Audience, Language, Tone } from '@/lib/api'

export interface GenerationOption<T extends string> {
  value: T
  label: string
}

export const DEFAULT_AUDIENCE: Audience = 'tech-professionals'
export const DEFAULT_TONE: Tone = 'professional'
export const DEFAULT_LANGUAGE: Language = 'es'

export const AUDIENCE_OPTIONS: GenerationOption<Audience>[] = [
  { value: 'tech-professionals', label: 'Profesionales de tecnología' },
  { value: 'ai-specialists', label: 'Especialistas en IA' },
  { value: 'business-leaders', label: 'Líderes y directivos' },
  { value: 'general-audience', label: 'Público general' },
]

export const TONE_OPTIONS: GenerationOption<Tone>[] = [
  { value: 'professional', label: 'Profesional' },
  { value: 'friendly', label: 'Cercano' },
  { value: 'inspiring', label: 'Inspirador' },
  { value: 'educational', label: 'Divulgativo' },
]

export const LANGUAGE_OPTIONS: GenerationOption<Language>[] = [
  { value: 'es', label: 'Español' },
  { value: 'en', label: 'Inglés' },
  { value: 'fr', label: 'Francés' },
  { value: 'it', label: 'Italiano' },
]
