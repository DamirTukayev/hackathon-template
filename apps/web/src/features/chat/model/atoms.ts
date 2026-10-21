import { atom } from 'jotai'
import type { ChatMessage } from '../types'

export const messagesAtom = atom<ChatMessage[]>([])
