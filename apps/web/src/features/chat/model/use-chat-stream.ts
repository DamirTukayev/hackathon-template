import { useMutation } from '@tanstack/react-query'
import { useAtom } from 'jotai'
import { useRef } from 'react'
import { streamChat } from '../api/stream'
import type { ChatMessage } from '../types'
import { messagesAtom } from './atoms'

const uid = () => crypto.randomUUID()

export function useChatStream() {
  const [messages, setMessages] = useAtom(messagesAtom)
  const abortRef = useRef<AbortController | null>(null)

  const patch = (id: string, fn: (m: ChatMessage) => Partial<ChatMessage>) =>
    setMessages((prev) => prev.map((m) => (m.id === id ? { ...m, ...fn(m) } : m)))

  const mutation = useMutation({
    mutationFn: async (text: string) => {
      const user: ChatMessage = { id: uid(), role: 'user', content: text }
      const assistant: ChatMessage = { id: uid(), role: 'assistant', content: '' }
      const history = [...messages, user].filter((m) => m.content && !m.error)
      setMessages([...messages, user, assistant])

      const controller = new AbortController()
      abortRef.current = controller
      try {
        for await (const ev of streamChat(history, controller.signal)) {
          if (ev.type === 'meta') patch(assistant.id, () => ({ provider: ev.provider }))
          else if (ev.type === 'fallback') patch(assistant.id, () => ({ fallbackFrom: ev.from }))
          else if (ev.type === 'delta')
            patch(assistant.id, (m) => ({ content: m.content + ev.text }))
          else if (ev.type === 'error') throw new Error(ev.message)
        }
      } catch (e) {
        if ((e as Error).name === 'AbortError') return // «Стоп» — оставляем частичный ответ
        patch(assistant.id, () => ({ error: (e as Error).message }))
        throw e
      } finally {
        abortRef.current = null
      }
    },
  })

  return {
    messages,
    send: mutation.mutate,
    stop: () => abortRef.current?.abort(),
    reset: () => setMessages([]),
    isStreaming: mutation.isPending,
  }
}
