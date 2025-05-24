import { createRouter, createWebHistory } from 'vue-router'
import AddCharacter from '../components/AddCharacter.vue'
import ViewCharacter from '../components/ViewCharacter.vue'
import EditCharacter from '@/components/EditCharacter.vue'

const routes = [
  { path: '/add', component: AddCharacter },
  { path: '/view', component: ViewCharacter },
  { path: '/', redirect: '/view' },
  { path: '/edit/:id', component: EditCharacter}
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
})

export default router
