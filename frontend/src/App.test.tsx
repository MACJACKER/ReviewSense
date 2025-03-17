import React from 'react'
import { render, screen } from '@testing-library/react'
import { vi, describe, test, expect } from 'vitest'
import App from './App'

// Mock the AuthContext
vi.mock('./context/AuthContext', () => ({
  AuthProvider: ({ children }: { children: React.ReactNode }) => (
    <div data-testid="auth-provider">{children}</div>
  ),
  useAuth: () => ({
    isAuthenticated: false,
    user: null,
    login: vi.fn().mockResolvedValue({}),
    register: vi.fn().mockResolvedValue({}),
    logout: vi.fn()
  })
}))

// Mock react-router-dom
const mockNavigate = vi.fn()
vi.mock('react-router-dom', async () => {
  const actual = await vi.importActual('react-router-dom')
  return {
    ...actual,
    BrowserRouter: ({ children }: { children: React.ReactNode }) => (
      <div data-testid="browser-router">{children}</div>
    ),
    Routes: ({ children }: { children: React.ReactNode }) => (
      <div data-testid="routes">{children}</div>
    ),
    Route: (props: any) => (
      <div data-testid="route" data-path={props.path}>{props.element}</div>
    ),
    Navigate: (props: any) => (
      <div data-testid="navigate" data-to={props.to}>Navigate</div>
    ),
    Outlet: () => <div data-testid="outlet">Outlet</div>,
    useNavigate: () => mockNavigate
  }
})

// Mock the page components
vi.mock('./pages/Login', () => ({
  default: () => <div data-testid="login-component">Login Component</div>
}))

vi.mock('./pages/Register', () => ({
  default: () => <div data-testid="register-component">Register Component</div>
}))

vi.mock('./pages/Dashboard', () => ({
  default: () => <div data-testid="dashboard-component">Dashboard Component</div>
}))

describe('App Component', () => {
  test('renders without crashing', () => {
    render(<App />)
    expect(document.body).toBeDefined()
  })

  test('renders route components', () => {
    render(<App />)
    expect(screen.getByTestId('browser-router')).toBeInTheDocument()
    expect(screen.getByTestId('routes')).toBeInTheDocument()
    expect(screen.getByTestId('auth-provider')).toBeInTheDocument()
  })
}) 