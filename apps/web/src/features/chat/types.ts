export type Role = 'user' | 'assistant'

export interface ChatMessage {
  id: string
  role: Role
  content: string
  /** Какой провайдер ответил (anthropic / openai / mock) */
  provider?: string
  /** Если был переход на запасной провайдер */
  fallbackFrom?: string
  error?: string
}

/** Зеркало событий из apps/api/app/ai/router.py */
export type StreamEvent =
  | { type: 'meta'; provider: string }
  | { type: 'delta'; text: string }
  | { type: 'fallback'; from: string; reason: string }
  | { type: 'done' }
  | { type: 'error'; message: string }
