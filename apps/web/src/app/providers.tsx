import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { RouterProvider } from '@tanstack/react-router'
import { Provider as JotaiProvider } from 'jotai'
import { router } from './router'

const queryClient = new QueryClient({
  defaultOptions: { queries: { retry: 1, refetchOnWindowFocus: false } },
})

export function Providers() {
  return (
    <QueryClientProvider client={queryClient}>
      <JotaiProvider>
        <RouterProvider router={router} />
      </JotaiProvider>
    </QueryClientProvider>
  )
}
