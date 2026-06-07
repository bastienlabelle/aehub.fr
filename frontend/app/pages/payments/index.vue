<template>
  <div>

    <!-- Header -->
    <div class="flex items-center justify-between mb-6">
      <h2 class="text-xl font-bold text-base-content">Paiements</h2>
      <NuxtLink to="/payments/new" class="btn btn-primary btn-sm gap-2">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
        </svg>
        Nouveau paiement
      </NuxtLink>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="flex justify-center py-12">
      <span class="loading loading-spinner loading-md"></span>
    </div>

    <!-- Empty -->
    <div v-else-if="payments.length === 0" class="py-16 flex flex-col items-center text-center">
      <svg xmlns="http://www.w3.org/2000/svg" class="h-12 w-12 text-base-content/20 mb-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M17 9V7a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2m2 4h10a2 2 0 002-2v-6a2 2 0 00-2-2H9a2 2 0 00-2 2v6a2 2 0 002 2zm7-5a2 2 0 11-4 0 2 2 0 014 0z" />
      </svg>
      <p class="text-base-content/40 font-medium">Aucun paiement pour l'instant</p>
      <NuxtLink to="/payments/new" class="btn btn-primary btn-sm mt-4">Enregistrer un paiement</NuxtLink>
    </div>

    <!-- Table -->
    <div v-else class="overflow-x-auto">
      <table class="table table-zebra">
        <thead>
          <tr class="text-base-content/60 text-xs uppercase tracking-wider">
            <th>Numéro</th>
            <th>Date</th>
            <th>Méthode</th>
            <th>Nature</th>
            <th>Factures</th>
            <th class="text-right">Montant</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="payment in payments" :key="payment.id" class="hover">
            <td class="font-mono text-sm font-medium">{{ payment.number }}</td>
            <td class="text-sm text-base-content/70">{{ formatDate(payment.paid_at) }}</td>
            <td class="text-sm text-base-content/70">{{ payment.method ?? '—' }}</td>
            <td class="text-sm text-base-content/70">{{ payment.category ?? '—' }}</td>
            <td class="text-sm text-base-content/70">
              <span v-if="payment.allocations?.length">
                {{ payment.allocations.length }} facture{{ payment.allocations.length > 1 ? 's' : '' }}
              </span>
              <span v-else class="text-base-content/30">—</span>
            </td>
            <td class="text-sm font-medium text-right">{{ payment.amount }} €</td>
            <td class="text-right">
              <div class="flex justify-end gap-1">
                <NuxtLink :to="`/payments/${payment.id}`" class="btn btn-ghost btn-xs">Modifier</NuxtLink>
                <button class="btn btn-ghost btn-xs text-error" @click="confirmDelete(payment)">Supprimer</button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Delete modal -->
    <dialog ref="deleteModal" class="modal">
      <div class="modal-box">
        <h3 class="font-bold text-lg mb-2">Supprimer ce paiement ?</h3>
        <p class="text-base-content/60 text-sm">
          Vous êtes sur le point de supprimer le paiement <strong>{{ paymentToDelete?.number }}</strong>. Cette action est irréversible.
        </p>
        <div class="modal-action">
          <button class="btn btn-ghost btn-sm" @click="deleteModal.close()">Annuler</button>
          <button class="btn btn-error btn-sm" :class="{ loading: deleting }" @click="deletePayment">Supprimer</button>
        </div>
      </div>
      <form method="dialog" class="modal-backdrop"><button>close</button></form>
    </dialog>

  </div>
</template>

<script setup lang="ts">
definePageMeta({ middleware: 'auth' })

const { token } = useAuth()

const payments = ref<any[]>([])
const loading = ref(true)
const deleting = ref(false)
const paymentToDelete = ref<any>(null)
const deleteModal = ref<HTMLDialogElement>()

async function fetchPayments() {
  loading.value = true
  try {
    payments.value = await $fetch('/api/payments/', {
      headers: { Authorization: `Bearer ${token.value}` }
    })
  } catch {}
  finally { loading.value = false }
}

function confirmDelete(payment: any) {
  paymentToDelete.value = payment
  deleteModal.value?.showModal()
}

async function deletePayment() {
  if (!paymentToDelete.value) return
  deleting.value = true
  try {
    await $fetch(`/api/payments/${paymentToDelete.value.id}`, {
      method: 'DELETE',
      headers: { Authorization: `Bearer ${token.value}` }
    })
    deleteModal.value?.close()
    await fetchPayments()
  } catch {}
  finally { deleting.value = false }
}

function formatDate(d: string) {
  return new Date(d).toLocaleDateString('fr-FR')
}

await fetchPayments()
</script>