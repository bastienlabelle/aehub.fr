export const useAuth = () => {
  const token = useCookie('auth_token', {
    maxAge: 60 * 60 * 24, // 24h
    sameSite: 'strict',
  })

  const isAuthenticated = computed(() => !!token.value)

  function setToken(t: string) {
    token.value = t
  }

  function logout() {
    token.value = null
    navigateTo('/login')
  }

  return { token, isAuthenticated, setToken, logout }
}