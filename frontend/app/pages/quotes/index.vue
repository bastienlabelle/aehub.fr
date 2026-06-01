<template>
  <div>

    <!-- Header -->
    <div class="flex items-center justify-between mb-6">
      <h2 class="text-xl font-bold text-base-content">Devis</h2>
      <NuxtLink to="/quotes/new" class="btn btn-primary btn-sm gap-2">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
        </svg>
        Nouveau devis
      </NuxtLink>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="flex justify-center py-12">
      <span class="loading loading-spinner loading-md"></span>
    </div>

    <!-- Empty -->
    <div v-else-if="quotes.length === 0" class="py-16 flex flex-col items-center text-center">
      <svg xmlns="http://www.w3.org/2000/svg" class="h-12 w-12 text-base-content/20 mb-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
      </svg>
      <p class="text-base-content/40 font-medium">Aucun devis pour l'instant</p>
      <NuxtLink to="/quotes/new" class="btn btn-primary btn-sm mt-4">Créer un devis</NuxtLink>
    </div>

    <!-- Table -->
    <div v-else class="overflow-x-auto">

      <table class="table table-zebra">
        <thead>
          <tr class="text-base-content/60 text-xs uppercase tracking-wider">
            <th>Numéro</th>
            <th>Client</th>
            <th>Objet</th>
            <th>Date</th>
            <th>Validité</th>
            <th>Statut</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="quote in quotes" :key="quote.id" class="hover">
            <td class="font-mono text-sm font-medium">{{ quote.number }}</td>
            <td class="text-sm text-base-content/70">{{ quote.client.name }}</td>
            <td class="text-sm text-base-content/70">{{ quote.subject ?? '—' }}</td>
            <td class="text-sm text-base-content/70">{{ formatDate(quote.issued_at) }}</td>
            <td class="text-sm text-base-content/70">{{ quote.valid_until ? formatDate(quote.valid_until) : '—' }}</td>
            <td>
              <span class="badge badge-sm" :class="statusClass(quote.status)">{{ statusLabel(quote.status) }}</span>
            </td>
            <td class="text-right">
              <div class="flex justify-end gap-1">
                <NuxtLink :to="`/quotes/${quote.id}`" class="btn btn-ghost btn-xs">Modifier</NuxtLink>
                <button class="btn btn-ghost btn-xs text-error" @click="confirmDelete(quote)">Supprimer</button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>

    </div>

    <!-- Delete modal -->
    <dialog ref="deleteModal" class="modal">
      <div class="modal-box">
        <h3 class="font-bold text-lg mb-2">Supprimer ce devis ?</h3>
        <p class="text-base-content/60 text-sm">
          Vous êtes sur le point de supprimer le devis <strong>{{ quoteToDelete?.number }}</strong>. Cette action est irréversible.
        </p>
        <div class="modal-action">
          <button class="btn btn-ghost btn-sm" @click="deleteModal.close()">Annuler</button>
          <button class="btn btn-error btn-sm" :class="{ loading: deleting }" @click="deleteQuote">Supprimer</button>
        </div>
      </div>
      <form method="dialog" class="modal-backdrop"><button>close</button></form>
    </dialog>

  </div>
</template>

<script setup lang="ts">
definePageMeta({ middleware: 'auth' })

const { token } = useAuth()

const quotes = ref<any[]>([])
const loading = ref(true)
const deleting = ref(false)
const quoteToDelete = ref<any>(null)
const deleteModal = ref<HTMLDialogElement>()

async function fetchQuotes() {
  loading.value = true
  try {
    quotes.value = await $fetch('/api/quotes/', {
      headers: { Authorization: `Bearer ${token.value}` }
    })
  } catch {}
  finally { loading.value = false }
}

function confirmDelete(quote: any) {
  quoteToDelete.value = quote
  deleteModal.value?.showModal()
}

async function deleteQuote() {
  if (!quoteToDelete.value) return
  deleting.value = true
  try {
    await $fetch(`/api/quotes/${quoteToDelete.value.id}`, {
      method: 'DELETE',
      headers: { Authorization: `Bearer ${token.value}` }
    })
    deleteModal.value?.close()
    await fetchQuotes()
  } catch {}
  finally { deleting.value = false }
}

function formatDate(date: string) {
  return new Date(date).toLocaleDateString('fr-FR')
}

function statusLabel(status: string) {
  const labels: Record<string, string> = {
    draft: 'Brouillon',
    sent: 'Envoyé',
    accepted: 'Accepté',
    refused: 'Refusé',
    expired: 'Expiré',
  }
  return labels[status] ?? status
}

function statusClass(status: string) {
  const classes: Record<string, string> = {
    draft: 'badge-ghost',
    sent: 'badge-info',
    accepted: 'badge-success',
    refused: 'badge-error',
    expired: 'badge-warning',
  }
  return classes[status] ?? 'badge-ghost'
}

await fetchQuotes()
</script>