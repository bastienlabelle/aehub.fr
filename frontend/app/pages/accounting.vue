<template>
  <div>

    <h2 class="text-xl font-bold text-base-content mb-6">Comptabilité</h2>

    <div class="card bg-base-100 border border-base-300">
      <div class="card-body gap-4">
        <h3 class="font-semibold text-base-content">Livre des recettes</h3>

        <div v-if="loading" class="flex justify-center py-6">
          <span class="loading loading-spinner loading-sm"></span>
        </div>

        <div v-else class="flex flex-col divide-y divide-base-200">
          <div v-for="year in availableYears" :key="year" class="flex items-center justify-between py-3">
            <span class="font-medium text-base-content">{{ year }}</span>
            <button class="btn btn-ghost btn-sm gap-2" @click="downloadCsv(year)">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
              </svg>
              Télécharger CSV
            </button>
          </div>
          <div v-if="availableYears.length === 0" class="py-6 text-center text-base-content/30 text-sm">
            Aucun paiement enregistré
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
const availableYears = ref<number[]>([])

onMounted(async () => {
  try {
    const stats = await $fetch<any>('/api/dashboard/stats', {
      headers: { Authorization: `Bearer ${token.value}` }
    })
    const oldest = stats.oldest_year ?? new Date().getFullYear()
    const current = new Date().getFullYear()
    const years = []
    for (let y = current; y >= oldest; y--) years.push(y)
    availableYears.value = years
  } catch {}
  finally { loading.value = false }
})

async function downloadCsv(year: number) {
  const response = await fetch(`/api/accounting/livre-recettes?year=${year}`, {
    headers: { Authorization: `Bearer ${token.value}` }
  })
  const blob = await response.blob()
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `livre-recettes-${year}.csv`
  a.click()
  URL.revokeObjectURL(url)
}
</script>