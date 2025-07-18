<template>
  <div class="p-6">
    <h2 class="text-2xl font-bold mb-4">Administración de Usuarios</h2>

    <!-- Botón para volver al inicio -->
    <button @click="$router.push('/')" class="btn volver">Volver al Inicio</button>

    <table class="w-full table-auto border-collapse border border-gray-300">
      <thead>
        <tr class="bg-gray-200">
          <th class="border px-4 py-2">ID</th>
          <th class="border px-4 py-2">Usuario</th>
          <th class="border px-4 py-2">Email</th>
          <th class="border px-4 py-2">Tipo</th>
          <th class="border px-4 py-2">Documento</th>
          <th class="border px-4 py-2">Acciones</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="usuario in usuarios" :key="usuario.id">
          <td class="border px-4 py-2">{{ usuario.id }}</td>
          <td class="border px-4 py-2">
            <input v-if="usuario.editando" v-model="usuario.username" class="border p-1 w-full" />
            <span v-else>{{ usuario.username }}</span>
          </td>
          <td class="border px-4 py-2">
            <input v-if="usuario.editando" v-model="usuario.email" class="border p-1 w-full" />
            <span v-else>{{ usuario.email }}</span>
          </td>
          <td class="border px-4 py-2">
            <select
              v-if="usuario.editando"
              v-model="usuario.tipo"
              class="border p-1 w-full rounded"
            >
              <option v-for="opcion in tiposDisponibles" :key="opcion" :value="opcion">
                {{ capitalize(opcion) }}
              </option>
            </select>
            <span v-else>{{ capitalize(usuario.tipo) }}</span>
          </td>
          <td class="border px-4 py-2">
            <input v-if="usuario.editando" v-model="usuario.documento" class="border p-1 w-full" />
            <span v-else>{{ usuario.documento }}</span>
          </td>
          <td class="border px-4 py-2 space-x-2">
            <button v-if="usuario.editando" @click="guardarUsuario(usuario)" class="btn guardar">
              Guardar
            </button>

            <button v-else @click="editarUsuario(usuario)" class="btn editar">Editar</button>

            <button @click="eliminarUsuario(usuario.id)" class="btn eliminar">Eliminar</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const tiposDisponibles = ['aprendiz', 'instructor', 'administrativo', 'visitante']
const usuarios = ref([])

const token = localStorage.getItem('token')

const obtenerUsuarios = async () => {
  try {
    const response = await fetch('http://localhost:8000/api/usuarios/', {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })
    const data = await response.json()
    usuarios.value = data.map((usuario) => ({
      ...usuario,
      editando: false,
    }))
  } catch (error) {
    console.error('Error al obtener usuarios:', error)
  }
}

const editarUsuario = (usuario) => {
  usuario.editando = true
}

const guardarUsuario = async (usuario) => {
  const payload = {
    username: usuario.username,
    email: usuario.email,
    tipo: usuario.tipo,
    documento: usuario.documento,
    nombres: usuario.nombres, // 👈 nuevo
    apellidos: usuario.apellidos, // 👈 nuevo
  }

  console.log('Payload que se va a enviar:', payload)

  try {
    const response = await fetch(`http://localhost:8000/api/usuarios/${usuario.id}/`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify(payload),
    })

    const data = await response.json()
    console.log('Respuesta del backend:', data)

    if (response.ok) {
      usuario.editando = false
      alert('Usuario actualizado correctamente.')
      await obtenerUsuarios()
    } else {
      alert('Error al guardar cambios: ' + JSON.stringify(data))
    }
  } catch (error) {
    console.error('Error al actualizar usuario:', error)
    alert('Error de red al guardar cambios.')
  }
}

const eliminarUsuario = async (id) => {
  if (confirm('¿Estás seguro de que deseas eliminar este usuario?')) {
    try {
      const response = await fetch(`http://localhost:8000/api/usuarios/${id}/`, {
        method: 'DELETE',
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })
      if (response.ok) {
        usuarios.value = usuarios.value.filter((usuario) => usuario.id !== id)
        alert('Usuario eliminado correctamente.')
      } else {
        const data = await response.json()
        alert(data?.error || 'No se pudo eliminar el usuario.')
      }
    } catch (error) {
      console.error('Error al eliminar usuario:', error)
      alert('No se pudo eliminar el usuario.')
    }
  }
}

const capitalize = (str) => str.charAt(0).toUpperCase() + str.slice(1)

onMounted(obtenerUsuarios)
</script>

<style scoped>
.btn {
  color: white;
  padding: 0.25rem 0.75rem; /* py-1 px-3 */
  border-radius: 0.375rem; /* rounded */
  border: none;
  cursor: pointer;
  font-size: 1rem;
  transition: background-color 0.3s ease;
}

/* Guardar - verde */
.guardar {
  background-color: #22c55e; /* bg-green-500 */
}
.guardar:hover {
  background-color: #16a34a; /* hover:bg-green-600 */
}

/* Editar - azul */
.editar {
  background-color: #3b82f6; /* bg-blue-500 */
}
.editar:hover {
  background-color: #2563eb; /* hover:bg-blue-600 */
}

/* Eliminar - rojo */
.eliminar {
  background-color: #ef4444; /* bg-red-500 */
}
.eliminar:hover {
  background-color: #dc2626; /* hover:bg-red-600 */
}

.volver {
  background-color: #374151; /* bg-gray-700 */
}

.volver:hover {
  background-color: #1f2937; /* hover:bg-gray-800 */
}
</style>
