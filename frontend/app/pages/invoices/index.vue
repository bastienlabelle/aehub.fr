<template>
  <div>

    <!-- Header -->
    <div class="flex items-center justify-between mb-6">
      <h2 class="text-xl font-bold text-base-content">Factures</h2>
      <NuxtLink to="/invoices/new" class="btn btn-primary btn-sm gap-2">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
        </svg>
        Nouvelle facture
      </NuxtLink>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="flex justify-center py-12">
      <span class="loading loading-spinner loading-md"></span>
    </div>

    <!-- Empty -->
    <div v-else-if="invoices.length === 0" class="py-16 flex flex-col items-center text-center">
      <svg xmlns="http://www.w3.org/2000/svg" class="h-12 w-12 text-base-content/20 mb-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M17 9V7a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2m2 4h10a2 2 0 002-2v-6a2 2 0 00-2-2H9a2 2 0 00-2 2v6a2 2 0 002 2zm7-5a2 2 0 11-4 0 2 2 0 014 0z" />
      </svg>
      <p class="text-base-content/40 font-medium">Aucune facture pour l'instant</p>
      <NuxtLink to="/invoices/new" class="btn btn-primary btn-sm mt-4">Créer une facture</NuxtLink>
    </div>

    <!-- Table -->
    <div v-else class="">
      <table class="table table-zebra">
        <thead>
          <tr class="text-base-content/60 text-xs uppercase tracking-wider">
            <th>Numéro</th>
            <th class="w-full">Client</th>
            <th>Émission</th>
            <th>Échéance</th>
            <th class="text-right">Total HT</th>
            <th>Statut</th>
            <th></th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="invoice in invoices" :key="invoice.id" class="hover">
            <td class="font-mono text-sm font-medium whitespace-nowrap">{{ invoice.number }}</td>
            <td class="text-sm text-base-content/70 w-full">{{ invoice.client.name }}</td>
            <td class="text-sm text-base-content/70 whitespace-nowrap">{{ formatDate(invoice.issued_at) }}</td>
            <td class="text-sm text-base-content/70 whitespace-nowrap">{{ invoice.due_date ? formatDate(invoice.due_date) : '—' }}</td>
            <td class="text-sm font-medium text-right whitespace-nowrap">{{ invoiceTotalHT(invoice) }} €</td>
            <td class="whitespace-nowrap">
              <span class="badge badge-sm" :class="statusClass(invoice.status)">{{ statusLabel(invoice.status) }}</span>
            </td>
            <td class="whitespace-nowrap">
              <span v-if="isOverdue(invoice)" class="badge badge-sm badge-error">En retard</span>
            </td>
            <td>
              <div class="dropdown dropdown-end">
                <label tabindex="0" class="btn btn-ghost btn-xs btn-square">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 12h.01M12 12h.01M19 12h.01M6 12a1 1 0 11-2 0 1 1 0 012 0zm7 0a1 1 0 11-2 0 1 1 0 012 0zm7 0a1 1 0 11-2 0 1 1 0 012 0z" />
                  </svg>
                </label>
                <ul tabindex="0" class="dropdown-content menu menu-sm shadow bg-base-100 rounded-box w-36 border border-base-200 z-10">
                  <li><NuxtLink :to="`/invoices/${invoice.id}`">Modifier</NuxtLink></li>
                  <li><a class="text-error" @click="confirmDelete(invoice)">Supprimer</a></li>
                </ul>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Delete modal -->
    <dialog ref="deleteModal" class="modal">
      <div class="modal-box">
        <h3 class="font-bold text-lg mb-2">Supprimer cette facture ?</h3>
        <p class="text-base-content/60 text-sm">
          Vous êtes sur le point de supprimer la facture <strong>{{ invoiceToDelete?.number }}</strong>. Cette action est irréversible.
        </p>
        <div class="modal-action">
          <button class="btn btn-ghost btn-sm" @click="deleteModal.close()">Annuler</button>
          <button class="btn btn-error btn-sm" :class="{ loading: deleting }" @click="deleteInvoice">Supprimer</button>
        </div>
      </div>
      <form method="dialog" class="modal-backdrop"><button>close</button></form>
    </dialog>

  </div>
</template>

<script setup lang="ts">
definePageMeta({ middleware: 'auth' })

const { token } = useAuth()

const invoices = ref<any[]>([])
const loading = ref(true)
const deleting = ref(false)
const invoiceToDelete = ref<any>(null)
const deleteModal = ref<HTMLDialogElement>()

async function fetchInvoices() {
  loading.value = true
  try {
    invoices.value = await $fetch('/api/invoices/', {
      headers: { Authorization: `Bearer ${token.value}` }
    })
  } catch {}
  finally { loading.value = false }
}

function confirmDelete(invoice: any) {
  invoiceToDelete.value = invoice
  deleteModal.value?.showModal()
}

async function deleteInvoice() {
  if (!invoiceToDelete.value) return
  deleting.value = true
  try {
    await $fetch(`/api/invoices/${invoiceToDelete.value.id}`, {
      method: 'DELETE',
      headers: { Authorization: `Bearer ${token.value}` }
    })
    deleteModal.value?.close()
    await fetchInvoices()
  } catch {}
  finally { deleting.value = false }
}

function invoiceTotalHT(invoice: any) {
  return invoice.lines.reduce((sum: number, l: any) => {
    const base = Number(l.quantity) * Number(l.unit_price)
    const discount = l.discount_percent ? base * (Number(l.discount_percent) / 100) : 0
    return sum + base - discount
  }, 0).toFixed(2)
}

function formatDate(date: string) {
  return new Date(date).toLocaleDateString('fr-FR')
}

function statusLabel(status: string) {
  const labels: Record<string, string> = {
    draft: 'Brouillon',
    sent: 'Envoyée',
    partial: 'Partielle',
    paid: 'Payée',
    cancelled: 'Annulée',
  }
  return labels[status] ?? status
}

function statusClass(status: string) {
  const classes: Record<string, string> = {
    draft: 'badge-ghost',
    sent: 'badge-info',
    partial: 'badge-warning',
    paid: 'badge-success',
    cancelled: 'badge-error',
  }
  return classes[status] ?? 'badge-ghost'
}

function isOverdue(invoice: any) {
  if (invoice.status === 'paid' || invoice.status === 'cancelled') return false
  if (!invoice.due_date) return false
  return new Date(invoice.due_date) < new Date()
}

await fetchInvoices()
</script>