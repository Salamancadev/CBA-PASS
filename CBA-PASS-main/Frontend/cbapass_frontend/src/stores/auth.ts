import { defineStore } from 'pinia'
import axios from 'axios'

interface Usuario {
  username: string
  nombres: string
  apellidos: string
  tipo: string
  documento: string
  email?: string
}

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: null as string | null,
    user: null as Usuario | null,
  }),
  actions: {
    async login(username: string, password: string) {
      try {
        const res = await axios.post('http://127.0.0.1:8000/api/token/', {
          username,
          password,
        })
        this.token = res.data.access
        axios.defaults.headers.common['Authorization'] = `Bearer ${this.token}`
        await this.fetchPerfil()
        alert('Inicio de sesión exitoso')
      } catch (err) {
        alert('Error al iniciar sesión')
      }
    },

    async register(data: {
      username: string
      password: string
      nombres: string
      apellidos: string
      tipo: string
      documento: string
      email?: string
    }) {
      try {
        const res = await axios.post('http://127.0.0.1:8000/api/register/', data)
        alert('Registro exitoso')
      } catch (error) {
        if (axios.isAxiosError(error)) {
          alert('Error al registrar: ' + (error.response?.data?.error || 'Error desconocido'))
        } else {
          alert('Error inesperado')
        }
      }
    },

    async fetchPerfil() {
      try {
        const res = await axios.get('http://127.0.0.1:8000/api/perfil/')
        this.user = res.data
      } catch (error) {
        alert('Error al obtener perfil')
      }
    },

    logout() {
      this.token = null
      this.user = null
      delete axios.defaults.headers.common['Authorization']
    }
  },
})