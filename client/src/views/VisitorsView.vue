<script setup>
import { onBeforeMount } from 'vue';
import {computed, ref} from 'vue';
import axios from 'axios';
import Cookies from 'js-cookie';
import _ from 'lodash';
// import { storeToRefs } from 'pinia';

// const userProfileStore = UserProfileViewSet();
// const {
//   is_authenticated, 
//   name
// } = storeToRefs(userProfileStore);

const visitors = ref([]);
const visitorToAdd = ref({});
const visitorToEdit = ref({});
const loading = ref(false);
const exhibitions = ref([]);
const stats = ref({})


const exhibitionsById = computed(() => {
  return _.keyBy(exhibitions.value, 'id');
});

async function fetchExhibitions() {
  loading.value = true;
  const r = await axios.get("/api/exhibitions/");
  exhibitions.value = r.data;
  loading.value = false;
}

async function fetchStats() {
  loading.value = true;
  const response = await axios.get("/api/visitors/stats/");
  stats.value = response.data;
  loading.value = false;
}

async function fetchVisitors() {
  loading.value = true;
  const r = await axios.get("/api/visitors/");
  visitors.value = r.data;
  loading.value = false;
}

onBeforeMount(() => {
  axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken");
})

onBeforeMount(async () => {
  await fetchExhibitions()
  await fetchVisitors()
  await fetchStats()
})

async function onVisitorsAdd() {
  await axios.post("/api/visitors/", {
    ...visitorToAdd.value,
  });
  await fetchVisitors(); 
  visitorToAdd.value = {};
}

async function onRemoveClick(visitor) {
  await axios.delete(`/api/visitors/${visitor.id}/`);
  await fetchVisitors(); 
}

async function onVisitorsEditClick(visitor) {
  visitorToEdit.value = { ...visitor };
}

async function onUpdateVisitor() {
  await axios.put(`/api/visitors/${visitorToEdit.value.id}/`, {
    ...visitorToEdit.value,
  });
  await fetchVisitors();
}






</script>

<template>
    <div class="container-fluid">
        <div class="modal fade" id="editVisitorModal" tabindex="-1">
          <div class="modal-dialog">
            <div class="modal-content">
              <div class="modal-header">
                <h1 class="modal-title fs-5" id="exampleModalLabel">
                  Редактировать
                </h1>
                <button
                  type="button"
                  class="btn-close"
                  data-bs-dismiss="modal"
                  aria-label="Close"
                ></button>
              </div>
              <div class="modal-body">
                <div class="row">
                  <div class="col-12">
                    <div class="form-floating mb-2"> 
                      <input
                        type="text"
                        class="form-control"
                        v-model="visitorToEdit.first_name" required
                      />
                      <label for="floatingInput">Имя</label>
                    </div>
                  </div>
                  <div class="col-12">
                    <div class="form-floating mb-2"> 
                      <input
                        type="text"
                        class="form-control"
                        v-model="visitorToEdit.last_name" required
                      />
                      <label for="floatingInput">Фамилия</label>
                    </div>
                  </div>
                  


                  <div class="col-12">
                    <div class="form-floating mb-2">
                      <input 
                        type="email"
                        class="form-control"
                        v-model="visitorToEdit.email"
                        required
                      />
                      <label for="floatingInput">Почта</label>
                    </div>
                  </div>
          
                  <div class="col-12">
                    <div class="form-floating mb-2">
                      <input 
                        type="text" 
                        class="form-control"
                        v-model="visitorToEdit.phone_number"
                        required 
                        maxlength="20"  
                      />
                      <label for="floatingInput">Номер телефона</label>
                    </div>
                  </div>
                
                  <div class="col-12">
                    <div class="form-floating mb-2">
                      <select class="form-select" v-model="visitorToEdit.exhibition" required>
                        <option :value="e.id" v-for="e in exhibitions">{{ e.name }}</option>
                      </select>
                      <label for="floatingInput">Выставка</label>
                    </div>
                  </div>
            </div>
          </div>
          <div class="modal-footer">
            <button
              type="button"
              class="btn btn-secondary"
              data-bs-dismiss="modal"
            >
              Закрыть
            </button>
            <button
              data-bs-dismiss="modal"
              type="button"
              class="btn btn-primary"
              @click="onUpdateVisitor"
            >
              Сохранить
            </button>
          </div>
        </div>
      </div>
    </div>


    <form @submit.prevent.stop="onVisitorsAdd" class="mt-4">
      <div class="row g-3" style="background-color: rgba(255, 255, 255, 0.8); padding: 1rem; border-radius: 8px;">
        <div class="col"> 
          <div class="form-floating">
            <input type="text" class="form-control"
              v-model="visitorToAdd.first_name"
              required
            />
            <label for="floatingInput">Имя</label>
          </div>
        </div>
        <div class="col"> 
          <div class="form-floating">
            <input type="text" class="form-control"
              v-model="visitorToAdd.last_name"
              required
            />
            <label for="floatingInput">Фамилия</label>
          </div>
        </div>

        <div class="col">
          <div class="form-floating">
            <input 
              type="email"
              class="form-control"
              v-model="visitorToAdd.email"
              required
            />
            <label for="floatingInput">Почта</label>
          </div>
        </div>

        <div class="col">
          <div class="form-floating">
            <input 
              type="text" 
              class="form-control"
              v-model="visitorToAdd.phone_number"
              required 
              maxlength="20"  
            />
            <label for="floatingInput">Номер телефона</label>
          </div>
        </div>
        
        

        <div class="col">
          <div class="form-floating">
            <select class="form-select" v-model="visitorToAdd.exhibition" required>
              <option :value="e.id" v-for="e in exhibitions">{{ e.name }}</option>
            </select>
            <label for="floatingInput">Выставка</label>
          </div>
        </div>
        
        <div class="col-auto">
          <button class="btn btn-primary">
            Добавить
          </button>
        </div>
      </div>
    </form>



      <div class="row">
        <div class="col-9">
          <div v-for="item in visitors" class="visitor-item" :key="item.id">
            <div class="visitor-details">
              <div class="visitor-name">{{ item.first_name + " " + item.last_name}}</div> 
              <div class="visitor-email">{{ item.email }}</div>
              <div class="visitor-phone_number">{{ item.phone_number }}</div>
            </div>
            <button class="btn btn-success" @click="onVisitorsEditClick(item)" data-bs-toggle="modal" data-bs-target="#editVisitorModal">
              <i class="bi bi-pen-fill"></i>
            </button>
            <button class="btn btn-danger" @click="onRemoveClick(item)"><i class="bi bi-x"></i></button>
          </div>
        </div>
        <div class="col-3 stats" style="">
        <h4>Статистика</h4>
          <p>Количество: {{ stats.count }}</p>
          <p>Средний ID: {{ stats.avg }}</p>
          <p>Максимальный ID: {{ stats.max }}</p>
          <p>Минимальный ID: {{ stats.min }}</p>
      </div>
    </div>


    </div>
</template>

<style lang="scss" scoped>
.visitor-item{
  padding: 0.5rem;
  margin: 0.5rem 0;
  border: 1px solid silver;
  border-radius: 8px;
  display: grid;
  grid-template-columns: 1fr auto auto auto;
  align-content: center;
  align-items: center;
  gap: 16px;
  background-color: rgba(255, 255, 255, 0.8) ;
}

  .visitor-content {
  display: flex;
  align-items: center;
  flex-grow: 1;
  gap: 32px;
  
  }
  
  .visitor-details {
  flex-grow: 1;
  }
  
  .visitor-name {
  font-weight: bold;
  }

  .visitor-description {
  color: #422F28;
  font-size: 14px;
  }
  
  .visitor-actions {
  display: flex;
  align-items: flex-start; 
  gap: 8px;
  }
  .stats{
    padding: 1rem; 
    margin: 0.5rem 0; 
    border-radius: 8px; 
    background-color: rgba(255, 255, 255, 0.8) ; 
    position:sticky; 
    top: 0; 
    max-width:fit-content;
    max-height:fit-content;
    align-items: center;
    flex-grow: 1;
    gap: 32px;
    margin: 1rem 0;
    gap: 16px;
  }
</style>
