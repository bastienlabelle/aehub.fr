<template>
  <div class="max-w-4xl">

    <!-- Header -->
    <div class="flex items-center gap-3 mb-6">
      <NuxtLink to="/quotes" class="btn btn-ghost btn-sm btn-circle">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
        </svg>
      </NuxtLink>
      <h2 class="text-xl font-bold text-base-content">Nouveau devis</h2>
    </div>

    <div class="flex flex-col gap-4">

      <!-- Infos générales -->
      <div class="card bg-base-100 border border-base-300">
        <div class="card-body gap-4">
          <h3 class="font-semibold text-base-content">Informations générales</h3>

          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">

            <div class="form-control">
              <label class="label"><span class="label-text font-medium">Numéro</span></label>
              <input :value="nextNumber" type="text" class="input input-bordered font-mono" disabled />
            </div>
            
            <div class="form-control">
              <label class="label"><span class="label-text font-medium">Client <span class="text-error">*</span></span></label>
              <select v-model="form.client_id" class="select select-bordered" :class="{ 'select-error': errors.client_id }">
                <option disabled value="">Sélectionner un client</option>
                <option v-for="client in clients" :key="client.id" :value="client.id">
                  {{ client.contact_name }}{{ client.company_name ? ` — ${client.company_name}` : '' }}
                </option>
              </select>
              <label v-if="errors.client_id" class="label"><span class="label-text-alt text-error">{{ errors.client_id }}</span></label>
            </div>

            <div class="form-control">
              <label class="label"><span class="label-text font-medium">Objet</span></label>
              <input v-model="form.subject" type="text" placeholder="Ex: Développement site web" class="input input-bordered" />
            </div>

            <div class="form-control">
              <label class="label"><span class="label-text font-medium">Date d'émission <span class="text-error">*</span></span></label>
              <input v-model="form.issued_at" type="date" class="input input-bordered" :class="{ 'input-error': errors.issued_at }" />
              <label v-if="errors.issued_at" class="label"><span class="label-text-alt text-error">{{ errors.issued_at }}</span></label>
            </div>

            <div class="form-control">
              <label class="label"><span class="label-text font-medium">Date de validité</span></label>
              <input v-model="form.valid_until" type="date" class="input input-bordered" />
            </div>

            <div class="form-control sm:col-span-2">
              <label class="label"><span class="label-text font-medium">Notes</span></label>
              <textarea v-model="form.notes" class="textarea textarea-bordered" rows="2" placeholder="Conditions particulières, délais..."></textarea>
            </div>

          </div>
        </div>
      </div>

      <!-- Lignes -->
      <div class="card bg-base-100 border border-base-300">
        <div class="card-body gap-4">
          <div class="flex items-center justify-between">
            <h3 class="font-semibold text-base-content">Lignes</h3>
            <button class="btn btn-ghost btn-sm gap-1" @click="addLine">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
              </svg>
              Ajouter une ligne
            </button>
          </div>

          <div v-if="form.lines.length === 0" class="text-center py-6 text-base-content/30 text-sm">
            Aucune ligne — cliquez sur "Ajouter une ligne"
          </div>

          <div v-else class="overflow-x-auto">
            <table class="table table-sm">
              <thead>
                <tr class="text-base-content/50 text-xs uppercase tracking-wider">
                  <th class="w-1/2">Description</th>
                  <th>Qté</th>
                  <th>Unité</th>
                  <th>P.U. HT (€)</th>
                  <th>Remise %</th>
                  <th>Total HT</th>
                  <th></th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(line, index) in form.lines" :key="index">
                  <td><input v-model="line.description" type="text" placeholder="Prestation..." class="input input-bordered input-sm w-full" /></td>
                  <td><input v-model="line.quantity" type="number" min="0" step="0.01" placeholder="1" class="input input-bordered input-sm w-24" /></td>
                  <td><input v-model="line.unit" type="text" placeholder="h / jour" class="input input-bordered input-sm w-24" /></td>
                  <td><input v-model="line.unit_price" type="number" min="0" step="0.01" placeholder="0.00" class="input input-bordered input-sm w-28" /></td>
                  <td><input v-model="line.discount_percent" type="number" min="0" max="100" step="0.01" placeholder="0" class="input input-bordered input-sm w-20" /></td>
                  <td class="font-medium text-sm whitespace-nowrap">{{ lineTotal(line) }} €</td>
                  <td>
                    <button class="btn btn-ghost btn-xs btn-square text-error" @click="removeLine(index)">
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                      </svg>
                    </button>
                  </td>
                </tr>
              </tbody>
              <tfoot>
                <tr>
                  <td colspan="5" class="text-right text-sm text-base-content/50 font-medium">Total HT</td>
                  <td class="font-bold text-base-content">{{ totalHT }} €</td>
                  <td></td>
                </tr>
              </tfoot>
            </table>
          </div>

        </div>
      </div>

      <div v-if="error" class="alert alert-error text-sm py-2">
        <span>{{ error }}</span>
      </div>

      <div class="flex justify-end gap-2">
        <NuxtLink to="/quotes" class="btn btn-ghost btn-sm">Annuler</NuxtLink>
        <button class="btn btn-primary btn-sm" :class="{ loading }" :disabled="loading" @click="submit">
          Créer le devis
        </button>
      </div>

    </div>
  </div>
</template>

<script setup lang="ts">
definePageMeta({ middleware: 'auth' })

const { token } = useAuth()
const router = useRouter()

const clients = ref<any[]>([])
const loading = ref(false)
const error = ref('')
const errors = reactive<Record<string, string>>({})

const form = reactive({
  client_id: '' as number | '',
  subject: '',
  issued_at: new Date().toISOString().split('T')[0],
  valid_until: '',
  notes: '',
  lines: [] as any[],
})

function addLine() {
  form.lines.push({ description: '', quantity: 1, unit: '', unit_price: 0, discount_percent: null })
}

function removeLine(index: number) {
  form.lines.splice(index, 1)
}

function lineTotal(line: any) {
  const base = (line.quantity ?? 0) * (line.unit_price ?? 0)
  const discount = line.discount_percent ? base * (line.discount_percent / 100) : 0
  return (base - discount).toFixed(2)
}

const totalHT = computed(() => {
  return form.lines.reduce((sum, line) => {
    const base = (line.quantity ?? 0) * (line.unit_price ?? 0)
    const discount = line.discount_percent ? base * (line.discount_percent / 100) : 0
    return sum + base - discount
  }, 0).toFixed(2)
})

function validate() {
  Object.keys(errors).forEach(k => delete errors[k])
  if (!form.client_id) errors.client_id = 'Champ requis'
  if (!form.issued_at) errors.issued_at = 'Champ requis'
  return Object.keys(errors).length === 0
}

async function submit() {
  if (!validate()) return
  loading.value = true
  error.value = ''
  try {
    await $fetch('/api/quotes/', {
      method: 'POST',
      headers: { Authorization: `Bearer ${token.value}` },
      body: {
        ...form,
        client_id: Number(form.client_id),
        valid_until: form.valid_until || null,
        notes: form.notes || null,
        lines: form.lines.map(l => ({
          ...l,
          quantity: Number(l.quantity),
          unit_price: Number(l.unit_price),
          unit: l.unit || null,
          discount_percent: l.discount_percent ? Number(l.discount_percent) : null,
        }))
      },
    })
    router.push('/quotes')
  } catch {
    error.value = 'Une erreur est survenue'
  } finally {
    loading.value = false
  }
}

const nextNumber = ref('')

onMounted(async () => {
  const [fetchedClients, { number }] = await Promise.all([
    $fetch<any[]>('/api/clients/', { headers: { Authorization: `Bearer ${token.value}` } }),
    $fetch<any>('/api/quotes/next-number', { headers: { Authorization: `Bearer ${token.value}` } }),
  ])
  clients.value = fetchedClients
  nextNumber.value = number
})
</script>