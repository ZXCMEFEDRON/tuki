<script setup>
import { ref, onBeforeMount, computed } from 'vue'
import axios from 'axios'
import Cookies from 'js-cookie'

onBeforeMount(() => {
  axios.defaults.headers.common['X-CSRFToken'] = Cookies.get('csrftoken')
})

const orders = ref([])
const groups = ref([])
const newOrder = ref({ name: '', group: '', count: null })
const editOrder = ref({})
const orderPictureRef = ref(null)
const orderAddImageUrl = ref(null)
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

const filteredOrders = computed(() => {
  let result = orders.value
  
  if (filterId.value) {
    result = result.filter(o => o.id.toString().includes(filterId.value))
  }
  
  if (filterName.value) {
    result = result.filter(o => o.name.toLowerCase().includes(filterName.value.toLowerCase()))
  }
  
  if (filterGroup.value) {
    result = result.filter(o => o.group == filterGroup.value)
  }
  
  if (filterCountMin.value) {
    result = result.filter(o => o.count >= Number(filterCountMin.value))
  }
  
  if (filterCountMax.value) {
    result = result.filter(o => o.count <= Number(filterCountMax.value))
  }
  
  return result
})

async function fetchGroups() {
  const res = await axios.get('/api/groups/')
  groups.value = res.data
}

async function fetchOrders() {
  const res = await axios.get('/api/orders/')
  orders.value = res.data
}

async function fetchStats() {
  const res = await axios.get('/api/orders/stats/')
  stats.value = res.data
  showStats.value = true
}

async function createOrder() {
  if (!newOrder.value.name) return
  
  const formData = new FormData()
  formData.append('name', newOrder.value.name)
  formData.append('group', newOrder.value.group)
  formData.append('count', newOrder.value.count)
  
  if (orderPictureRef.value?.files[0]) {
    formData.append('picture', orderPictureRef.value.files[0])
  }
  
  await axios.post('/api/orders/', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  })
  
  newOrder.value = { name: '', group: '', count: null }
  orderAddImageUrl.value = null
  if (orderPictureRef.value) orderPictureRef.value.value = ''
  await fetchOrders()
  await fetchStats()
}

async function deleteOrder(id) {
  await axios.delete(`/api/orders/${id}/`)
  await fetchOrders()
  await fetchStats()
}

function openEditModal(order) {
  editOrder.value = { ...order }
  editPictureFile.value = null
  if (editPictureRef.value) editPictureRef.value.value = ''
}

async function updateOrder() {
  if (editPictureFile.value) {
    const formData = new FormData()
    formData.append('name', editOrder.value.name)
    formData.append('group', editOrder.value.group)
    formData.append('count', editOrder.value.count)
    formData.append('picture', editPictureFile.value)
    
    await axios.put(`/api/orders/${editOrder.value.id}/`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
  } else {
    await axios.put(`/api/orders/${editOrder.value.id}/`, {
      name: editOrder.value.name,
      group: editOrder.value.group,
      count: editOrder.value.count
    })
  }
  
  editPictureFile.value = null
  if (editPictureRef.value) editPictureRef.value.value = ''
  await fetchOrders()
  await fetchStats()
}

function getGroupName(id) {
  return groups.value.find(g => g.id === id)?.name || '—'
}

function onPictureChange() {
  if (orderPictureRef.value?.files[0]) {
    orderAddImageUrl.value = URL.createObjectURL(orderPictureRef.value.files[0])
  }
}

function onEditPictureChange() {
  if (editPictureRef.value?.files[0]) {
    editPictureFile.value = editPictureRef.value.files[0]
    const previewUrl = URL.createObjectURL(editPictureRef.value.files[0])
    const previewImg = document.getElementById('editOrderPicturePreview')
    if (previewImg) previewImg.src = previewUrl
  }
}

function openImageModal(imageUrl) {
  enlargedImage.value = imageUrl
  const modalElement = document.getElementById('imageModalOrder')
  if (modalElement) {
    const modal = new bootstrap.Modal(modalElement)
    modal.show()
  }
}

onBeforeMount(async () => {
  await fetchGroups()
  await fetchOrders()
})
</script>

<template>
  <div>
    <h2>Заказы</h2>
    
    <button class="btn btn-info mb-3" @click="fetchStats">📊 Показать статистику</button>
    
    <div v-if="showStats" class="alert alert-info mb-3">
      <h5>Статистика по заказам:</h5>
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
    
    <form @submit.prevent="createOrder" class="row g-2 mb-3 align-items-center">
      <div class="col">
        <input class="form-control" v-model="newOrder.name" placeholder="Название заказа" required />
      </div>
      <div class="col">
        <select class="form-select" v-model="newOrder.group" required>
          <option value="">Выберите вид</option>
          <option v-for="g in groups" :key="g.id" :value="g.id">{{ g.name }}</option>
        </select>
      </div>
      <div class="col">
        <input class="form-control" v-model.number="newOrder.count" type="number" placeholder="Литры" required />
      </div>
      
      <div class="col-auto">
        <input type="file" class="form-control" ref="orderPictureRef" @change="onPictureChange" accept="image/*" />
      </div>
      
      <div class="col-auto" v-if="orderAddImageUrl">
        <img :src="orderAddImageUrl" style="height: 40px; width: auto;" alt="preview" />
      </div>
      
      <div class="col-auto">
        <button class="btn btn-primary">➕ Добавить заказ</button>
      </div>
    </form>

    <div class="list-group">
      <div v-for="order in filteredOrders" :key="order.id" class="list-group-item d-flex justify-content-between align-items-center">
        <div class="d-flex align-items-center gap-3">
          <img v-if="order.picture" 
               :src="order.picture" 
               style="height: 50px; width: auto; cursor: pointer;" 
               @click="openImageModal(order.picture)"
               class="img-thumbnail" />
          <div>
            <span class="badge bg-secondary me-2">ID: {{ order.id }}</span>
            <strong>{{ order.name }}</strong>
            <span class="text-muted ms-2">({{ getGroupName(order.group) }})</span>
            <span class="badge bg-warning ms-2">{{ order.count }} литров</span>
          </div>
        </div>
        <div>
          <button class="btn btn-sm btn-success me-2" @click="openEditModal(order)" data-bs-toggle="modal" data-bs-target="#editOrderModal">✏️</button>
          <button class="btn btn-sm btn-danger" @click="deleteOrder(order.id)">✕</button>
        </div>
      </div>
    </div>
    
    <div v-if="filteredOrders.length === 0 && orders.length > 0" class="alert alert-warning mt-3">
      Ничего не найдено по заданным фильтрам
    </div>

    <div class="modal fade" id="editOrderModal" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5>Редактировать заказ</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body">
            <div class="mb-3">
              <label class="form-label">Название</label>
              <input class="form-control" v-model="editOrder.name" />
            </div>
            <div class="mb-3">
              <label class="form-label">Вид мёда</label>
              <select class="form-select" v-model="editOrder.group">
                <option v-for="g in groups" :key="g.id" :value="g.id">{{ g.name }}</option>
              </select>
            </div>
            <div class="mb-3">
              <label class="form-label">Количество (литры)</label>
              <input class="form-control" v-model.number="editOrder.count" type="number" />
            </div>
            
            <div class="mb-3">
              <label class="form-label">Текущая картинка</label>
              <img v-if="editOrder.picture" :src="editOrder.picture" style="max-height: 100px;" class="d-block mb-2" />
              <p v-else class="text-muted">Нет картинки</p>
              <label class="form-label">Заменить картинку</label>
              <input type="file" class="form-control" ref="editPictureRef" @change="onEditPictureChange" accept="image/*" />
              <img id="editOrderPicturePreview" style="max-height: 50px; margin-top: 10px;" />
            </div>
          </div>
          <div class="modal-footer">
            <button class="btn btn-secondary" data-bs-dismiss="modal">Отмена</button>
            <button class="btn btn-primary" data-bs-dismiss="modal" @click="updateOrder">Сохранить</button>
          </div>
        </div>
      </div>
    </div>

    <div class="modal fade" id="imageModalOrder" tabindex="-1">
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