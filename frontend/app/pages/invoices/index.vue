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
    <div v-else-if="invoices.length === 0" class="card bg-base-100 border border-base-300">
      <div class="card-body items-center text-center py-16">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-12 w-12 text-base-content/20 mb-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M17 9V7a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2m2 4h10a2 2 0 002-2v-6a2 2 0 00-2-2H9a2 2 0 00-2 2v6a2 2 0 002 2zm7-5a2 2 0 11-4 0 2 2 0 014 0z" />
        </svg>
        <p class="text-base-content/40 font-medium">Aucune facture pour l'instant</p>
        <NuxtLink to="/invoices/new" class="btn btn-primary btn-sm mt-4">Créer une facture</NuxtLink>
      </div>
    </div>

    <!-- Table -->
    <div v-else class="card bg-base-100 border border-base-300 overflow-hidden">
      <div class="overflow-x-auto">
        <table class="table table-zebra">
          <thead>
            <tr class="bg-base-200 text-base-content/60 text-xs uppercase tracking-wider">
              <th>Numéro</th>
              <th>Client</th>
              <th>Objet</th>
              <th>Émission</th>
              <th>Échéance</th>
              <th>Statut</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="invoice in invoices" :key="invoice.id" class="hover">
              <td class="font-mono text-sm font-medium">{{ invoice.number }}</td>
              <td class="text-sm text-base-content/70">{{ invoice.client_id }}</td>
              <td class="text-sm text-base-content/70">{{ invoice.subject ?? '—' }}</td>
              <td class="text-sm text-base-content/70">{{ formatDate(invoice.issued_at) }}</td>
              <td class="text-sm text-base-content/70">{{ invoice.due_date ? formatDate(invoice.due_date) : '—' }}</td>
              <td>
                <span class="badge badge-sm" :class="statusClass(invoice.status)">{{ statusLabel(invoice.status) }}</span>
              </td>
              <td class="text-right">
                <div class="flex justify-end gap-1">
                  <NuxtLink :to="`/invoices/${invoice.id}`" class="btn btn-ghost btn-xs">Modifier</NuxtLink>
                  <button class="btn btn-ghost btn-xs text-error" @click="confirmDelete(invoice)">Supprimer</button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
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

await fetchInvoices()
</script>