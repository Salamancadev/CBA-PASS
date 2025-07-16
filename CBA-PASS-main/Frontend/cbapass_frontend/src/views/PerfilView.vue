<template>
  <div class="container shadow">
    <h1 class="text-center text-white">Mi Perfil</h1>

    <div class="profile-card" v-if="user">
      <p class="text-white fw-bold">
        <strong class="text-white">Usuario:</strong> {{ user.username }}
      </p>
      <p class="text-white fw-bold">
        <strong class="text-white">Nombres:</strong> {{ user.nombres }}
      </p>
      <p class="text-white fw-bold">
        <strong class="text-white">Apellidos:</strong> {{ user.apellidos }}
      </p>
      <p class="text-white fw-bold"><strong class="text-white">Tipo:</strong> {{ user.tipo }}</p>
      <p class="text-white fw-bold">
        <strong class="text-white">Documento:</strong> {{ user.documento }}
      </p>
      <p class="text-white fw-bold">
        <strong class="text-white">Email:</strong> {{ user.email || 'No especificado' }}
      </p>
      <p class="text-white fw-bold">
        <strong class="text-white">Registrado el:</strong> {{ formatFecha(user.creado_en) }}
      </p>
    </div>

    <div class="acciones">
      <button @click="handleLogout">Cerrar sesión</button>
      <router-link to="/" class="text-white fw-bold">Ir al inicio</router-link>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'

const authStore = useAuthStore()
const router = useRouter()

const user = authStore.user

const handleLogout = () => {
  authStore.logout()
  router.push('/login')
}

const formatFecha = (fecha: string) => {
  const date = new Date(fecha)
  return date.toLocaleDateString('es-CO', {
    day: '2-digit',
    month: 'long',
    year: 'numeric',
  })
}
</script>

<style scoped>
.container {
  max-width: 400px;
  margin: 3rem auto;
  padding: 2rem;
  border-radius: 8px;
  background: #87c159;
}

h1 {
  margin-bottom: 2rem;
}

.profile-card p {
  font-size: 1rem;
  margin-bottom: 0.75rem;
  line-height: 1.4;
}

.profile-card {
  background: #2f70af;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.acciones {
  margin-top: 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

button {
  background-color: #f44336;
  color: white;
  border: none;
  padding: 0.7rem 1.2rem;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  font-weight: bold;
  transition: background-color 0.3s ease;
}

button:hover {
  background-color: #d32f2f;
}

a {
  font-size: 1rem;
  background-color: #2f70af;
  text-decoration: none;
  font-weight: bold;
  transition: 0.3s ease;
  border-radius: 4px;

  padding: 0.5rem 1rem;

}
a:hover {
  background-color: #1a5276;
}
</style>
