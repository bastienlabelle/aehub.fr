<template>
  <div>

    <!-- Header -->
    <div class="flex items-center justify-between mb-6">
      <h2 class="text-xl font-bold text-base-content">Déclarations</h2>
      <select v-model="selectedYear" class="select select-bordered select-sm" @change="fetchDeclarations">
        <option v-for="y in availableYears" :key="y" :value="y">{{ y }}</option>
      </select>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="flex justify-center py-12">
      <span class="loading loading-spinner loading-md"></span>
    </div>

    <div v-else class="flex flex-col gap-6">

      <!-- Trimestres -->
      <div class="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <div v-for="q in quarters" :key="q.key" class="card bg-base-100 border border-base-300">
          <div class="card-body p-5">
            <p class="text-xs text-base-content/50 font-medium uppercase tracking-wider">{{ q.key }} {{ selectedYear }}</p>
            <p class="text-2xl font-bold text-base-content mt-1">{{ formatAmount(q.total) }} €</p>
            <p class="text-xs text-base-content/40 mt-1">{{ q.period }}</p>
            <div class="divider my-1"></div>
            <p class="text-xs text-base-content/50">Cotisations estimées</p>
            <p class="text-lg font-semibold text-warning">{{ formatAmount(q.total * rate) }} €</p>
          </div>
        </div>
      </div>

      <!-- Total annuel -->
      <div class="card bg-base-100 border border-base-300">
        <div class="card-body p-5 flex flex-row items-center justify-between">
          <div>
            <p class="text-xs text-base-content/50 font-medium uppercase tracking-wider">Total {{ selectedYear }}</p>
            <p class="text-3xl font-bold text-base-content mt-1">{{ formatAmount(totalYear) }} €</p>
          </div>
          <div class="text-right">
            <p class="text-xs text-base-content/50 font-medium uppercase tracking-wider">Cotisations estimées</p>
            <p class="text-2xl font-bold text-warning mt-1">{{ formatAmount(estimatedContributions) }} €</p>
            <p class="text-xs text-base-content/30 mt-1">~22% (taux micro-entreprise services)</p>
          </div>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup lang="ts">
definePageMeta({ middleware: 'auth' })

const { token } = useAuth()

const currentYear = new Date().getFullYear()
const selectedYear = ref(currentYear)
const loading = ref(true)
const data = ref<any>(null)

const availableYears = computed(() => {
  const oldest = data.value?.oldest_year ?? currentYear
  const years = []
  for (let y = currentYear; y >= oldest; y--) {
    years.push(y)
  }
  return years
})

const rate = 0.278

const quarters = computed(() => {
  if (!data.value) return []
  return [
    { key: 'T1', period: 'Jan — Mar', total: data.value.quarters.Q1 },
    { key: 'T2', period: 'Avr — Jun', total: data.value.quarters.Q2 },
    { key: 'T3', period: 'Jul — Sep', total: data.value.quarters.Q3 },
    { key: 'T4', period: 'Oct — Déc', total: data.value.quarters.Q4 },
  ]
})

const totalYear = computed(() => {
  if (!data.value) return 0
  return Object.values(data.value.quarters).reduce((sum: number, v: any) => sum + v, 0)
})

const estimatedContributions = computed(() => totalYear.value * rate)

async function fetchDeclarations() {
  loading.value = true
  try {
    data.value = await $fetch(`/api/dashboard/declarations?year=${selectedYear.value}`, {
      headers: { Authorization: `Bearer ${token.value}` }
    })
  } catch {}
  finally { loading.value = false }
}

function formatAmount(val: number) {
  return new Intl.NumberFormat('fr-FR', { minimumFractionDigits: 2, maximumFractionDigits: 2 }).format(val)
}

onMounted(() => fetchDeclarations())
</script>