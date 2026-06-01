<template>
  <div class="max-w-2xl">

    <!-- Header -->
    <div class="flex items-center gap-3 mb-6">
      <NuxtLink to="/clients" class="btn btn-ghost btn-sm btn-circle">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
        </svg>
      </NuxtLink>
      <h2 class="text-xl font-bold text-base-content">Nouveau client</h2>
    </div>

    <div class="card bg-base-100 border border-base-300">
      <div class="card-body gap-5">

        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">

          <div class="form-control sm:col-span-2">
            <label class="label"><span class="label-text font-medium">Nom <span class="text-error">*</span></span></label>
            <input v-model="form.name" type="text" placeholder="Ex: Dupont SARL ou Jean Dupont" class="input input-bordered" :class="{ 'input-error': errors.name }" />
            <label v-if="errors.name" class="label"><span class="label-text-alt text-error">{{ errors.name }}</span></label>
          </div>

          <div class="form-control">
            <label class="label"><span class="label-text font-medium">Nom du contact</span></label>
            <input v-model="form.contact_name" type="text" placeholder="Jean Dupont" class="input input-bordered" />
          </div>

          <div class="form-control">
            <label class="label"><span class="label-text font-medium">Société</span></label>
            <input v-model="form.company_name" type="text" placeholder="Dupont SARL" class="input input-bordered" />
          </div>

          <div class="form-control">
            <label class="label"><span class="label-text font-medium">Email <span class="text-error">*</span></span></label>
            <input v-model="form.email" type="email" placeholder="jean@exemple.fr" class="input input-bordered" :class="{ 'input-error': errors.email }" />
            <label v-if="errors.email" class="label"><span class="label-text-alt text-error">{{ errors.email }}</span></label>
          </div>

          <div class="form-control">
            <label class="label"><span class="label-text font-medium">Téléphone</span></label>
            <input v-model="form.phone" type="tel" placeholder="0612345678" class="input input-bordered" />
          </div>

          <div class="form-control sm:col-span-2">
            <label class="label"><span class="label-text font-medium">Adresse</span></label>
            <input v-model="form.address" type="text" placeholder="10 rue de la République" class="input input-bordered" />
          </div>

          <div class="form-control">
            <label class="label"><span class="label-text font-medium">Code postal</span></label>
            <input v-model="form.zip_code" type="text" placeholder="69001" class="input input-bordered" />
          </div>

          <div class="form-control">
            <label class="label"><span class="label-text font-medium">Ville</span></label>
            <input v-model="form.city" type="text" placeholder="Lyon" class="input input-bordered" />
          </div>

          <div class="form-control">
            <label class="label"><span class="label-text font-medium">SIREN</span></label>
            <input v-model="form.siren" type="text" placeholder="123456789" maxlength="9" class="input input-bordered font-mono" />
          </div>

          <div class="form-control">
            <label class="label"><span class="label-text font-medium">SIRET</span></label>
            <input v-model="form.siret" type="text" placeholder="12345678900014" maxlength="14" class="input input-bordered font-mono" />
          </div>

        </div>

        <div v-if="error" class="alert alert-error text-sm py-2">
          <span>{{ error }}</span>
        </div>

        <div class="flex justify-end gap-2 pt-2">
          <NuxtLink to="/clients" class="btn btn-ghost btn-sm">Annuler</NuxtLink>
          <button class="btn btn-primary btn-sm" :class="{ loading }" :disabled="loading" @click="submit">
            Créer le client
          </button>
        </div>

      </div>
    </div>

  </div>
</template>

<script setup lang="ts">
definePageMeta({ middleware: 'auth' })

const { token } = useAuth()
const router = useRouter()

const form = reactive({
  name: '',
  contact_name: '',
  company_name: '',
  email: '',
  phone: '',
  address: '',
  zip_code: '',
  city: '',
  siren: '',
  siret: '',
})

const errors = reactive<Record<string, string>>({})
const error = ref('')
const loading = ref(false)

function validate() {
  Object.keys(errors).forEach(k => delete errors[k])
  if (!form.name) errors.name = 'Champ requis'
  if (!form.email) errors.email = 'Champ requis'
  return Object.keys(errors).length === 0
}

async function submit() {
  if (!validate()) return
  loading.value = true
  error.value = ''
  try {
    await $fetch('/api/clients/', {
      method: 'POST',
      headers: { Authorization: `Bearer ${token.value}` },
      body: {
        ...form,
        contact_name: form.contact_name || null,
        company_name: form.company_name || null,
        phone: form.phone || null,
        address: form.address || null,
        zip_code: form.zip_code || null,
        city: form.city || null,
        siren: form.siren || null,
        siret: form.siret || null,
      },
    })
    router.push('/clients')
  } catch {
    error.value = 'Une erreur est survenue'
  } finally {
    loading.value = false
  }
}
</script>