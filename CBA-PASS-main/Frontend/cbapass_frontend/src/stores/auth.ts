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
    token: localStorage.getItem('token') || '',
    user: null as Usuario | null,
  }),
  actions: {
    async login(username: string, password: string): Promise<boolean> {
  try {
    const res = await axios.post('http://127.0.0.1:8000/api/token/', {
      username,
      password,
    });

    this.token = res.data.access || '';
    localStorage.setItem('token', this.token);
    axios.defaults.headers.common['Authorization'] = `Bearer ${this.token}`;

    await this.fetchPerfil();
    alert('Inicio de sesión exitoso');
    return true;
  } catch (err) {
    alert('Error al iniciar sesión');
    this.token = '';
    localStorage.removeItem('token'); // Limpia token viejo
    return false;
  }
},

    async register(userData: Usuario & { password: string }) {
      try {
        await axios.post('http://127.0.0.1:8000/api/register/', userData)
        alert('Registro exitoso. Ahora puedes iniciar sesión.')
      } catch (error) {
        alert('Error al registrar usuario')
        console.error(error)
      }
    },

    async fetchPerfil() {
      try {
        if (this.token) {
          axios.defaults.headers.common['Authorization'] = `Bearer ${this.token}`
        }
        const res = await axios.get('http://127.0.0.1:8000/api/perfil/')
        this.user = res.data
      } catch (error) {
        alert('Error al obtener perfil')
      }
    },

    restoreSession() {
      const token = localStorage.getItem('token')
      if (token) {
        this.token = token
        axios.defaults.headers.common['Authorization'] = `Bearer ${token}`
      }
    },

    logout() {
      this.token = ''
      this.user = null
      localStorage.removeItem('token')
      delete axios.defaults.headers.common['Authorization']
    },
  },
})
