<template>
    <div class="Caja">
      <div class="qr">
          <qrcode-vue :value="qrData" :size="200" level="h" />
      </div>
      <div>
        <h4>Tiempo de expiracion: {{ tiempoRestante }}</h4>
        <button @click="Salir" >Salir</button>
      </div>
    </div>
</template>

<script setup >
import { useAuthStore } from '@/stores/auth'
import QrcodeVue from 'qrcode.vue'
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const tiempoRestante = ref(300) // 5 minutos = 300 segundos
const authStore = useAuthStore()

onMounted(() => {
  // Temporizador de cuenta regresiva cada segundo
  const intervalo = setInterval(() => {
    tiempoRestante.value--
    if (tiempoRestante.value <= 0) {
      clearInterval(intervalo)
      router.push('/') // Redirigir al inicio
    }
  }, 1000)
})

const Salir = () => {
  authStore.logout()
  router.push('/')
}

</script>

<style scoped>

.Caja{
  border-radius: 20px;
  border:  2px solid black;
  margin: 10rem;
  padding: 3rem;
  background: white;
}
.qr{
  display: flex;
  justify-content: center;
  padding-bottom: 5rem;
}
button{
  background: red;
  font-size: larger;
  width: 5rem;
  border-radius: 10px;
  display: flex;
  justify-content: center;
}

h4{
  color: black;
}
</style>