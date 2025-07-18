<template>
  <div class="container shadow">
    <h1 class="text-center text-white">Mi Perfil</h1>

    <div class="profile-card" v-if="user">
      <!-- Usuario y Email (editable) -->
      <div v-if="editando">
        <p class="text-white fw-bold">
          <strong class="text-white">Usuario:</strong>
          <input v-model="editUser.username" class="input-editar" />
        </p>
        <p class="text-white fw-bold">
          <strong class="text-white">Email:</strong>
          <input v-model="editUser.email" class="input-editar" />
        </p>

      </div>

      <!-- Vista normal -->
      <div v-else>
        <p class="text-white fw-bold">
          <strong class="text-white">Usuario:</strong> {{ user.username }}
        </p>
        <p class="text-white fw-bold">
          <strong class="text-white">Email:</strong> {{ user.email || 'No especificado' }}
        </p>
        <p class="text-white fw-bold">
          <strong class="text-white">Nombres:</strong> {{ user.nombres }}
        </p>
        <p class="text-white fw-bold">
          <strong class="text-white">Apellidos:</strong> {{ user.apellidos }}
        </p>
        <p class="text-white fw-bold">
          <strong class="text-white">Tipo:</strong> {{ user.tipo }}
        </p>
      </div>

      <!-- Campos siempre visibles -->
      <p class="text-white fw-bold">
        <strong class="text-white">Documento:</strong> {{ user.documento }}
      </p>
      <p class="text-white fw-bold">
        <strong class="text-white">Registrado el:</strong> {{ formatFecha(user.creado_en) }}
      </p>

      <!-- Botones -->
      <div class="acciones-editar">
        <button v-if="!editando" @click="editando = true">Editar</button>
        <div v-else>
          <button @click="guardarCambios">Guardar</button>
          <button @click="cancelarEdicion" class="cancelar">Cancelar</button>
        </div>
      </div>
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
import { ref, reactive, watch } from 'vue'

const authStore = useAuthStore()
const router = useRouter()

const editando = ref(false)
const user = ref(authStore.user)  // hacemos esto reactivo

// Editables con fallback a string vacío para evitar errores de tipo
const editUser = reactive({
  username: user.value?.username ?? '',
  email: user.value?.email ?? '',

})

// Si el usuario cambia (por ejemplo, después de un login), actualiza los campos editables
watch(() => authStore.user, (nuevoUsuario) => {
  user.value = nuevoUsuario
  if (nuevoUsuario) {
    editUser.username = nuevoUsuario.username ?? ''
    editUser.email = nuevoUsuario.email ?? ''
  }
})

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

const guardarCambios = async () => {
  console.log('Haciendo petición para guardar cambios...');
  const token = localStorage.getItem('token');
  if (!token) {
    console.error('No hay token de autenticación');
    return;
  }

  try {
    const response = await fetch('http://127.0.0.1:8000/api/perfil/actualizar/', {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({
        username: editUser.username,
        email: editUser.email,

      }),
    });

    const data = await response.json();
    console.log('Respuesta del backend:', data);

    if (response.ok) {
      user.value = data
      Object.assign(editUser, data)
      authStore.user = { ...data }
      editando.value = false
      console.log('Perfil actualizado correctamente')
    } else {
      console.error('Error al actualizar:', data);
      alert(data?.error || 'Error al actualizar el perfil');
    }
  } catch (error) {
    console.error('Error de red:', error);
    alert('Ocurrió un error de red al intentar guardar');
  }
}
const cancelarEdicion = () => {
  if (user.value) {
    editUser.username = user.value.username
    editUser.email = user.value.email

  }
  editando.value = false
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

.input-editar {
  padding: 0.4rem;
  margin-top: 0.2rem;
  border-radius: 4px;
  border: 1px solid #ccc;
  width: 100%;
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

.acciones-editar {
  margin-top: 1rem;
}

button {
  background-color: #f44336;
  color: white;
  border: none;
  padding: 0.6rem 1.1rem;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  font-weight: bold;
  margin-right: 0.5rem;
  transition: background-color 0.3s ease;
}

button:hover {
  background-color: #d32f2f;
}

.cancelar {
  background-color: #888;
}
.cancelar:hover {
  background-color: #666;
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