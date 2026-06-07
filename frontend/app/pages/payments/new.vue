<template>
  <div class="max-w-3xl">

    <!-- Header -->
    <div class="flex items-center gap-3 mb-6">
      <NuxtLink to="/payments" class="btn btn-ghost btn-sm btn-circle">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
        </svg>
      </NuxtLink>
      <h2 class="text-xl font-bold text-base-content">Nouveau paiement</h2>
    </div>

    <div class="flex flex-col gap-4">

      <!-- Infos générales -->
      <div class="card bg-base-100 border border-base-300">
        <div class="card-body gap-4">
          <h3 class="font-semibold text-base-content">Informations générales</h3>

          <div class="grid grid-cols-2 gap-4">

            <div class="form-control">
              <label class="label"><span class="label-text font-medium">Numéro</span></label>
              <input :value="nextNumber" type="text" class="input input-bordered font-mono bg-base-200" disabled />
            </div>

            <div class="form-control">
              <label class="label"><span class="label-text font-medium">Date de paiement <span class="text-error">*</span></span></label>
              <input v-model="form.paid_at" type="date" class="input input-bordered" :class="{ 'input-error': errors.paid_at }" />
              <label v-if="errors.paid_at" class="label"><span class="label-text-alt text-error">{{ errors.paid_at }}</span></label>
            </div>

            <div class="form-control">
              <label class="label"><span class="label-text font-medium">Montant <span class="text-error">*</span></span></label>
              <input v-model="form.amount" type="number" min="0" step="0.01" placeholder="0.00" class="input input-bordered" :class="{ 'input-error': errors.amount }" />
              <label v-if="errors.amount" class="label"><span class="label-text-alt text-error">{{ errors.amount }}</span></label>
            </div>

            <div class="form-control">
              <label class="label"><span class="label-text font-medium">Méthode</span></label>
              <select v-model="form.method" class="select select-bordered">
                <option :value="null">—</option>
                <option value="virement">Virement</option>
                <option value="chèque">Chèque</option>
                <option value="CB">CB</option>
                <option value="espèces">Espèces</option>
                <option value="autre">Autre</option>
              </select>
            </div>

            <div class="form-control col-span-2">
              <label class="label"><span class="label-text font-medium">Référence bancaire</span></label>
              <input v-model="form.reference" type="text" placeholder="Ex: VIR-2026-001" class="input input-bordered" />
            </div>

            <div class="form-control">
              <label class="label"><span class="label-text font-medium">Catégorie</span></label>
              <select v-model="form.category" class="select select-bordered">
                <option :value="null">—</option>
                <option v-for="cat in categories" :key="cat" :value="cat">{{ cat }}</option>
              </select>
            </div>

            <div class="form-control">
              <label class="label"><span class="label-text font-medium">Notes</span></label>
              <textarea v-model="form.notes" class="textarea textarea-bordered" rows="2" placeholder="Informations complémentaires..."></textarea>
            </div>

          </div>
        </div>
      </div>

      <!-- Allocations -->
      <div class="card bg-base-100 border border-base-300">
        <div class="card-body gap-4">
          <div class="flex items-center justify-between">
            <h3 class="font-semibold text-base-content">Factures concernées</h3>
            <button class="btn btn-ghost btn-sm gap-1" @click="addAllocation">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
              </svg>
              Ajouter une facture
            </button>
          </div>

          <div v-if="form.allocations.length === 0" class="text-center py-6 text-base-content/30 text-sm">
            Aucune facture associée
          </div>

          <div v-else class="overflow-x-auto">
            <table class="table table-sm">
              <thead>
                <tr class="text-base-content/50 text-xs uppercase tracking-wider">
                  <th>Facture</th>
                  <th>Solde restant</th>
                  <th>Montant alloué</th>
                  <th></th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(alloc, index) in form.allocations" :key="index">
                  <td>
                    <select v-model="alloc.invoice_id" class="select select-bordered select-sm w-full">
                      <option disabled :value="null">Sélectionner une facture</option>
                      <option v-for="invoice in unpaidInvoices" :key="invoice.id" :value="invoice.id">
                        {{ invoice.number }} — {{ invoice.client.name }}
                      </option>
                    </select>
                  </td>
                  <td class="text-sm text-base-content/70 whitespace-nowrap">
                    {{ remainingForInvoice(alloc.invoice_id) }} €
                  </td>
                  <td>
                    <input v-model="alloc.allocated_amount" type="number" min="0" step="0.01" placeholder="0.00" class="input input-bordered input-sm w-32" />
                  </td>
                  <td>
                    <button class="btn btn-ghost btn-xs btn-square text-error" @click="removeAllocation(index)">
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                      </svg>
                    </button>
                  </td>
                </tr>
              </tbody>
              <tfoot>
                <tr>
                  <td colspan="2" class="text-right text-sm text-base-content/50 font-medium">Total alloué</td>
                  <td class="font-bold text-base-content">{{ totalAllocated }} €</td>
                  <td></td>
                </tr>
              </tfoot>
            </table>
          </div>

          <div v-if="allocationWarning" class="alert alert-warning text-sm py-2">
            <span>{{ allocationWarning }}</span>
          </div>

        </div>
      </div>

      <div v-if="error" class="alert alert-error text-sm py-2">
        <span>{{ error }}</span>
      </div>

      <div class="flex justify-end gap-2">
        <NuxtLink to="/payments" class="btn btn-ghost btn-sm">Annuler</NuxtLink>
        <button class="btn btn-primary btn-sm" :class="{ loading }" :disabled="loading" @click="submit">
          Enregistrer le paiement
        </button>
      </div>

    </div>
  </div>
</template>

<script setup lang="ts">
definePageMeta({ middleware: 'auth' })

const { token } = useAuth()
const router = useRouter()

const invoices = ref<any[]>([])
const nextNumber = ref('')
const loading = ref(false)
const error = ref('')
const errors = reactive<Record<string, string>>({})

const form = reactive({
  paid_at: new Date().toISOString().split('T')[0],
  amount: '',
  method: null as string | null,
  reference: '',
  notes: '',
  allocations: [] as { invoice_id: number | null, allocated_amount: string }[],
})

// Factures non entièrement payées
const unpaidInvoices = computed(() =>
  invoices.value.filter(i => i.status !== 'paid' && i.status !== 'cancelled')
)

function invoiceTotalHT(invoice: any) {
  return invoice.lines.reduce((sum: number, l: any) => {
    const base = Number(l.quantity) * Number(l.unit_price)
    const discount = l.discount_percent ? base * (Number(l.discount_percent) / 100) : 0
    return sum + base - discount
  }, 0)
}

function invoiceTotalPaid(invoice: any) {
  return (invoice.payments ?? []).reduce((sum: number, p: any) => sum + Number(p.allocated_amount), 0)
}

function remainingForInvoice(invoice_id: number | null) {
  if (!invoice_id) return '—'
  const invoice = invoices.value.find(i => i.id === invoice_id)
  if (!invoice) return '—'
  return (invoiceTotalHT(invoice) - invoiceTotalPaid(invoice)).toFixed(2)
}

function addAllocation() {
  form.allocations.push({ invoice_id: null, allocated_amount: '' })
}

function removeAllocation(index: number) {
  form.allocations.splice(index, 1)
}

const totalAllocated = computed(() =>
  form.allocations.reduce((sum, a) => sum + Number(a.allocated_amount || 0), 0).toFixed(2)
)

const allocationWarning = computed(() => {
  const amount = Number(form.amount || 0)
  const allocated = Number(totalAllocated.value)
  if (allocated > amount) return `Le total alloué (${allocated} €) dépasse le montant du paiement (${amount} €)`
  if (amount > 0 && allocated < amount) return `${(amount - allocated).toFixed(2)} € non alloués`
  return null
})

function validate() {
  Object.keys(errors).forEach(k => delete errors[k])
  if (!form.paid_at) errors.paid_at = 'Champ requis'
  if (!form.amount) errors.amount = 'Champ requis'
  if (Number(totalAllocated.value) > Number(form.amount)) {
    errors.amount = `Le total alloué (${totalAllocated.value} €) dépasse le montant du paiement`
  }
  return Object.keys(errors).length === 0
}

async function submit() {
  if (!validate()) return
  loading.value = true
  error.value = ''
  try {
    await $fetch('/api/payments/', {
      method: 'POST',
      headers: { Authorization: `Bearer ${token.value}` },
      body: {
        paid_at: form.paid_at,
        amount: Number(form.amount),
        method: form.method,
        reference: form.reference || null,
        notes: form.notes || null,
        category: form.category || null,
        allocations: form.allocations
          .filter(a => a.invoice_id && a.allocated_amount)
          .map(a => ({
            invoice_id: Number(a.invoice_id),
            allocated_amount: Number(a.allocated_amount),
          })),
      },
    })
    router.push('/payments')
  } catch {
    error.value = 'Une erreur est survenue'
  } finally {
    loading.value = false
  }
}

const categories = ref<string[]>([])

onMounted(async () => {
  const user = await $fetch<any>('/api/auth/me', {
    headers: { Authorization: `Bearer ${token.value}` }
  })
  categories.value = user.payment_categories
    ? user.payment_categories.split('\n').map((c: string) => c.trim()).filter(Boolean)
    : []
  const [fetchedInvoices, { number }] = await Promise.all([
    $fetch<any[]>('/api/invoices/', { headers: { Authorization: `Bearer ${token.value}` } }),
    $fetch<any>('/api/payments/next-number', { headers: { Authorization: `Bearer ${token.value}` } }),
  ])
  invoices.value = fetchedInvoices
  nextNumber.value = number
})
</script>