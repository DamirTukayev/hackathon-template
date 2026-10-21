import { useQuery } from '@tanstack/react-query'
import { useEffect, useRef } from 'react'
import { api } from '@/shared/api/client'
import { Button } from '@/shared/ui/button'
import { useChatStream } from '../model/use-chat-stream'
import { ChatForm } from './chat-form'
import { MessageBubble } from './message-bubble'

const SUGGESTIONS = ['Что ты умеешь?', 'Какие есть риски?', 'Как быстро обрабатываются заявки?']

interface Health {
  demo_mode: boolean
  providers: string[]
}

export function ChatPanel() {
  const { messages, send, stop, reset, isStreaming } = useChatStream()
  const bottomRef = useRef<HTMLDivElement>(null)

  const { data: health, isError } = useQuery({
    queryKey: ['health'],
    queryFn: () => api<Health>('/api/health'),
    refetchInterval: 15_000,
  })

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth', block: 'end' })
  }, [messages])

  return (
    <div className="flex min-h-0 flex-1 flex-col gap-4">
      <header className="flex items-center justify-between">
        <h1 className="text-lg font-semibold">AI Assistant</h1>
        <div className="flex items-center gap-2">
          <span className="rounded-full bg-white/5 px-3 py-1 text-xs text-slate-300">
            {isError
              ? '⚠ API offline'
              : health?.demo_mode
                ? 'DEMO MODE'
                : (health?.providers[0] ?? '…')}
          </span>
          {messages.length > 0 && (
            <Button
              variant="ghost"
              className="h-8 px-3 text-xs"
              onClick={reset}
              disabled={isStreaming}
            >
              Очистить
            </Button>
          )}
        </div>
      </header>

      <div className="min-h-0 flex-1 space-y-3 overflow-y-auto pr-1">
        {messages.length === 0 && (
          <div className="flex h-full flex-col items-center justify-center gap-4 text-center">
            <p className="text-slate-400">Задайте вопрос или выберите пример</p>
            <div className="flex flex-wrap justify-center gap-2">
              {SUGGESTIONS.map((s) => (
                <Button key={s} variant="ghost" className="h-9 text-[13px]" onClick={() => send(s)}>
                  {s}
                </Button>
              ))}
            </div>
          </div>
        )}
        {messages.map((m, i) => (
          <MessageBubble
            key={m.id}
            message={m}
            streaming={isStreaming && i === messages.length - 1}
          />
        ))}
        <div ref={bottomRef} />
      </div>

      <ChatForm isStreaming={isStreaming} onSend={send} onStop={stop} />
    </div>
  )
}
