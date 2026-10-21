import { Button as BaseButton } from '@base-ui/react/button'
import type { ComponentProps } from 'react'
import { cn } from '../lib/cn'

type Props = ComponentProps<typeof BaseButton> & { variant?: 'primary' | 'ghost' }

export function Button({ variant = 'primary', className, ...props }: Props) {
  return (
    <BaseButton
      {...props}
      className={cn(
        'inline-flex h-10 items-center justify-center rounded-xl px-4 text-sm font-medium transition outline-none',
        'focus-visible:ring-2 focus-visible:ring-brand/60 data-[disabled]:cursor-not-allowed data-[disabled]:opacity-40',
        variant === 'primary' && 'bg-brand text-white hover:brightness-110',
        variant === 'ghost' && 'bg-white/5 text-slate-200 hover:bg-white/10',
        className,
      )}
    />
  )
}
