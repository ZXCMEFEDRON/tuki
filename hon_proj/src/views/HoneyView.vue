<script setup>
import { ref, onBeforeMount, computed } from 'vue'
import axios from 'axios'
import Cookies from 'js-cookie'

onBeforeMount(() => {
  axios.defaults.headers.common['X-CSRFToken'] = Cookies.get('csrftoken')
})

const honeys = ref([])
const groups = ref([])
const newHoney = ref({ name: '', group: '' })
const editHoney = ref({})
const honeyPictureRef = ref(null)
const honeyAddImageUrl = ref(null)
const enlargedImage = ref(null)
const editPictureRef = ref(null)
const editPictureFile = ref(null)

// Фильтры
const filterId = ref('')
const filterName = ref('')
const filterGroup = ref('')

// Статистика
const stats = ref({ count: 0, avg: 0, max: 0, min: 0 })
const showStats = ref(false)

const filteredHoneys = computed(() => {
  let result = honeys.value
  
  if (filterId.value) {
    result = result.filter(h => h.id.toString().includes(filterId.value))
  }
  
  if (filterName.value) {
    result = result.filter(h => h.name.toLowerCase().includes(filterName.value.toLowerCase()))
  }
  
  if (filterGroup.value) {
    result = result.filter(h => h.group == filterGroup.value)
  }
  
  return result
})

async function fetchGroups() {
  const res = await axios.get('/api/groups/')
  groups.value = res.data
}

async function fetchHoneys() {
  const res = await axios.get('/api/honey/')
  honeys.value = res.data
}

async function fetchStats() {
  const res = await axios.get('/api/honey/stats/')
  stats.value = res.data
  showStats.value = true
}

async function exportToExcel() {
  try {
    const response = await axios.get('/api/honey/export-excel/', {
      responseType: 'blob',
      withCredentials: true
    })
    
    const url = window.URL.createObjectURL(new Blob([response.data]))
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', 'honey_export.xlsx')
    document.body.appendChild(link)
    link.click()
    link.remove()
    window.URL.revokeObjectURL(url)
  } catch (error) {
    console.error('Ошибка при экспорте:', error)
  }
}

async function createHoney() {
  if (!newHoney.value.name) return
  
  const formData = new FormData()
  formData.append('name', newHoney.value.name)
  formData.append('group', newHoney.value.group)
  
  if (honeyPictureRef.value?.files[0]) {
    formData.append('picture', honeyPictureRef.value.files[0])
  }
  
  await axios.post('/api/honey/', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  })
  
  newHoney.value = { name: '', group: '' }
  honeyAddImageUrl.value = null
  if (honeyPictureRef.value) honeyPictureRef.value.value = ''
  await fetchHoneys()
  await fetchStats()
}

async function deleteHoney(id) {
  await axios.delete(`/api/honey/${id}/`)
  await fetchHoneys()
  await fetchStats()
}

function openEditModal(honey) {
  editHoney.value = { ...honey }
  editPictureFile.value = null
  if (editPictureRef.value) editPictureRef.value.value = ''
}

async function updateHoney() {
  if (editPictureFile.value) {
    const formData = new FormData()
    formData.append('name', editHoney.value.name)
    formData.append('group', editHoney.value.group)
    formData.append('picture', editPictureFile.value)
    
    await axios.put(`/api/honey/${editHoney.value.id}/`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
  } else {
    await axios.put(`/api/honey/${editHoney.value.id}/`, {
      name: editHoney.value.name,
      group: editHoney.value.group
    })
  }
  
  editPictureFile.value = null
  if (editPictureRef.value) editPictureRef.value.value = ''
  await fetchHoneys()
  await fetchStats()
}

function getGroupName(id) {
  return groups.value.find(g => g.id === id)?.name || '—'
}

function onPictureChange() {
  if (honeyPictureRef.value?.files[0]) {
    honeyAddImageUrl.value = URL.createObjectURL(honeyPictureRef.value.files[0])
  }
}

function onEditPictureChange() {
  if (editPictureRef.value?.files[0]) {
    editPictureFile.value = editPictureRef.value.files[0]
    const previewUrl = URL.createObjectURL(editPictureRef.value.files[0])
    const previewImg = document.getElementById('editHoneyPicturePreview')
    if (previewImg) previewImg.src = previewUrl
  }
}

function openImageModal(imageUrl) {
  enlargedImage.value = imageUrl
  const modalElement = document.getElementById('imageModalHoney')
  if (modalElement) {
    const modal = new bootstrap.Modal(modalElement)
    modal.show()
  }
}

onBeforeMount(async () => {
  await fetchGroups()
  await fetchHoneys()
})
</script>

<template>
  <div>
    <h2>Товары</h2>
    
    <div class="mb-3">
      <button class="btn btn-info" @click="fetchStats">📊 Показать статистику</button>
      <button class="btn btn-success ms-2" @click="exportToExcel">📎 Экспорт в Excel</button>
    </div>
    
    <div v-if="showStats" class="alert alert-info mb-3">
      <h5>Статистика по товарам:</h5>
      <p>📋 Всего записей: {{ stats.count }}</p>
      <p>📊 Средний ID: {{ stats.avg.toFixed(2) }}</p>
      <p>📈 Максимальный ID: {{ stats.max }}</p>
      <p>📉 Минимальный ID: {{ stats.min }}</p>
    </div>
    
    <!-- ФИЛЬТРЫ -->
    <div class="card mb-3">
      <div class="card-header bg-light">
        <strong>🔍 Фильтры</strong>
      </div>
      <div class="card-body">
        <div class="row g-3">
          <div class="col-md-4">
            <label class="form-label">Фильтр по ID</label>
            <input type="text" class="form-control" v-model="filterId" placeholder="Введите ID..." />
          </div>
          <div class="col-md-4">
            <label class="form-label">Фильтр по названию</label>
            <input type="text" class="form-control" v-model="filterName" placeholder="Введите название..." />
          </div>
          <div class="col-md-4">
            <label class="form-label">Фильтр по виду мёда</label>
            <select class="form-select" v-model="filterGroup">
              <option value="">Все</option>
              <option v-for="g in groups" :key="g.id" :value="g.id">{{ g.name }}</option>
            </select>
          </div>
        </div>
        <div class="mt-3">
          <button class="btn btn-sm btn-secondary" @click="filterId = ''; filterName = ''; filterGroup = ''">Сбросить фильтры</button>
        </div>
      </div>
    </div>
    
    <form @submit.prevent="createHoney" class="row g-2 mb-3 align-items-center">
      <div class="col">
        <input class="form-control" v-model="newHoney.name" placeholder="Название товара" required />
      </div>
      <div class="col">
        <select class="form-select" v-model="newHoney.group" required>
          <option value="">Выберите вид</option>
          <option v-for="g in groups" :key="g.id" :value="g.id">{{ g.name }}</option>
        </select>
      </div>
      
      <div class="col-auto">
        <input type="file" class="form-control" ref="honeyPictureRef" @change="onPictureChange" accept="image/*" />
      </div>
      
      <div class="col-auto" v-if="honeyAddImageUrl">
        <img :src="honeyAddImageUrl" style="height: 40px; width: auto;" alt="preview" />
      </div>
      
      <div class="col-auto">
        <button class="btn btn-primary">➕ Добавить</button>
      </div>
    </form>

    <div class="list-group">
      <div v-for="honey in filteredHoneys" :key="honey.id" class="list-group-item d-flex justify-content-between align-items-center">
        <div class="d-flex align-items-center gap-3">
          <img v-if="honey.picture" 
               :src="honey.picture" 
               style="height: 50px; width: auto; cursor: pointer;" 
               @click="openImageModal(honey.picture)"
               class="img-thumbnail" />
          <div>
            <span class="badge bg-secondary me-2">ID: {{ honey.id }}</span>
            {{ honey.name }} — {{ getGroupName(honey.group) }}
          </div>
        </div>
        <div>
          <button class="btn btn-sm btn-success me-2" @click="openEditModal(honey)" data-bs-toggle="modal" data-bs-target="#editHoneyModal">✏️</button>
          <button class="btn btn-sm btn-danger" @click="deleteHoney(honey.id)">✕</button>
        </div>
      </div>
    </div>
    
    <div v-if="filteredHoneys.length === 0 && honeys.length > 0" class="alert alert-warning mt-3">
      Ничего не найдено по заданным фильтрам
    </div>

    <div class="modal fade" id="editHoneyModal" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5>Редактировать товар</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body">
            <div class="mb-3">
              <label class="form-label">Название</label>
              <input class="form-control" v-model="editHoney.name" />
            </div>
            <div class="mb-3">
              <label class="form-label">Вид мёда</label>
              <select class="form-select" v-model="editHoney.group">
                <option v-for="g in groups" :key="g.id" :value="g.id">{{ g.name }}</option>
              </select>
            </div>
            
            <div class="mb-3">
              <label class="form-label">Текущая картинка</label>
              <img v-if="editHoney.picture" :src="editHoney.picture" style="max-height: 100px;" class="d-block mb-2" />
              <p v-else class="text-muted">Нет картинки</p>
              <label class="form-label">Заменить картинку</label>
              <input type="file" class="form-control" ref="editPictureRef" @change="onEditPictureChange" accept="image/*" />
              <img id="editHoneyPicturePreview" style="max-height: 50px; margin-top: 10px;" />
            </div>
          </div>
          <div class="modal-footer">
            <button class="btn btn-secondary" data-bs-dismiss="modal">Отмена</button>
            <button class="btn btn-primary" data-bs-dismiss="modal" @click="updateHoney">Сохранить</button>
          </div>
        </div>
      </div>
    </div>

    <div class="modal fade" id="imageModalHoney" tabindex="-1">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5>Просмотр изображения</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body text-center">
            <img :src="enlargedImage" style="max-width: 100%; max-height: 70vh;" alt="" />
          </div>
          <div class="modal-footer">
            <button class="btn btn-secondary" data-bs-dismiss="modal">Закрыть</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>