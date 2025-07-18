<template>
  <div class="container shadow">
    <h1 class="text-center text-white">Iniciar Sesión</h1>
    <form @submit.prevent="handleLogin">
      <input v-model="username" placeholder="Nombre de usuario" required />
      <input v-model="password" type="password" placeholder="Contraseña" required />
      <button type="submit">Ingresar</button>
    </form>

    <div class="extra-links">
      <p class="text-center text-white fw-semibold">
        ¿No estás registrado? <router-link to="/register">Regístrate aquí</router-link>
      </p>
      <router-link to="/">Ir al inicio</router-link>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const username = ref('')
const password = ref('')
const authStore = useAuthStore()
const router = useRouter()

const handleLogin = async () => {
  await authStore.login(username.value, password.value)

  // Esperamos fetchPerfil y revisamos si tiene un tipo válido
  if (authStore.token) {
    await authStore.fetchPerfil()

    const tipoUsuario = authStore.user?.tipo?.toLowerCase()

    console.log('Tipo de usuario:', tipoUsuario)

    if (tipoUsuario === 'administrativo') {
      router.push('/admin/usuarios')
    } else if (tipoUsuario === 'aprendiz' || tipoUsuario === 'seguridad') {
      router.push('/perfil')
    } else {
      alert('Tipo de usuario no reconocido')
    }
  } else {
    alert('Error en el login')
  }
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
input {
  display: block;
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
