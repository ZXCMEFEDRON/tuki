<script setup>
import { ref, onBeforeMount, computed } from 'vue'
import axios from 'axios'
import Cookies from 'js-cookie'

onBeforeMount(() => {
  axios.defaults.headers.common['X-CSRFToken'] = Cookies.get('csrftoken')
})

const feedbacks = ref([])
const groups = ref([])
const newFeedback = ref({ name: '', group: '', comment: '' })
const editFeedback = ref({})
const feedbackPictureRef = ref(null)
const feedbackAddImageUrl = ref(null)
const enlargedImage = ref(null)
const editFeedbackPictureRef = ref(null)
const editFeedbackPictureFile = ref(null)

// Фильтры
const filterId = ref('')
const filterName = ref('')
const filterGroup = ref('')
const filterComment = ref('')

// Статистика
const stats = ref({ count: 0, avg: 0, max: 0, min: 0 })
const showStats = ref(false)

const filteredFeedbacks = computed(() => {
  let result = feedbacks.value
  
  if (filterId.value) {
    result = result.filter(f => f.id.toString().includes(filterId.value))
  }
  
  if (filterName.value) {
    result = result.filter(f => f.name.toLowerCase().includes(filterName.value.toLowerCase()))
  }
  
  if (filterGroup.value) {
    result = result.filter(f => f.group == filterGroup.value)
  }
  
  if (filterComment.value) {
    result = result.filter(f => f.comment.toLowerCase().includes(filterComment.value.toLowerCase()))
  }
  
  return result
})

async function fetchGroups() {
  const res = await axios.get('/api/groups/')
  groups.value = res.data
}

async function fetchFeedbacks() {
  const res = await axios.get('/api/feedback/')
  feedbacks.value = res.data
}

async function fetchStats() {
  const res = await axios.get('/api/feedback/stats/')
  stats.value = res.data
  showStats.value = true
}

async function createFeedback() {
  if (!newFeedback.value.name || !newFeedback.value.comment) return
  
  const formData = new FormData()
  formData.append('name', newFeedback.value.name)
  formData.append('group', newFeedback.value.group)
  formData.append('comment', newFeedback.value.comment)
  
  if (feedbackPictureRef.value?.files[0]) {
    formData.append('picture', feedbackPictureRef.value.files[0])
  }
  
  await axios.post('/api/feedback/', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  })
  
  newFeedback.value = { name: '', group: '', comment: '' }
  feedbackAddImageUrl.value = null
  if (feedbackPictureRef.value) feedbackPictureRef.value.value = ''
  await fetchFeedbacks()
  await fetchStats()
}

async function deleteFeedback(id) {
  await axios.delete(`/api/feedback/${id}/`)
  await fetchFeedbacks()
  await fetchStats()
}

function openEditModal(feedback) {
  editFeedback.value = { ...feedback }
  editFeedbackPictureFile.value = null
  if (editFeedbackPictureRef.value) editFeedbackPictureRef.value.value = ''
}

async function updateFeedback() {
  if (editFeedbackPictureFile.value) {
    const formData = new FormData()
    formData.append('name', editFeedback.value.name)
    formData.append('group', editFeedback.value.group)
    formData.append('comment', editFeedback.value.comment)
    formData.append('picture', editFeedbackPictureFile.value)
    
    await axios.put(`/api/feedback/${editFeedback.value.id}/`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
  } else {
    await axios.put(`/api/feedback/${editFeedback.value.id}/`, editFeedback.value)
  }
  
  editFeedbackPictureFile.value = null
  if (editFeedbackPictureRef.value) editFeedbackPictureRef.value.value = ''
  await fetchFeedbacks()
  await fetchStats()
}

function getGroupName(id) {
  return groups.value.find(g => g.id === id)?.name || '—'
}

function onPictureChange() {
  if (feedbackPictureRef.value?.files[0]) {
    feedbackAddImageUrl.value = URL.createObjectURL(feedbackPictureRef.value.files[0])
  }
}

function onEditPictureChange() {
  if (editFeedbackPictureRef.value?.files[0]) {
    editFeedbackPictureFile.value = editFeedbackPictureRef.value.files[0]
    const previewUrl = URL.createObjectURL(editFeedbackPictureRef.value.files[0])
    const previewImg = document.getElementById('editFeedbackPicturePreview')
    if (previewImg) previewImg.src = previewUrl
  }
}

function openImageModal(imageUrl) {
  enlargedImage.value = imageUrl
  const modalElement = document.getElementById('imageModalFeedback')
  if (modalElement) {
    const modal = new bootstrap.Modal(modalElement)
    modal.show()
  }
}

onBeforeMount(async () => {
  await fetchGroups()
  await fetchFeedbacks()
})
</script>

<template>
  <div>
    <h2>Отзывы о мёде</h2>
    
    <button class="btn btn-info mb-3" @click="fetchStats">📊 Показать статистику</button>
    
    <div v-if="showStats" class="alert alert-info mb-3">
      <h5>Статистика по отзывам:</h5>
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
          <div class="col-md-3">
            <label class="form-label">Фильтр по ID</label>
            <input type="text" class="form-control" v-model="filterId" placeholder="Введите ID..." />
          </div>
          <div class="col-md-3">
            <label class="form-label">Фильтр по имени</label>
            <input type="text" class="form-control" v-model="filterName" placeholder="Введите имя..." />
          </div>
          <div class="col-md-3">
            <label class="form-label">Фильтр по виду</label>
            <select class="form-select" v-model="filterGroup">
              <option value="">Все</option>
              <option v-for="g in groups" :key="g.id" :value="g.id">{{ g.name }}</option>
            </select>
          </div>
          <div class="col-md-3">
            <label class="form-label">Фильтр по отзыву</label>
            <input type="text" class="form-control" v-model="filterComment" placeholder="Введите текст..." />
          </div>
        </div>
        <div class="mt-3">
          <button class="btn btn-sm btn-secondary" @click="filterId = ''; filterName = ''; filterGroup = ''; filterComment = ''">Сбросить фильтры</button>
        </div>
      </div>
    </div>
    
    <form @submit.prevent="createFeedback" class="row g-2 mb-3 align-items-center">
      <div class="col-md-3">
        <input class="form-control" v-model="newFeedback.name" placeholder="Ваше имя" required />
      </div>
      <div class="col-md-3">
        <select class="form-select" v-model="newFeedback.group" required>
          <option value="">Выберите вид</option>
          <option v-for="g in groups" :key="g.id" :value="g.id">{{ g.name }}</option>
        </select>
      </div>
      <div class="col-md-3">
        <textarea class="form-control" v-model="newFeedback.comment" placeholder="Ваш отзыв" rows="1" required></textarea>
      </div>
      
      <div class="col-auto">
        <input type="file" class="form-control" ref="feedbackPictureRef" @change="onPictureChange" accept="image/*" />
      </div>
      
      <div class="col-auto" v-if="feedbackAddImageUrl">
        <img :src="feedbackAddImageUrl" style="height: 40px; width: auto;" alt="preview" />
      </div>
      
      <div class="col-auto">
        <button class="btn btn-primary">➕ Добавить отзыв</button>
      </div>
    </form>

    <div class="list-group">
      <div v-for="feedback in filteredFeedbacks" :key="feedback.id" class="list-group-item d-flex justify-content-between align-items-start">
        <div class="flex-grow-1">
          <div class="d-flex align-items-center gap-3">
            <img v-if="feedback.picture" 
                 :src="feedback.picture" 
                 style="height: 50px; width: auto; cursor: pointer;" 
                 @click="openImageModal(feedback.picture)"
                 class="img-thumbnail" />
            <div>
              <span class="badge bg-secondary me-2">ID: {{ feedback.id }}</span>
              <strong>{{ feedback.name }}</strong>
              <span class="badge bg-secondary ms-2">{{ getGroupName(feedback.group) }}</span>
              <p class="mb-0 mt-2 text-muted">{{ feedback.comment }}</p>
            </div>
          </div>
        </div>
        <div class="ms-3">
          <button class="btn btn-sm btn-success me-2" @click="openEditModal(feedback)" data-bs-toggle="modal" data-bs-target="#editFeedbackModal">✏️</button>
          <button class="btn btn-sm btn-danger" @click="deleteFeedback(feedback.id)">✕</button>
        </div>
      </div>
    </div>
    
    <div v-if="filteredFeedbacks.length === 0 && feedbacks.length > 0" class="alert alert-warning mt-3">
      Ничего не найдено по заданным фильтрам
    </div>

    <div class="modal fade" id="editFeedbackModal" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5>Редактировать отзыв</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body">
            <div class="mb-3">
              <label class="form-label">Имя</label>
              <input class="form-control" v-model="editFeedback.name" />
            </div>
            <div class="mb-3">
              <label class="form-label">Вид мёда</label>
              <select class="form-select" v-model="editFeedback.group">
                <option v-for="g in groups" :key="g.id" :value="g.id">{{ g.name }}</option>
              </select>
            </div>
            <div class="mb-3">
              <label class="form-label">Отзыв</label>
              <textarea class="form-control" v-model="editFeedback.comment" rows="3"></textarea>
            </div>
            
            <div class="mb-3">
              <label class="form-label">Текущая картинка</label>
              <img v-if="editFeedback.picture" :src="editFeedback.picture" style="max-height: 100px;" class="d-block mb-2" />
              <p v-else class="text-muted">Нет картинки</p>
              <label class="form-label">Заменить картинку</label>
              <input type="file" class="form-control" ref="editFeedbackPictureRef" @change="onEditPictureChange" accept="image/*" />
              <img id="editFeedbackPicturePreview" style="max-height: 50px; margin-top: 10px;" />
            </div>
          </div>
          <div class="modal-footer">
            <button class="btn btn-secondary" data-bs-dismiss="modal">Отмена</button>
            <button class="btn btn-primary" data-bs-dismiss="modal" @click="updateFeedback">Сохранить</button>
          </div>
        </div>
      </div>
    </div>

    <div class="modal fade" id="imageModalFeedback" tabindex="-1">
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