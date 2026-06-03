<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '../stores/userStore'

const router = useRouter()
const userStore = useUserStore()

const username = ref('')
const password = ref('')
const error = ref('')
const isLoading = ref(false)

async function handleLogin() {
  if (!username.value || !password.value) {
    error.value = 'Введите имя пользователя и пароль'
    return
  }
  
  isLoading.value = true
  error.value = ''
  
  const success = await userStore.login(username.value, password.value)
  
  if (success) {
    router.push('/')
  } else {
    error.value = 'Неверное имя пользователя или пароль'
  }
  
  isLoading.value = false
}
</script>

<template>
  <div class="container mt-5">
    <div class="row justify-content-center">
      <div class="col-md-6">
        <div class="card">
          <div class="card-header bg-primary text-white">
            <h4 class="mb-0">Авторизация</h4>
          </div>
          <div class="card-body">
            <div v-if="error" class="alert alert-danger">
              {{ error }}
            </div>
            
            <form @submit.prevent="handleLogin">
              <div class="mb-3">
                <label class="form-label">Имя пользователя</label>
                <input 
                  type="text" 
                  class="form-control" 
                  v-model="username" 
                  required
                  autocomplete="username"
                />
              </div>
              
              <div class="mb-3">
                <label class="form-label">Пароль</label>
                <input 
                  type="password" 
                  class="form-control" 
                  v-model="password" 
                  required
                  autocomplete="current-password"
                />
              </div>
              
              <button type="submit" class="btn btn-primary w-100" :disabled="isLoading">
                {{ isLoading ? 'Вход...' : 'Войти' }}
              </button>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>