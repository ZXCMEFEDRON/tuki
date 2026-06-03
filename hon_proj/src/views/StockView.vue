<script setup>
import { ref, onBeforeMount, computed } from 'vue'
import axios from 'axios'
import Cookies from 'js-cookie'

onBeforeMount(() => {
  axios.defaults.headers.common['X-CSRFToken'] = Cookies.get('csrftoken')
})

const stocks = ref([])
const groups = ref([])
const newStock = ref({ name: '', group: '', count: null })
const editStock = ref({})
const stockPictureRef = ref(null)
const stockAddImageUrl = ref(null)
const enlargedImage = ref(null)
const editPictureRef = ref(null)
const editPictureFile = ref(null)

// Фильтры
const filterId = ref('')
const filterName = ref('')
const filterGroup = ref('')
const filterCountMin = ref('')
const filterCountMax = ref('')

// Статистика
const stats = ref({ count: 0, avg: 0, max: 0, min: 0 })
const showStats = ref(false)

const filteredStocks = computed(() => {
  let result = stocks.value
  
  if (filterId.value) {
    result = result.filter(s => s.id.toString().includes(filterId.value))
  }
  
  if (filterName.value) {
    result = result.filter(s => s.name.toLowerCase().includes(filterName.value.toLowerCase()))
  }
  
  if (filterGroup.value) {
    result = result.filter(s => s.group == filterGroup.value)
  }
  
  if (filterCountMin.value) {
    result = result.filter(s => s.count >= Number(filterCountMin.value))
  }
  
  if (filterCountMax.value) {
    result = result.filter(s => s.count <= Number(filterCountMax.value))
  }
  
  return result
})

async function fetchGroups() {
  const res = await axios.get('/api/groups/')
  groups.value = res.data
}

async function fetchStocks() {
  const res = await axios.get('/api/stock/')
  stocks.value = res.data
}

async function fetchStats() {
  const res = await axios.get('/api/stock/stats/')
  stats.value = res.data
  showStats.value = true
}

async function createStock() {
  if (!newStock.value.name) return
  
  const formData = new FormData()
  formData.append('name', newStock.value.name)
  formData.append('group', newStock.value.group)
  formData.append('count', newStock.value.count)
  
  if (stockPictureRef.value?.files[0]) {
    formData.append('picture', stockPictureRef.value.files[0])
  }
  
  await axios.post('/api/stock/', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  })
  
  newStock.value = { name: '', group: '', count: null }
  stockAddImageUrl.value = null
  if (stockPictureRef.value) stockPictureRef.value.value = ''
  await fetchStocks()
  await fetchStats()
}

async function deleteStock(id) {
  await axios.delete(`/api/stock/${id}/`)
  await fetchStocks()
  await fetchStats()
}

function openEditModal(stock) {
  editStock.value = { ...stock }
  editPictureFile.value = null
  if (editPictureRef.value) editPictureRef.value.value = ''
}

async function updateStock() {
  if (editPictureFile.value) {
    const formData = new FormData()
    formData.append('name', editStock.value.name)
    formData.append('group', editStock.value.group)
    formData.append('count', editStock.value.count)
    formData.append('picture', editPictureFile.value)
    
    await axios.put(`/api/stock/${editStock.value.id}/`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
  } else {
    await axios.put(`/api/stock/${editStock.value.id}/`, {
      name: editStock.value.name,
      group: editStock.value.group,
      count: editStock.value.count
    })
  }
  
  editPictureFile.value = null
  if (editPictureRef.value) editPictureRef.value.value = ''
  await fetchStocks()
  await fetchStats()
}

function getGroupName(id) {
  return groups.value.find(g => g.id === id)?.name || '—'
}

function onPictureChange() {
  if (stockPictureRef.value?.files[0]) {
    stockAddImageUrl.value = URL.createObjectURL(stockPictureRef.value.files[0])
  }
}

function onEditPictureChange() {
  if (editPictureRef.value?.files[0]) {
    editPictureFile.value = editPictureRef.value.files[0]
    const previewUrl = URL.createObjectURL(editPictureRef.value.files[0])
    const previewImg = document.getElementById('editStockPicturePreview')
    if (previewImg) previewImg.src = previewUrl
  }
}

function openImageModal(imageUrl) {
  enlargedImage.value = imageUrl
  const modalElement = document.getElementById('imageModalStock')
  if (modalElement) {
    const modal = new bootstrap.Modal(modalElement)
    modal.show()
  }
}

onBeforeMount(async () => {
  await fetchGroups()
  await fetchStocks()
})
</script>

<template>
  <div>
    <h2>Остатки мёда</h2>
    
    <button class="btn btn-info mb-3" @click="fetchStats">📊 Показать статистику</button>
    
    <div v-if="showStats" class="alert alert-info mb-3">
      <h5>Статистика по остаткам:</h5>
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
            <label class="form-label">Фильтр по названию</label>
            <input type="text" class="form-control" v-model="filterName" placeholder="Введите название..." />
          </div>
          <div class="col-md-3">
            <label class="form-label">Фильтр по виду</label>
            <select class="form-select" v-model="filterGroup">
              <option value="">Все</option>
              <option v-for="g in groups" :key="g.id" :value="g.id">{{ g.name }}</option>
            </select>
          </div>
          <div class="col-md-3">
            <label class="form-label">Фильтр по количеству</label>
            <div class="d-flex gap-2">
              <input type="number" class="form-control" v-model="filterCountMin" placeholder="от" />
              <input type="number" class="form-control" v-model="filterCountMax" placeholder="до" />
            </div>
          </div>
        </div>
        <div class="mt-3">
          <button class="btn btn-sm btn-secondary" @click="filterId = ''; filterName = ''; filterGroup = ''; filterCountMin = ''; filterCountMax = ''">Сбросить фильтры</button>
        </div>
      </div>
    </div>
    
    <form @submit.prevent="createStock" class="row g-2 mb-3 align-items-center">
      <div class="col">
        <input class="form-control" v-model="newStock.name" placeholder="Название" required />
      </div>
      <div class="col">
        <select class="form-select" v-model="newStock.group" required>
          <option value="">Выберите вид</option>
          <option v-for="g in groups" :key="g.id" :value="g.id">{{ g.name }}</option>
        </select>
      </div>
      <div class="col">
        <input class="form-control" v-model.number="newStock.count" type="number" placeholder="Литры" required />
      </div>
      
      <div class="col-auto">
        <input type="file" class="form-control" ref="stockPictureRef" @change="onPictureChange" accept="image/*" />
      </div>
      
      <div class="col-auto" v-if="stockAddImageUrl">
        <img :src="stockAddImageUrl" style="height: 40px; width: auto;" alt="preview" />
      </div>
      
      <div class="col-auto">
        <button class="btn btn-primary">➕ Добавить остаток</button>
      </div>
    </form>

    <div class="list-group">
      <div v-for="stock in filteredStocks" :key="stock.id" class="list-group-item d-flex justify-content-between align-items-center">
        <div class="d-flex align-items-center gap-3">
          <img v-if="stock.picture" 
               :src="stock.picture" 
               style="height: 50px; width: auto; cursor: pointer;" 
               @click="openImageModal(stock.picture)"
               class="img-thumbnail" />
          <div>
            <span class="badge bg-secondary me-2">ID: {{ stock.id }}</span>
            <strong>{{ stock.name }}</strong>
            <span class="text-muted ms-2">({{ getGroupName(stock.group) }})</span>
            <span class="badge bg-info ms-2">{{ stock.count }} литров</span>
          </div>
        </div>
        <div>
          <button class="btn btn-sm btn-success me-2" @click="openEditModal(stock)" data-bs-toggle="modal" data-bs-target="#editStockModal">✏️</button>
          <button class="btn btn-sm btn-danger" @click="deleteStock(stock.id)">✕</button>
        </div>
      </div>
    </div>
    
    <div v-if="filteredStocks.length === 0 && stocks.length > 0" class="alert alert-warning mt-3">
      Ничего не найдено по заданным фильтрам
    </div>

    <div class="modal fade" id="editStockModal" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5>Редактировать остаток</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body">
            <div class="mb-3">
              <label class="form-label">Название</label>
              <input class="form-control" v-model="editStock.name" />
            </div>
            <div class="mb-3">
              <label class="form-label">Вид мёда</label>
              <select class="form-select" v-model="editStock.group">
                <option v-for="g in groups" :key="g.id" :value="g.id">{{ g.name }}</option>
              </select>
            </div>
            <div class="mb-3">
              <label class="form-label">Количество (литры)</label>
              <input class="form-control" v-model.number="editStock.count" type="number" />
            </div>
            
            <div class="mb-3">
              <label class="form-label">Текущая картинка</label>
              <img v-if="editStock.picture" :src="editStock.picture" style="max-height: 100px;" class="d-block mb-2" />
              <p v-else class="text-muted">Нет картинки</p>
              <label class="form-label">Заменить картинку</label>
              <input type="file" class="form-control" ref="editPictureRef" @change="onEditPictureChange" accept="image/*" />
              <img id="editStockPicturePreview" style="max-height: 50px; margin-top: 10px;" />
            </div>
          </div>
          <div class="modal-footer">
            <button class="btn btn-secondary" data-bs-dismiss="modal">Отмена</button>
            <button class="btn btn-primary" data-bs-dismiss="modal" @click="updateStock">Сохранить</button>
          </div>
        </div>
      </div>
    </div>

    <div class="modal fade" id="imageModalStock" tabindex="-1">
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