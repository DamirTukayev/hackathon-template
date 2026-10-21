import { useForm } from '@tanstack/react-form'
import { Button } from '@/shared/ui/button'

interface Props {
  isStreaming: boolean
  onSend: (text: string) => void
  onStop: () => void
}

export function ChatForm({ isStreaming, onSend, onStop }: Props) {
  const form = useForm({
    defaultValues: { text: '' },
    onSubmit: ({ value, formApi }) => {
      const text = value.text.trim()
      if (!text) return
      onSend(text)
      formApi.reset()
    },
  })

  return (
    <form
      className="flex items-end gap-2"
      onSubmit={(e) => {
        e.preventDefault()
        form.handleSubmit()
      }}
    >
      <form.Field name="text">
        {(field) => (
          <textarea
            value={field.state.value}
            onChange={(e) => field.handleChange(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault()
                if (!isStreaming) form.handleSubmit()
              }
            }}
            rows={1}
            placeholder="Спросите что-нибудь…  (Enter — отправить, Shift+Enter — перенос)"
            className="max-h-40 min-h-10 flex-1 resize-none rounded-xl bg-white/5 px-4 py-2.5 text-[15px] outline-none placeholder:text-slate-500 focus:ring-2 focus:ring-brand/60"
          />
        )}
      </form.Field>

      {isStreaming ? (
        <Button type="button" variant="ghost" onClick={onStop}>
          Стоп
        </Button>
      ) : (
        <form.Subscribe selector={(s) => s.values.text.trim().length > 0}>
          {(canSend) => (
            <Button type="submit" disabled={!canSend}>
              Отправить
            </Button>
          )}
        </form.Subscribe>
      )}
    </form>
  )
}
