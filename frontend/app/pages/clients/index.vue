<template>
  <div>

    <!-- Header -->
    <div class="flex items-center justify-between mb-6">
      <h2 class="text-xl font-bold text-base-content">Clients</h2>
      <NuxtLink to="/clients/new" class="btn btn-primary btn-sm gap-2">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
        </svg>
        Nouveau client
      </NuxtLink>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="flex justify-center py-12">
      <span class="loading loading-spinner loading-md"></span>
    </div>

    <!-- Empty -->
    <div v-else-if="clients.length === 0" class="py-16 flex flex-col items-center text-center">
      <svg xmlns="http://www.w3.org/2000/svg" class="h-12 w-12 text-base-content/20 mb-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0z" />
      </svg>
      <p class="text-base-content/40 font-medium">Aucun client pour l'instant</p>
      <NuxtLink to="/clients/new" class="btn btn-primary btn-sm mt-4">Ajouter un client</NuxtLink>
    </div>

    <!-- Table -->
    <div v-else class="">
      <table class="table table-zebra">
        <thead>
          <tr class="text-base-content/60 text-xs uppercase tracking-wider">
            <th class="w-full">Nom / Société</th>
            <th>Email</th>
            <th>Ville</th>
            <th>SIREN</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="client in clients" :key="client.id" class="hover">
            <td class="w-full">
              <div class="font-medium text-base-content">{{ client.name }}</div>
              <div v-if="client.company_name || client.contact_name" class="text-xs text-base-content/50">
                {{ client.company_name || client.contact_name }}
              </div>
            </td>
            <td class="text-sm text-base-content/70 whitespace-nowrap">{{ client.email }}</td>
            <td class="text-sm text-base-content/70 whitespace-nowrap">{{ client.city ?? '—' }}</td>
            <td class="text-sm text-base-content/70 font-mono whitespace-nowrap">{{ client.siren ?? '—' }}</td>
            <td>
              <div class="dropdown dropdown-end">
                <label tabindex="0" class="btn btn-ghost btn-xs btn-square">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 12h.01M12 12h.01M19 12h.01M6 12a1 1 0 11-2 0 1 1 0 012 0zm7 0a1 1 0 11-2 0 1 1 0 012 0zm7 0a1 1 0 11-2 0 1 1 0 012 0z" />
                  </svg>
                </label>
                <ul tabindex="0" class="dropdown-content menu menu-sm shadow bg-base-100 rounded-box w-36 border border-base-200 z-10">
                  <li><NuxtLink :to="`/clients/${client.id}`">Modifier</NuxtLink></li>
                  <li><a class="text-error" @click="confirmDelete(client)">Supprimer</a></li>
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
        <h3 class="font-bold text-lg mb-2">Supprimer ce client ?</h3>
        <p class="text-base-content/60 text-sm">
          Vous êtes sur le point de supprimer <strong>{{ clientToDelete?.name }}</strong>. Cette action est irréversible.
        </p>
        <div class="modal-action">
          <button class="btn btn-ghost btn-sm" @click="deleteModal.close()">Annuler</button>
          <button class="btn btn-error btn-sm" :class="{ loading: deleting }" @click="deleteClient">Supprimer</button>
        </div>
      </div>
      <form method="dialog" class="modal-backdrop"><button>close</button></form>
    </dialog>

  </div>
</template>

<script setup lang="ts">
definePageMeta({ middleware: 'auth' })

const { token } = useAuth()

const clients = ref<any[]>([])
const loading = ref(true)
const deleting = ref(false)
const clientToDelete = ref<any>(null)
const deleteModal = ref<HTMLDialogElement>()

async function fetchClients() {
  loading.value = true
  try {
    clients.value = await $fetch('/api/clients/', {
      headers: { Authorization: `Bearer ${token.value}` }
    })
  } catch {}
  finally { loading.value = false }
}

function confirmDelete(client: any) {
  clientToDelete.value = client
  deleteModal.value?.showModal()
}

async function deleteClient() {
  if (!clientToDelete.value) return
  deleting.value = true
  try {
    await $fetch(`/api/clients/${clientToDelete.value.id}`, {
      method: 'DELETE',
      headers: { Authorization: `Bearer ${token.value}` }
    })
    deleteModal.value?.close()
    await fetchClients()
  } catch {}
  finally { deleting.value = false }
}

await fetchClients()
</script>