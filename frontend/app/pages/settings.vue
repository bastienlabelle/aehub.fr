<template>
  <div class="max-w-2xl">

    <!-- Header -->
    <h2 class="text-xl font-bold text-base-content mb-6">Préférences</h2>

    <!-- Loading -->
    <div v-if="loading" class="flex justify-center py-12">
      <span class="loading loading-spinner loading-md"></span>
    </div>

    <div v-else class="flex flex-col gap-4">

      <!-- Identité -->
      <div class="card bg-base-100 border border-base-300">
        <div class="card-body gap-4">
          <h3 class="font-semibold text-base-content">Identité</h3>

          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">

            <div class="form-control">
              <label class="label"><span class="label-text font-medium">Prénom <span class="text-error">*</span></span></label>
              <input v-model="form.first_name" type="text" placeholder="Jean" class="input input-bordered" :class="{ 'input-error': errors.first_name }" />
              <label v-if="errors.first_name" class="label"><span class="label-text-alt text-error">{{ errors.first_name }}</span></label>
            </div>

            <div class="form-control">
              <label class="label"><span class="label-text font-medium">Nom <span class="text-error">*</span></span></label>
              <input v-model="form.last_name" type="text" placeholder="Dupont" class="input input-bordered" :class="{ 'input-error': errors.last_name }" />
              <label v-if="errors.last_name" class="label"><span class="label-text-alt text-error">{{ errors.last_name }}</span></label>
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

          </div>
        </div>
      </div>

      <!-- Entreprise -->
      <div class="card bg-base-100 border border-base-300">
        <div class="card-body gap-4">
          <h3 class="font-semibold text-base-content">Entreprise</h3>

          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">

            <div class="form-control sm:col-span-2">
              <label class="label"><span class="label-text font-medium">Nom de la société</span></label>
              <input v-model="form.company_name" type="text" placeholder="Dupont SARL" class="input input-bordered" />
            </div>

            <div class="form-control">
              <label class="label"><span class="label-text font-medium">SIREN <span class="text-error">*</span></span></label>
              <input v-model="form.siren" type="text" placeholder="123456789" maxlength="9" class="input input-bordered font-mono" :class="{ 'input-error': errors.siren }" />
              <label v-if="errors.siren" class="label"><span class="label-text-alt text-error">{{ errors.siren }}</span></label>
            </div>

            <div class="form-control">
              <label class="label"><span class="label-text font-medium">SIRET <span class="text-error">*</span></span></label>
              <input v-model="form.siret" type="text" placeholder="12345678900014" maxlength="14" class="input input-bordered font-mono" :class="{ 'input-error': errors.siret }" />
              <label v-if="errors.siret" class="label"><span class="label-text-alt text-error">{{ errors.siret }}</span></label>
            </div>

            <div class="form-control sm:col-span-2">
              <label class="label"><span class="label-text font-medium">Adresse <span class="text-error">*</span></span></label>
              <input v-model="form.address" type="text" placeholder="10 rue de la République" class="input input-bordered" :class="{ 'input-error': errors.address }" />
              <label v-if="errors.address" class="label"><span class="label-text-alt text-error">{{ errors.address }}</span></label>
            </div>

            <div class="form-control">
              <label class="label"><span class="label-text font-medium">Code postal <span class="text-error">*</span></span></label>
              <input v-model="form.zip_code" type="text" placeholder="69001" class="input input-bordered" :class="{ 'input-error': errors.zip_code }" />
              <label v-if="errors.zip_code" class="label"><span class="label-text-alt text-error">{{ errors.zip_code }}</span></label>
            </div>

            <div class="form-control">
              <label class="label"><span class="label-text font-medium">Ville <span class="text-error">*</span></span></label>
              <input v-model="form.city" type="text" placeholder="Lyon" class="input input-bordered" :class="{ 'input-error': errors.city }" />
              <label v-if="errors.city" class="label"><span class="label-text-alt text-error">{{ errors.city }}</span></label>
            </div>

            <div class="form-control">
              <label class="label"><span class="label-text font-medium">Site web</span></label>
              <input v-model="form.website" type="url" placeholder="https://mon-site.fr" class="input input-bordered" />
            </div>

            <div class="form-control">
              <label class="label"><span class="label-text font-medium">IBAN</span></label>
              <input v-model="form.iban" type="text" placeholder="FR76..." class="input input-bordered font-mono" />
            </div>

          </div>
        </div>
      </div>

      <!-- Mot de passe -->
      <div class="card bg-base-100 border border-base-300">
        <div class="card-body gap-4">
          <h3 class="font-semibold text-base-content">Mot de passe</h3>
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div class="form-control">
              <label class="label"><span class="label-text font-medium">Nouveau mot de passe</span></label>
              <input v-model="form.password" type="password" placeholder="Laisser vide pour ne pas changer" class="input input-bordered" />
            </div>
            <div class="form-control">
              <label class="label"><span class="label-text font-medium">Confirmer</span></label>
              <input v-model="passwordConfirm" type="password" placeholder="Confirmer le mot de passe" class="input input-bordered" :class="{ 'input-error': errors.password }" />
              <label v-if="errors.password" class="label"><span class="label-text-alt text-error">{{ errors.password }}</span></label>
            </div>
          </div>
        </div>
      </div>

      <!-- Template de facture -->
      <div class="card bg-base-100 border border-base-300">
        <div class="card-body gap-4">
          <h3 class="font-semibold text-base-content">Template de facture</h3>
          <div class="grid grid-cols-2 sm:grid-cols-3 gap-3">
            <div
              v-for="t in templates"
              :key="t.value"
              class="border-2 rounded-lg p-4 cursor-pointer transition-all"
              :class="form.invoice_template === t.value ? 'border-primary bg-primary/5' : 'border-base-300 hover:border-base-content/30'"
              @click="form.invoice_template = t.value"
            >
              <p class="font-medium text-sm">{{ t.label }}</p>
              <p class="text-xs text-base-content/40 mt-1">{{ t.description }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Catégories de paiement -->
      <div class="card bg-base-100 border border-base-300">
        <div class="card-body gap-4">
          <h3 class="font-semibold text-base-content">Catégories de paiement</h3>
          <div class="form-control">
            <textarea
              v-model="form.payment_categories"
              class="textarea textarea-bordered"
              rows="5"
              placeholder="Développement web&#10;Contenu digital&#10;Conseil"
            ></textarea>
            <label class="label"><span class="label-text-alt text-base-content/40">Une catégorie par ligne</span></label>
          </div>
        </div>
      </div>

      <div v-if="error" class="alert alert-error text-sm py-2">
        <span>{{ error }}</span>
      </div>

      <div v-if="success" class="alert alert-success text-sm py-2">
        <span>Préférences enregistrées avec succès</span>
      </div>

      <div class="flex justify-end">
        <button class="btn btn-primary btn-sm" :class="{ loading: saving }" :disabled="saving" @click="submit">
          Enregistrer
        </button>
      </div>

    </div>
  </div>
</template>

<script setup lang="ts">
definePageMeta({ middleware: 'auth' })

const { token } = useAuth()

const loading = ref(true)
const saving = ref(false)
const error = ref('')
const success = ref(false)
const errors = reactive<Record<string, string>>({})
const passwordConfirm = ref('')

const templates = [
  { value: 'default', label: 'Par défaut', description: 'Template standard' },
  { value: 'swiss-minimal', label: 'Swiss Minimal', description: 'Design épuré, typographie forte' },
  { value: 'modern', label: 'Modern', description: 'Design card avec badges colorés' },
  { value: 'editorial', label: 'Editorial', description: 'Layout éditorial, deux colonnes' },
  { value: 'grid', label: 'Grid', description: 'Design structuré façon tableur' },
  { value: 'fintech', label: 'Fintech', description: 'Design card minimaliste, layout lignes' },
  { value: 'bstn', label: 'BSTN', description: 'Style éditorial noir, mise en page sidebar' },
]

const form = reactive({
  first_name: '',
  last_name: '',
  email: '',
  phone: '',
  company_name: '',
  siren: '',
  siret: '',
  address: '',
  zip_code: '',
  city: '',
  website: '',
  iban: '',
  password: '',
  invoice_template: '',
  payment_categories: '',
})

onMounted(async () => {
  try {
    const user = await $fetch<any>('/api/auth/me', {
      headers: { Authorization: `Bearer ${token.value}` }
    })
    Object.assign(form, {
      first_name: user.first_name ?? '',
      last_name: user.last_name ?? '',
      email: user.email ?? '',
      phone: user.phone ?? '',
      company_name: user.company_name ?? '',
      siren: user.siren ?? '',
      siret: user.siret ?? '',
      address: user.address ?? '',
      zip_code: user.zip_code ?? '',
      city: user.city ?? '',
      website: user.website ?? '',
      iban: user.iban ?? '',
      invoice_template: user.invoice_template ?? 'default',
      payment_categories: user.payment_categories ?? '',
    })
  } catch {
    error.value = 'Impossible de charger les préférences'
  } finally {
    loading.value = false
  }
})

function validate() {
  Object.keys(errors).forEach(k => delete errors[k])
  if (!form.first_name) errors.first_name = 'Champ requis'
  if (!form.last_name) errors.last_name = 'Champ requis'
  if (!form.email) errors.email = 'Champ requis'
  if (!form.siren) errors.siren = 'Champ requis'
  if (!form.siret) errors.siret = 'Champ requis'
  if (!form.address) errors.address = 'Champ requis'
  if (!form.zip_code) errors.zip_code = 'Champ requis'
  if (!form.city) errors.city = 'Champ requis'
  if (form.password && form.password !== passwordConfirm.value) {
    errors.password = 'Les mots de passe ne correspondent pas'
  }
  return Object.keys(errors).length === 0
}

async function submit() {
  if (!validate()) return
  saving.value = true
  error.value = ''
  success.value = false
  try {
    await $fetch('/api/auth/me', {
      method: 'PATCH',
      headers: { Authorization: `Bearer ${token.value}` },
      body: {
        ...form,
        password: form.password || null,
        phone: form.phone || null,
        company_name: form.company_name || null,
        website: form.website || null,
        iban: form.iban || null,
        payment_categories: form.payment_categories || null,
      },
    })
    success.value = true
    setTimeout(() => { success.value = false }, 3000)
  } catch {
    error.value = 'Une erreur est survenue'
  } finally {
    saving.value = false
  }
}
</script>