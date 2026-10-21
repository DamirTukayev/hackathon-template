import Markdown from 'react-markdown'
import { cn } from '@/shared/lib/cn'
import type { ChatMessage } from '../types'

function TypingDots() {
  return (
    <span className="inline-flex gap-1 py-1" aria-label="Модель думает">
      {[0, 150, 300].map((d) => (
        <span
          key={d}
          className="size-1.5 animate-bounce rounded-full bg-slate-400"
          style={{ animationDelay: `${d}ms` }}
        />
      ))}
    </span>
  )
}

export function MessageBubble({
  message,
  streaming,
}: {
  message: ChatMessage
  streaming: boolean
}) {
  const isUser = message.role === 'user'
  const waiting = !isUser && streaming && !message.content && !message.error

  return (
    <div className={cn('flex', isUser ? 'justify-end' : 'justify-start')}>
      <div
        className={cn(
          'max-w-[85%] rounded-2xl px-4 py-2.5 text-[15px] leading-relaxed',
          isUser ? 'bg-brand text-white' : 'bg-white/5 text-slate-100',
          message.error && 'border border-red-500/40 bg-red-500/10',
        )}
      >
        {waiting ? (
          <TypingDots />
        ) : isUser ? (
          <p className="whitespace-pre-wrap">{message.content}</p>
        ) : (
          <div className="md">
            <Markdown>{message.content}</Markdown>
            {streaming && message.content && (
              <span className="ml-0.5 inline-block h-4 w-1.5 animate-pulse bg-slate-300 align-middle" />
            )}
          </div>
        )}
        {message.error && <p className="mt-1 text-sm text-red-300">Ошибка: {message.error}</p>}
        {message.fallbackFrom && !streaming && (
          <p className="mt-1 text-xs text-amber-300/80">
            {message.fallbackFrom} недоступен — ответил {message.provider}
          </p>
        )}
      </div>
    </div>
  )
}
