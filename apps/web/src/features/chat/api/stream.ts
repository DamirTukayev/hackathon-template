import { API_URL } from '@/shared/api/client'
import type { ChatMessage, StreamEvent } from '../types'

/** POST + SSE (EventSource умеет только GET, поэтому читаем поток через fetch). */
export async function* streamChat(
  messages: Pick<ChatMessage, 'role' | 'content'>[],
  signal: AbortSignal,
): AsyncGenerator<StreamEvent> {
  const res = await fetch(`${API_URL}/api/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ messages }),
    signal,
  })
  if (!res.ok || !res.body) throw new Error(`API error ${res.status}`)

  const reader = res.body.pipeThrough(new TextDecoderStream()).getReader()
  let buffer = ''
  while (true) {
    const { done, value } = await reader.read()
    if (done) break
    buffer += value
    const frames = buffer.split('\n\n')
    buffer = frames.pop() ?? ''
    for (const frame of frames) {
      const line = frame.split('\n').find((l) => l.startsWith('data: '))
      if (line) yield JSON.parse(line.slice(6)) as StreamEvent
    }
  }
}
