<template>
  <div class="min-h-screen flex" :data-theme="currentTheme">

    <!-- Image side -->
    <div class="hidden lg:flex lg:w-1/2 relative overflow-hidden">
      <img
        src="https://images.unsplash.com/photo-1497366216548-37526070297c?w=1200&auto=format&fit=crop&q=80"
        alt="Office"
        class="w-full h-full object-cover"
      />
      <div class="absolute inset-0 bg-black/40 flex flex-col justify-end p-12">
        <p class="text-white/70 text-sm font-mono tracking-widest uppercase mb-3">Bienvenue sur</p>
        <h1 class="text-white text-6xl font-bold tracking-tight">ÆHUB</h1>
        <p class="text-white/60 mt-3 text-lg">Gérez votre micro-entreprise simplement.</p>
      </div>
    </div>

    <!-- Form side -->
    <div class="w-full lg:w-1/2 flex flex-col items-center justify-center px-8 py-12 bg-base-100 relative">

      <!-- Theme toggle -->
      <button
        class="absolute top-6 right-6 btn btn-ghost btn-circle"
        @click="toggleTheme"
        :aria-label="isDark ? 'Passer en mode clair' : 'Passer en mode sombre'"
      >
        <svg v-if="isDark" xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364-6.364l-.707.707M6.343 17.657l-.707.707M17.657 17.657l-.707-.707M6.343 6.343l-.707-.707M12 7a5 5 0 100 10A5 5 0 0012 7z" />
        </svg>
        <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
        </svg>
      </button>

      <div class="w-full max-w-md">

        <!-- Logo mobile -->
        <div class="lg:hidden mb-10">
          <h1 class="text-4xl font-bold text-base-content tracking-tight">ÆHUB</h1>
          <p class="text-base-content/50 mt-1 text-sm">Gérez votre micro-entreprise simplement.</p>
        </div>

        <h2 class="text-3xl font-bold text-base-content mb-2">Connexion</h2>
        <p class="text-base-content/50 mb-8 text-sm">Entrez vos identifiants pour accéder à votre espace.</p>

        <form @submit.prevent="handleLogin" class="space-y-5">

          <div class="form-control">
            <label class="label">
              <span class="label-text font-medium">Email</span>
            </label>
            <input
              v-model="form.email"
              type="email"
              placeholder="vous@exemple.fr"
              class="input input-bordered w-full"
              :class="{ 'input-error': error }"
              required
              autofocus
            />
          </div>

          <div class="form-control">
            <label class="label">
              <span class="label-text font-medium">Mot de passe</span>
            </label>
            <div class="relative">
              <input
                v-model="form.password"
                :type="showPassword ? 'text' : 'password'"
                placeholder="••••••••"
                class="input input-bordered w-full pr-12"
                :class="{ 'input-error': error }"
                required
              />
              <button
                type="button"
                class="absolute right-3 top-1/2 -translate-y-1/2 text-base-content/40 hover:text-base-content transition-colors"
                @click="showPassword = !showPassword"
              >
                <svg v-if="showPassword" xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 4.411m0 0L21 21" />
                </svg>
                <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                </svg>
              </button>
            </div>
          </div>

          <div v-if="error" class="alert alert-error text-sm py-2">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <span>{{ error }}</span>
          </div>

          <button
            type="submit"
            class="btn btn-primary w-full"
            :class="{ 'loading': loading }"
            :disabled="loading"
          >
            {{ loading ? 'Connexion...' : 'Se connecter' }}
          </button>

        </form>

      </div>
    </div>

  </div>
</template>

<script setup lang="ts">
definePageMeta({ layout: false })
import { useMediaQuery } from '@vueuse/core'

// Theme
const prefersDark = useMediaQuery('(prefers-color-scheme: dark)')
const isDark = ref(prefersDark.value)
const currentTheme = computed(() => isDark.value ? 'dark' : 'emerald')

watch(prefersDark, (val) => { isDark.value = val })

function toggleTheme() {
  isDark.value = !isDark.value
}

// Form
const form = reactive({ email: '', password: '' })
const showPassword = ref(false)
const loading = ref(false)
const error = ref('')

async function handleLogin() {
  loading.value = true
  error.value = ''
  try {
    const data = await $fetch('/api/auth/login', {
      method: 'POST',
      body: new URLSearchParams({
        username: form.email,
        password: form.password,
      }),
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    })
    const { setToken } = useAuth()
    // après le fetch réussi :
    setToken(data.access_token)
    navigateTo('/')

    console.log(data)
  } catch (e: any) {
    error.value = 'Identifiants invalides'
  } finally {
    loading.value = false
  }
}
</script>