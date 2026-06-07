<template>
  <div class="min-h-screen bg-base-100" :data-theme="currentTheme">

    <div class="drawer lg:drawer-open">
      <input id="sidebar-drawer" type="checkbox" class="drawer-toggle" />

      <!-- Page content -->
      <div class="drawer-content flex flex-col">

        <!-- Topbar -->
        <div class="navbar bg-neutral text-neutral-content px-6 sticky top-0 z-10 min-h-14">
          <!-- Burger mobile -->
          <div class="flex-none lg:hidden">
            <label for="sidebar-drawer" class="btn btn-ghost btn-circle btn-sm">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
              </svg>
            </label>
          </div>

          <div class="flex-1">
            <span class="text-base font-semibold text-neutral-content">{{ pageTitle }}</span>
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
                  <div class="bg-neutral-content text-neutral rounded-full w-7 flex items-center justify-center">
                    <span class="text-xs font-bold">{{ userInitials }}</span>
                  </div>
                </div>
                <span class="hidden sm:inline text-sm font-medium">{{ userName }}</span>
                <svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3 opacity-40" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                </svg>
              </label>
              <ul tabindex="0" class="dropdown-content menu menu-sm shadow-lg bg-base-100 text-base-content rounded-box w-48 mt-2 border border-base-200">
                <li><NuxtLink to="/settings">Préférences</NuxtLink></li>
                <li><NuxtLink to="/import">Import</NuxtLink></li>
                <li><a @click="logout" class="text-error">Se déconnecter</a></li>
              </ul>
            </div>

          </div>
        </div>

        <!-- Main content -->
        <main class="flex-1 p-6 bg-base-100">
          <NuxtPage />
        </main>

      </div>

      <!-- Sidebar -->
      <div class="drawer-side z-20">
        <label for="sidebar-drawer" class="drawer-overlay"></label>
        <aside class="w-60 min-h-screen bg-neutral text-neutral-content flex flex-col">

          <!-- Logo -->
          <div class="px-5 py-4 flex items-center gap-3">
            <div class="avatar placeholder">
              <div class="bg-neutral-content text-neutral rounded-full w-8 flex items-center justify-center">
                <span class="text-xs font-bold">Æ</span>
              </div>
            </div>
            <span class="text-base font-bold tracking-tight text-neutral-content">ÆHUB</span>
          </div>

          <!-- Nav -->
          <nav class="flex-1 px-2 py-2">
            <ul class="menu menu-sm p-0 gap-0.5 w-[100%]">
              <li v-for="item in menuItems" :key="item.to">
                <NuxtLink
                  :to="item.to"
                  :class="[
                    'rounded-lg font-medium text-lg text-neutral-content',
                    isActive(item)
                      ? 'bg-neutral-content !text-neutral hover:bg-neutral-content hover:!text-neutral'
                      : 'hover:bg-neutral-content/20 hover:text-neutral-content'
                  ]"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" :d="item.icon" />
                  </svg>
                  {{ item.label }}
                </NuxtLink>
              </li>
            </ul>
          </nav>

          <!-- Bottom -->
          <div class="px-5 py-4">
            <p class="text-xs text-neutral-content/30">v0.1.0</p>
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

const menuItems = [
  {
    to: '/',
    label: 'Dashboard',
    exact: true,
    icon: 'M4 13h6V4H4v9zm0 7h6v-5H4v5zm10 0h6V9h-6v11zm0-18v7h6V2h-6z',
  },
  {
    to: '/clients',
    label: 'Clients',
    exact: false,
    icon: 'M9 12a3 3 0 100-6 3 3 0 000 6zm6 0a2.5 2.5 0 100-5 2.5 2.5 0 000 5zM2 20a7 7 0 0114 0H2zm12 0a5.5 5.5 0 015-5.5V20h-5z',
  },
  {
    to: '/quotes',
    label: 'Devis',
    exact: false,
    icon: 'M7 3h10a2 2 0 012 2v14l-7-3-7 3V5a2 2 0 012-2zm2 5h6v2H9V8zm0 4h6v2H9v-2z',
  },
  {
    to: '/invoices',
    label: 'Factures',
    exact: false,
    icon: 'M7 2h8l5 5v15a2 2 0 01-2 2H7a2 2 0 01-2-2V4a2 2 0 012-2zm8 1v5h5M9 12h6M9 16h6',
  },
  {
    to: '/payments',
    label: 'Paiements',
    exact: false,
    icon: 'M3 7a3 3 0 013-3h12a3 3 0 013 3v10a3 3 0 01-3 3H6a3 3 0 01-3-3V7zm2 0v2h14V7H5zm0 6h5v2H5v-2z',
  },
  {
    to: '/declarations',
    label: 'Déclarations',
    exact: false,
    icon: 'M6 2h9l5 5v15a2 2 0 01-2 2H6a2 2 0 01-2-2V4a2 2 0 012-2zm3 7h6v2H9V9zm0 4h6v2H9v-2zm0 4h4v2H9v-2z',
  },
  {
    to: '/accounting',
    label: 'Comptabilité',
    exact: false,
    icon: 'M5 3a2 2 0 012-2h10a2 2 0 012 2v18a1 1 0 01-1.447.894L12 19.118l-5.553 2.776A1 1 0 015 21V3zm3 3v2h8V6H8zm0 4v2h8v-2H8zm0 4v2h5v-2H8z',
  },
]

const route = useRoute()

const pageTitle = computed(() => {
  const extraTitles: Record<string, string> = {
    '/settings': 'Préférences',
    '/import': 'Import de données',
  }
  if (extraTitles[route.path]) return extraTitles[route.path]
  const match = menuItems.find(item =>
    item.exact ? route.path === item.to : route.path.startsWith(item.to)
  )
  return match?.label ?? ''
})

function isActive(item: typeof menuItems[0]) {
  return item.exact ? route.path === item.to : route.path.startsWith(item.to)
}
</script>