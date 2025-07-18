<template>
  <div class="min-vh-100 d-flex flex-column text-light">
    <!-- Header -->
    <header class="text-white py-4 shadow rounded my-4">
      <div class="container d-flex justify-content-between align-items-center">
        <h1 class="h3 mb-0 fw-bold">
          <img src="/public/images/logo.png" class="logo" alt="CBA PASS Logo" />CBA PASS
        </h1>
        <div>
          <RouterLink to="/login" class="btn btn-light fw-bold me-2">Iniciar sesión</RouterLink>
          <RouterLink to="/register" class="btn btn-light fw-bold">Registrarse</RouterLink>
        </div>
      </div>
    </header>

    <!-- Sección principal -->
    <main class="flex-grow-1 d-flex rounded align-items-center justify-content-center px-3 shadow">
      <div class="container text-center py-5">
        <h2 class="display-4 fw-bold mb-3">Sistema inteligente de control de acceso</h2>
        <p class="lead mb-4">
          CBA PASS es una solución híbrida (web y móvil) para controlar el ingreso y salida de
          aprendices, visitantes e instructores del SENA CBA Mosquera.
        </p>
        <RouterLink to="/register" class="btn btn-light btn-lg rounded-pill shadow-sm px-5">
          Comenzar ahora
        </RouterLink>
      </div>
    </main>

    <!-- Footer -->
    <footer class="text-center text-white fw-bold py-3 my-4 rounded shadow">
      &copy; 2025 CBA PASS | Proyecto de control de acceso SENA
    </footer>
  </div>
</template>

<script setup lang="ts">
// No necesitas lógica adicional aún
</script>
<style scoped>
body {
  background-color: #217074;
}
main {
  background-color: #258a8f;
}
.logo {
  width: 100px;
  height: auto;
}
footer {
  background-color: #258a8f;
}
header {
  background-color: #87c159;
}
</style>
