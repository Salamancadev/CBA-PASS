<template>
  <div class="card">
    <h2>Carnet Virtual</h2>
    <p><strong>Nombre:</strong> {{ persona.nombre }}</p>
    <p><strong>Documento:</strong> {{ persona.documento }}</p>
    <p><strong>Email:</strong> {{ persona.email }}</p>
    <p><strong>Contraseña:</strong> {{ persona.contraseña }}</p>
    <img :src="'data:image/png;base64,' + qr" alt="QR Code">

    <button @click="cancelar">Cancelar</button>
  </div>
</template>

<script>
export default {
  props: {
    persona: {
      type: Object,
      required: true
    },
    qr: {
      type: String,
      required: true
    }
  },
  emits: ['cancelar'],
  methods: {
    cancelar() {
      this.$emit('cancelar')
      window.scrollTo({ top: 0, behavior: 'smooth' })  // ir al inicio
    }
  }
}

</script>

<style scoped>
.card {
  border: 2px solid #0077cc;
  padding: 20px;
  border-radius: 12px;
  width: 300px;
  text-align: center;
  margin: 0 auto;
  margin-top: 20px;
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}
.card img {
  margin-top: 15px;
  width: 150px;
  height: 150px;
}
button {
  margin-top: 20px;
  padding: 8px 16px;
  background-color: #cc0000;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
}
button:hover {
  background-color: #a00000;
}
</style>
