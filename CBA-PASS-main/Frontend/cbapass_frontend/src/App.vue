<template>
  <div id="app">
    <!-- Aquí se inyectan las vistas del router -->
    <router-view />
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()

onMounted(() => {
  auth.restoreSession()
})

</script>

<style>
/* Estilos base globales */
body {
  margin: 0;
  padding: 0;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  background-color: #217074;
}

#app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}
</style>
