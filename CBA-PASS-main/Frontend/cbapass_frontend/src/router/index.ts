import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', name: 'Landing', component: () => import('../views/LandingView.vue') },
    { path: '/login', name: 'Login', component: () => import('../views/LoginView.vue') },
    { path: '/register', name: 'Register', component: () => import('../views/RegisterView.vue') },
    {
      path: '/perfil',
      name: 'Perfil',
      component: () => import('@/views/PerfilView.vue'),
      meta: { requiresAuth: true }, // opcional si quieres protegerla
    },
    {
    path: '/admin/usuarios',
    name: 'AdminUsuarios',
    component: () => import('@/views/AdminUsuarios.vue'),
}
  ],
})


export default router
