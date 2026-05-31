<template>
  <div class="min-h-screen bg-base-200" :data-theme="currentTheme">

    <div class="drawer lg:drawer-open">
      <input id="sidebar-drawer" type="checkbox" class="drawer-toggle" />

      <!-- Page content -->
      <div class="drawer-content flex flex-col">

        <!-- Topbar -->
        <div class="navbar bg-base-100 px-6 sticky top-0 z-10 min-h-14">
          <!-- Burger mobile -->
          <div class="flex-none lg:hidden">
            <label for="sidebar-drawer" class="btn btn-ghost btn-circle btn-sm">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
              </svg>
            </label>
          </div>

          <div class="flex-1">
            <span class="text-base font-semibold text-base-content">{{ pageTitle }}</span>
          </div>

          <div class="flex-none flex items-center gap-2">

            <!-- Theme toggle -->
            <button class="btn btn-ghost btn-circle btn-sm" @click="toggleTheme">
              <svg v-if="isDark" xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364-6.364l-.707.707M6.343 17.657l-.707.707M17.657 17.657l-.707-.707M6.343 6.343l-.707-.707M12 7a5 5 0 100 10A5 5 0 0012 7z" />
              </svg>
              <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
              </svg>
            </button>

            <!-- User dropdown -->
            <div class="dropdown dropdown-end">
              <label tabindex="0" class="btn btn-ghost btn-sm gap-2 normal-case px-2">
                <div class="avatar placeholder">
                  <div class="bg-base-content text-base-100 rounded-full w-7 flex items-center justify-center">
                    <span class="text-xs font-bold">{{ userInitials }}</span>
                  </div>
                </div>
                <span class="hidden sm:inline text-sm font-medium">{{ userName }}</span>
                <svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3 opacity-40" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                </svg>
              </label>
              <ul tabindex="0" class="dropdown-content menu menu-sm shadow-lg bg-base-100 rounded-box w-48 mt-2 border border-base-200">
                <li><a @click="logout" class="text-error">Se déconnecter</a></li>
              </ul>
            </div>

          </div>
        </div>

        <!-- Main content -->
        <main class="flex-1 p-6">
          <NuxtPage />
        </main>

      </div>

      <!-- Sidebar -->
      <div class="drawer-side z-20">
        <label for="sidebar-drawer" class="drawer-overlay"></label>
        <aside class="w-60 min-h-screen bg-base-100 flex flex-col">

          <!-- Logo -->
          <div class="px-5 py-4 flex items-center gap-3">
            <div class="avatar placeholder">
              <div class="bg-base-content text-base-100 rounded-full w-8 flex items-center justify-center">
                <span class="text-xs font-bold">Æ</span>
              </div>
            </div>
            <span class="text-base font-bold tracking-tight text-base-content">ÆHUB</span>
          </div>

          <!-- Nav -->
          <nav class="flex-1 px-2 py-2">
            <ul class="menu menu-sm p-0 gap-0.5 w-[100%]">
              <li>
                <NuxtLink
                  to="/"
                  exact-active-class="bg-base-content text-base-100 hover:bg-base-content"
                  active-class=""
                  class="rounded-lg font-medium text-lg"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
                  </svg>
                  Dashboard
                </NuxtLink>
              </li>
              <li>
                <NuxtLink
                  to="/clients"
                  active-class="bg-base-content text-base-100 hover:bg-base-content"
                  exact-active-class="bg-base-content text-base-100 hover:bg-base-content"
                  class="rounded-lg font-medium text-lg"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0z" />
                  </svg>
                  Clients
                </NuxtLink>
              </li>
              <li>
                <NuxtLink
                  to="/quotes"
                  active-class="bg-base-content text-base-100 hover:bg-base-content"
                  exact-active-class="bg-base-content text-base-100 hover:bg-base-content"
                  class="rounded-lg font-medium text-lg"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                  </svg>
                  Devis
                </NuxtLink>
              </li>
              <li>
                <NuxtLink
                  to="/invoices"
                  active-class="bg-base-content text-base-100 hover:bg-base-content"
                  exact-active-class="bg-base-content text-base-100 hover:bg-base-content"
                  class="rounded-lg font-lg text-lg"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 9V7a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2m2 4h10a2 2 0 002-2v-6a2 2 0 00-2-2H9a2 2 0 00-2 2v6a2 2 0 002 2zm7-5a2 2 0 11-4 0 2 2 0 014 0z" />
                  </svg>
                  Factures
                </NuxtLink>
              </li>
            </ul>
          </nav>

          <!-- Bottom -->
          <div class="px-5 py-4">
            <p class="text-xs text-base-content/30">v0.1.0</p>
          </div>

        </aside>
      </div>
    </div>

  </div>
</template>

<script setup lang="ts">
import { useMediaQuery } from '@vueuse/core'

// Theme
const prefersDark = useMediaQuery('(prefers-color-scheme: dark)')
const isDark = ref(prefersDark.value)
const currentTheme = computed(() => isDark.value ? 'dark' : 'emerald')
watch(prefersDark, (val) => { isDark.value = val })
function toggleTheme() { isDark.value = !isDark.value }

// Auth
const { logout: authLogout, token } = useAuth()
function logout() { authLogout() }

// User
const user = ref<{ first_name: string; last_name: string } | null>(null)
const userName = computed(() => user.value ? `${user.value.first_name} ${user.value.last_name}` : '')
const userInitials = computed(() => user.value ? `${user.value.first_name[0]}${user.value.last_name[0]}` : '?')

onMounted(async () => {
  try {
    user.value = await $fetch('/api/auth/me', {
      headers: { Authorization: `Bearer ${token.value}` }
    })
  } catch {}
})

// Page title
const route = useRoute()
const pageTitle = computed(() => {
  const titles: Record<string, string> = {
    '/': 'Dashboard',
    '/clients': 'Clients',
    '/clients/new': 'Nouveau client',
    '/quotes': 'Devis',
    '/quotes/new': 'Nouveau devis',
    '/invoices': 'Factures',
    '/invoices/new': 'Nouvelle facture',
  }
  return titles[route.path] ?? ''
})
</script>