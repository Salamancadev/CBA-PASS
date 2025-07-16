<template>
  <div id="app">
    <!-- Aquí se inyectan las vistas del router -->
    <router-view />
  </div>
</template>

<script setup lang="ts">
// No necesitas importar nada aquí todavía
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