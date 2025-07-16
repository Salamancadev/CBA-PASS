<template>
  <div class="container shadow">
    <h1 class="text-center text-white mb-4">Registro</h1>
    <form @submit.prevent="handleRegister">
      <input v-model="form.username" placeholder="Nombre de usuario" required />
      <input v-model="form.password" type="password" placeholder="Contraseña" required />
      <input v-model="form.nombres" placeholder="Nombres" required />
      <input v-model="form.apellidos" placeholder="Apellidos" required />
      <select v-model="form.tipo" required>
        <option disabled value="">Tipo de usuario</option>
        <option value="aprendiz">Aprendiz</option>
        <option value="instructor">Instructor</option>
        <option value="administrativo">Administrativo</option>
        <option value="visitante">Visitante</option>
      </select>
      <input v-model="form.documento" placeholder="Documento" required />
      <input v-model="form.email" placeholder="Email (opcional)" />
      <button type="submit">Registrarse</button>
    </form>

    <div class="extra-links">
      <p class="text-center text-white fw-semibold">¿Ya tienes una cuenta? <router-link to="/login">Ingresa aquí</router-link></p>
      <router-link to="/">Ir al inicio</router-link>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'

const form = reactive({
  username: '',
  password: '',
  nombres: '',
  apellidos: '',
  tipo: '',
  documento: '',
  email: ''
})

const authStore = useAuthStore()
const router = useRouter()

const handleRegister = async () => {
  await authStore.register(form)
  router.push('/login')
}
</script>

<style scoped>
.container {
  max-width: 500px;
  margin: 3rem auto;
  padding: 2rem;
  border-radius: 8px;
  background: #87C159;
}
input, select {
  width: 100%;
  border-style: none;
  border-radius: 4px;
  margin-bottom: 1rem;
  padding: 0.5rem;
}
button {
  width: 100%;
    border-radius: 4px;

  padding: 0.75rem;
  background-color: #30acb3;
  color: white;
  border: none;
  cursor: pointer;
  font-size: 1rem;
  font-weight: bold;
  transition: background-color 0.3s ease;
}
button:hover {
  background-color: #258a8f;
}
.extra-links {
  margin-top: 1.5rem;
  text-align: center;
}
.extra-links a {
  color: #fff;
  font-weight: bold;
  text-decoration: underline;
  text-decoration: none;
}
</style>
