import { createRootRoute, createRoute, createRouter, Outlet } from '@tanstack/react-router'
import { ChatPage } from '@/pages/chat-page'

const rootRoute = createRootRoute({ component: () => <Outlet /> })

const indexRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: '/',
  component: ChatPage,
})

// Новые страницы: createRoute({ path: '/dashboard', ... }) и добавить в addChildren
export const router = createRouter({ routeTree: rootRoute.addChildren([indexRoute]) })

declare module '@tanstack/react-router' {
  interface Register {
    router: typeof router
  }
}
