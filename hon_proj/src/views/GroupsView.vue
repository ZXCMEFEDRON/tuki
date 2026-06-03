<script setup>
import { ref, onBeforeMount, computed } from 'vue'
import axios from 'axios'
import Cookies from 'js-cookie'

onBeforeMount(() => {
  axios.defaults.headers.common['X-CSRFToken'] = Cookies.get('csrftoken')
})

const groups = ref([])
const newGroup = ref({ name: '' })
const editGroup = ref({})
const groupPictureRef = ref(null)
const groupAddImageUrl = ref(null)
const enlargedImage = ref(null)
const editPictureRef = ref(null)
const editPictureFile = ref(null)

// Фильтры
const filterName = ref('')
const filterId = ref('')

// Статистика
const stats = ref({ count: 0, avg: 0, max: 0, min: 0 })
const showStats = ref(false)

// Отфильтрованный список
const filteredGroups = computed(() => {
  let result = groups.value
  
  if (filterId.value) {
    result = result.filter(g => g.id.toString().includes(filterId.value))
  }
  
  if (filterName.value) {
    result = result.filter(g => g.name.toLowerCase().includes(filterName.value.toLowerCase()))
  }
  
  return result
})

async function fetchGroups() {
  const res = await axios.get('/api/groups/')
  groups.value = res.data
}

async function fetchStats() {
  const res = await axios.get('/api/groups/stats/')
  stats.value = res.data
  showStats.value = true
}

async function createGroup() {
  if (!newGroup.value.name) return
  
  const formData = new FormData()
  formData.append('name', newGroup.value.name)
  
  if (groupPictureRef.value?.files[0]) {
    formData.append('picture', groupPictureRef.value.files[0])
  }
  
  await axios.post('/api/groups/', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  })
  
  newGroup.value = { name: '' }
  groupAddImageUrl.value = null
  if (groupPictureRef.value) groupPictureRef.value.value = ''
  await fetchGroups()
  await fetchStats()
}

async function deleteGroup(id) {
  await axios.delete(`/api/groups/${id}/`)
  await fetchGroups()
  await fetchStats()
}

function openEditModal(group) {
  editGroup.value = { ...group }
  editPictureFile.value = null
  if (editPictureRef.value) editPictureRef.value.value = ''
}

async function updateGroup() {
  if (editPictureFile.value) {
    const formData = new FormData()
    formData.append('name', editGroup.value.name)
    formData.append('picture', editPictureFile.value)
    
    await axios.put(`/api/groups/${editGroup.value.id}/`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
  } else {
    await axios.put(`/api/groups/${editGroup.value.id}/`, {
      name: editGroup.value.name
    })
  }
  
  editPictureFile.value = null
  if (editPictureRef.value) editPictureRef.value.value = ''
  await fetchGroups()
  await fetchStats()
}

function onPictureChange() {
  if (groupPictureRef.value?.files[0]) {
    groupAddImageUrl.value = URL.createObjectURL(groupPictureRef.value.files[0])
  }
}

function onEditPictureChange() {
  if (editPictureRef.value?.files[0]) {
    editPictureFile.value = editPictureRef.value.files[0]
    const previewUrl = URL.createObjectURL(editPictureRef.value.files[0])
    const previewImg = document.getElementById('editPicturePreview')
    if (previewImg) previewImg.src = previewUrl
  }
}

function openImageModal(imageUrl) {
  enlargedImage.value = imageUrl
  const modalElement = document.getElementById('imageModalGroups')
  if (modalElement) {
    const modal = new bootstrap.Modal(modalElement)
    modal.show()
  }
}

onBeforeMount(async () => {
  await fetchGroups()
})
</script>

<template>
  <div>
    <h2>Виды мёда</h2>
    
    <button class="btn btn-info mb-3" @click="fetchStats">📊 Показать статистику</button>
    
    <div v-if="showStats" class="alert alert-info mb-3">
      <h5>Статистика по видам мёда:</h5>
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
          <div class="col-md-6">
            <label class="form-label">Фильтр по ID</label>
            <input type="text" class="form-control" v-model="filterId" placeholder="Введите ID..." />
          </div>
          <div class="col-md-6">
            <label class="form-label">Фильтр по названию</label>
            <input type="text" class="form-control" v-model="filterName" placeholder="Введите название..." />
          </div>
        </div>
        <div class="mt-3">
          <button class="btn btn-sm btn-secondary" @click="filterId = ''; filterName = ''">Сбросить фильтры</button>
        </div>
      </div>
    </div>
    
    <form @submit.prevent="createGroup" class="row g-2 mb-3 align-items-center">
      <div class="col">
        <input class="form-control" v-model="newGroup.name" placeholder="Название вида" required />
      </div>
      
      <div class="col-auto">
        <input type="file" class="form-control" ref="groupPictureRef" @change="onPictureChange" accept="image/*" />
      </div>
      
      <div class="col-auto" v-if="groupAddImageUrl">
        <img :src="groupAddImageUrl" style="height: 40px; width: auto;" alt="preview" />
      </div>
      
      <div class="col-auto">
        <button class="btn btn-primary">➕ Добавить</button>
      </div>
    </form>

    <div class="list-group">
      <div v-for="group in filteredGroups" :key="group.id" class="list-group-item d-flex justify-content-between align-items-center">
        <div class="d-flex align-items-center gap-3">
          <img v-if="group.picture" 
               :src="group.picture" 
               style="height: 50px; width: auto; cursor: pointer;" 
               @click="openImageModal(group.picture)"
               class="img-thumbnail" />
          <div>
            <span class="badge bg-secondary me-2">ID: {{ group.id }}</span>
            {{ group.name }}
          </div>
        </div>
        <div>
          <button class="btn btn-sm btn-success me-2" @click="openEditModal(group)" data-bs-toggle="modal" data-bs-target="#editGroupModal">✏️</button>
          <button class="btn btn-sm btn-danger" @click="deleteGroup(group.id)">✕</button>
        </div>
      </div>
    </div>
    
    <div v-if="filteredGroups.length === 0 && groups.length > 0" class="alert alert-warning mt-3">
      Ничего не найдено по заданным фильтрам
    </div>

    <div class="modal fade" id="editGroupModal" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5>Редактировать вид</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body">
            <div class="mb-3">
              <label class="form-label">Название</label>
              <input class="form-control" v-model="editGroup.name" />
            </div>
            
            <div class="mb-3">
              <label class="form-label">Текущая картинка</label>
              <img v-if="editGroup.picture" :src="editGroup.picture" style="max-height: 100px;" class="d-block mb-2" />
              <p v-else class="text-muted">Нет картинки</p>
              <label class="form-label">Заменить картинку</label>
              <input type="file" class="form-control" ref="editPictureRef" @change="onEditPictureChange" accept="image/*" />
              <img id="editPicturePreview" style="max-height: 50px; margin-top: 10px;" />
            </div>
          </div>
          <div class="modal-footer">
            <button class="btn btn-secondary" data-bs-dismiss="modal">Отмена</button>
            <button class="btn btn-primary" data-bs-dismiss="modal" @click="updateGroup">Сохранить</button>
          </div>
        </div>
      </div>
    </div>

    <div class="modal fade" id="imageModalGroups" tabindex="-1">
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