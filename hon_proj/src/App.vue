<script setup>
import { useRouter } from 'vue-router'
import { useUserStore } from './stores/userStore'

const router = useRouter()
const userStore = useUserStore()

const tabs = [
  { name: 'Виды мёда', path: '/groups' },
  { name: 'Товары', path: '/honey' },
  { name: 'Остатки', path: '/stock' },
  { name: 'Заказы', path: '/orders' },
  { name: 'Отзывы', path: '/feedback' }
]

function logout() {
  userStore.logout()
  router.push('/login')
}
</script>

<template>
  <div id="app">
    <nav class="navbar navbar-dark bg-dark mb-4">
      <div class="container">
        <span class="navbar-brand">Магазин мёда</span>
        <div class="d-flex gap-3 align-items-center">
          <span v-if="userStore.isAuthenticated" class="text-white">
            👤 {{ userStore.user?.username }}
          </span>
          <a href="/admin" class="btn btn-warning btn-sm">Админка</a>
          <button v-if="userStore.isAuthenticated" @click="logout" class="btn btn-danger btn-sm">
            Выйти
          </button>
        </div>
      </div>
    </nav>

    <div class="container">
      <ul class="nav nav-tabs mb-4" v-if="userStore.isAuthenticated">
        <li class="nav-item" v-for="tab in tabs" :key="tab.path">
          <a class="nav-link" :class="{ active: $route.path === tab.path }" 
             @click.prevent="router.push(tab.path)" href="#">
            {{ tab.name }}
          </a>
        </li>
      </ul>

      <router-view />
    </div>
  </div>
</template>

<style scoped>
.nav-link {
  cursor: pointer;
}
</style>