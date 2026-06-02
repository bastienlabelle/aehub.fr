<template>
  <div class="max-w-2xl">

    <h2 class="text-xl font-bold text-base-content mb-6">Import de données</h2>

    <div class="flex flex-col gap-4">

      <div class="card bg-base-100 border border-base-300">
        <div class="card-body gap-4">
          <h3 class="font-semibold text-base-content">Importer un fichier JSON</h3>
          <p class="text-sm text-base-content/60">
            Le fichier doit respecter le format ÆHUB. Les clients existants (même email) seront mis à jour. Les factures déjà existantes (même numéro) seront ignorées.
          </p>

          <div class="form-control">
            <label class="label"><span class="label-text font-medium">Fichier JSON</span></label>
            <input
              ref="fileInput"
              type="file"
              accept=".json"
              class="file-input file-input-bordered w-full"
              @change="onFileChange"
            />
          </div>

          <div v-if="preview" class="mockup-code text-xs max-h-64 overflow-y-auto">
            <pre>{{ preview }}</pre>
          </div>

          <div v-if="error" class="alert alert-error text-sm py-2">
            <span>{{ error }}</span>
          </div>

          <div class="flex justify-end">
            <button
              class="btn btn-primary btn-sm"
              :class="{ loading }"
              :disabled="loading || !fileData"
              @click="submit"
            >
              Importer
            </button>
          </div>
        </div>
      </div>

      <!-- Résultat -->
      <div v-if="result" class="card bg-base-100 border border-base-300">
        <div class="card-body gap-3">
          <h3 class="font-semibold text-base-content">Résultat de l'import</h3>

          <div class="grid grid-cols-2 gap-3">
            <div class="stat bg-base-200 rounded-lg px-4 py-3">
              <div class="stat-title text-xs">Clients créés</div>
              <div class="stat-value text-lg">{{ result.clients_created }}</div>
            </div>
            <div class="stat bg-base-200 rounded-lg px-4 py-3">
              <div class="stat-title text-xs">Clients mis à jour</div>
              <div class="stat-value text-lg">{{ result.clients_updated }}</div>
            </div>
            <div class="stat bg-base-200 rounded-lg px-4 py-3">
              <div class="stat-title text-xs">Factures importées</div>
              <div class="stat-value text-lg">{{ result.invoices_created }}</div>
            </div>
            <div class="stat bg-base-200 rounded-lg px-4 py-3">
              <div class="stat-title text-xs">Factures ignorées</div>
              <div class="stat-value text-lg">{{ result.invoices_skipped }}</div>
            </div>
            <div class="stat bg-base-200 rounded-lg px-4 py-3">
              <div class="stat-title text-xs">Paiements importés</div>
              <div class="stat-value text-lg">{{ result.payments_created }}</div>
            </div>
            <div class="stat bg-base-200 rounded-lg px-4 py-3">
              <div class="stat-title text-xs">Paiements ignorés</div>
              <div class="stat-value text-lg">{{ result.payments_skipped }}</div>
            </div>
          </div>

          <div v-if="result.errors.length" class="flex flex-col gap-1 mt-2">
            <p class="text-sm font-medium text-warning">Avertissements :</p>
            <ul class="text-sm text-base-content/60 list-disc list-inside">
              <li v-for="(err, i) in result.errors" :key="i">{{ err }}</li>
            </ul>
          </div>

          <div v-else class="alert alert-success text-sm py-2">
            <span>Import terminé sans erreur !</span>
          </div>

        </div>
      </div>

    </div>
  </div>
</template>

<script setup lang="ts">
definePageMeta({ middleware: 'auth' })

const { token } = useAuth()

const fileInput = ref<HTMLInputElement>()
const fileData = ref<any>(null)
const preview = ref('')
const loading = ref(false)
const error = ref('')
const result = ref<any>(null)

function onFileChange(event: Event) {
  error.value = ''
  result.value = null
  const file = (event.target as HTMLInputElement).files?.[0]
  if (!file) return

  const reader = new FileReader()
  reader.onload = (e) => {
    try {
      const text = e.target?.result as string
      fileData.value = JSON.parse(text)
      preview.value = JSON.stringify(fileData.value, null, 2)
    } catch {
      error.value = 'Fichier JSON invalide'
      fileData.value = null
      preview.value = ''
    }
  }
  reader.readAsText(file)
}

async function submit() {
  if (!fileData.value) return
  loading.value = true
  error.value = ''
  result.value = null
  try {
    result.value = await $fetch('/api/import/', {
      method: 'POST',
      headers: { Authorization: `Bearer ${token.value}` },
      body: fileData.value,
    })
  } catch {
    error.value = 'Une erreur est survenue lors de l\'import'
  } finally {
    loading.value = false
  }
}
</script>