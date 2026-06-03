<template>
  <div>

    <!-- Loading -->
    <div v-if="loading" class="flex justify-center py-12">
      <span class="loading loading-spinner loading-md"></span>
    </div>

    <div v-else class="flex flex-col gap-6">

      <!-- Stats cards -->
      <div class="grid grid-cols-2 lg:grid-cols-4 gap-4">

        <div class="card bg-base-100 border border-base-300">
          <div class="card-body p-5">
            <p class="text-xs text-base-content/50 font-medium uppercase tracking-wider">CA encaissé {{ currentYear }}</p>
            <p class="text-2xl font-bold text-base-content mt-1">{{ formatAmount(stats.revenue_paid) }} €</p>
          </div>
        </div>

        <div class="card bg-base-100 border border-base-300">
          <div class="card-body p-5">
            <p class="text-xs text-base-content/50 font-medium uppercase tracking-wider">En attente</p>
            <p class="text-2xl font-bold text-warning mt-1">{{ formatAmount(stats.revenue_pending) }} €</p>
          </div>
        </div>

        <div class="card bg-base-100 border border-base-300">
          <div class="card-body p-5">
            <p class="text-xs text-base-content/50 font-medium uppercase tracking-wider">Clients</p>
            <p class="text-2xl font-bold text-base-content mt-1">{{ stats.clients_count }}</p>
          </div>
        </div>

        <div class="card bg-base-100 border border-base-300">
          <div class="card-body p-5">
            <p class="text-xs text-base-content/50 font-medium uppercase tracking-wider">Devis en cours</p>
            <p class="text-2xl font-bold text-base-content mt-1">{{ stats.quotes_count }}</p>
          </div>
        </div>

      </div>

      <!-- Graphique CA mensuel -->
      <div class="card bg-base-100 border border-base-300">
        <div class="card-body p-5">
          <h3 class="font-semibold text-base-content mb-4">CA mensuel {{ currentYear }}</h3>
          <div class="flex items-end gap-1 h-40">
            <div
              v-for="m in monthlyData"
              :key="m.month"
              class="flex-1 flex flex-col items-center gap-1"
            >
              <span v-if="m.total > 0" class="text-xs text-base-content/50 whitespace-nowrap">{{ formatAmount(m.total) }}</span>
              <span v-else class="text-xs text-transparent">0</span>
              <div
                class="w-full rounded-t transition-all"
                :class="m.total > 0 ? 'bg-primary' : 'bg-base-200'"
                :style="{ height: `${Math.max((m.total / maxMonthly) * 100, 4)}px` }"
                :title="`${m.label} : ${formatAmount(m.total)} €`"
              ></div>
              <span class="text-xs text-base-content/40">{{ m.short }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 2 colonnes -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-4">

        <!-- Dernières factures -->
        <div class="card bg-base-100 border border-base-300">
          <div class="card-body p-5 gap-3">
            <div class="flex items-center justify-between">
              <h3 class="font-semibold text-base-content">Dernières factures</h3>
              <NuxtLink to="/invoices" class="text-xs text-base-content/40 hover:text-base-content">Voir tout →</NuxtLink>
            </div>
            <div v-if="stats.recent_invoices.length === 0" class="text-sm text-base-content/30 py-4 text-center">
              Aucune facture
            </div>
            <div v-else class="flex flex-col gap-2">
              <NuxtLink
                v-for="inv in stats.recent_invoices"
                :key="inv.id"
                :to="`/invoices/${inv.id}`"
                class="flex items-center justify-between py-2 border-b border-base-200 last:border-0 hover:opacity-70 transition-opacity"
              >
                <div>
                  <span class="font-mono text-sm font-medium">{{ inv.number }}</span>
                  <span class="text-xs text-base-content/50 ml-2">{{ inv.client_name }}</span>
                </div>
                <span class="badge badge-sm" :class="statusClass(inv.status)">{{ statusLabel(inv.status) }}</span>
              </NuxtLink>
            </div>
          </div>
        </div>

        <!-- Factures en retard -->
        <div class="card bg-base-100 border border-base-300">
          <div class="card-body p-5 gap-3">
            <h3 class="font-semibold text-base-content">Factures en retard</h3>
            <div v-if="stats.overdue_invoices.length === 0" class="text-sm text-base-content/30 py-4 text-center">
              Aucune facture en retard 🎉
            </div>
            <div v-else class="flex flex-col gap-2">
              <NuxtLink
                v-for="inv in stats.overdue_invoices"
                :key="inv.id"
                :to="`/invoices/${inv.id}`"
                class="flex items-center justify-between py-2 border-b border-base-200 last:border-0 hover:opacity-70 transition-opacity"
              >
                <div>
                  <span class="font-mono text-sm font-medium">{{ inv.number }}</span>
                  <span class="text-xs text-base-content/50 ml-2">{{ inv.client_name }}</span>
                </div>
                <span class="text-xs text-error font-medium">{{ daysOverdue(inv.due_date) }}j de retard</span>
              </NuxtLink>
            </div>
          </div>
        </div>

      </div>

    </div>
  </div>
</template>

<script setup lang="ts">
definePageMeta({ middleware: 'auth' })

const { token } = useAuth()

const loading = ref(true)
const stats = ref<any>({
  revenue_paid: 0,
  revenue_pending: 0,
  clients_count: 0,
  quotes_count: 0,
  monthly: [],
  recent_invoices: [],
  overdue_invoices: [],
})

const currentYear = new Date().getFullYear()

const MONTHS = [
  { label: 'Janvier', short: 'Jan' },
  { label: 'Février', short: 'Fév' },
  { label: 'Mars', short: 'Mar' },
  { label: 'Avril', short: 'Avr' },
  { label: 'Mai', short: 'Mai' },
  { label: 'Juin', short: 'Jun' },
  { label: 'Juillet', short: 'Jul' },
  { label: 'Août', short: 'Aoû' },
  { label: 'Septembre', short: 'Sep' },
  { label: 'Octobre', short: 'Oct' },
  { label: 'Novembre', short: 'Nov' },
  { label: 'Décembre', short: 'Déc' },
]

const monthlyData = computed(() => {
  return MONTHS.map((m, i) => {
    const found = stats.value.monthly.find((r: any) => r.month === i + 1)
    return { month: i + 1, label: m.label, short: m.short, total: found ? found.total : 0 }
  })
})

const maxMonthly = computed(() => {
  const max = Math.max(...monthlyData.value.map(m => m.total))
  return max > 0 ? max : 1
})

function formatAmount(val: number) {
  return new Intl.NumberFormat('fr-FR', { minimumFractionDigits: 2, maximumFractionDigits: 2 }).format(val)
}

function daysOverdue(due_date: string) {
  const diff = new Date().getTime() - new Date(due_date).getTime()
  return Math.floor(diff / (1000 * 60 * 60 * 24))
}

function statusLabel(status: string) {
  const labels: Record<string, string> = {
    draft: 'Brouillon', sent: 'Envoyée', partial: 'Partielle', paid: 'Payée', cancelled: 'Annulée',
  }
  return labels[status] ?? status
}

function statusClass(status: string) {
  const classes: Record<string, string> = {
    draft: 'badge-ghost', sent: 'badge-info', partial: 'badge-warning', paid: 'badge-success', cancelled: 'badge-error',
  }
  return classes[status] ?? 'badge-ghost'
}

onMounted(async () => {
  try {
    stats.value = await $fetch('/api/dashboard/stats', {
      headers: { Authorization: `Bearer ${token.value}` }
    })
  } catch {}
  finally { loading.value = false }
})
</script>