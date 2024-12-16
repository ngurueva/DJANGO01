<script setup>
import { onBeforeMount } from 'vue';
import {ref} from 'vue';
import axios from 'axios';
import Cookies from 'js-cookie';
import _ from 'lodash';

const hall = ref([]);
const hallToAdd = ref({});
const hallToEdit = ref({});
const loading = ref(false)
const stats = ref({})

async function fetchHalls() {
  loading.value = true;
  const r = await axios.get("/api/halls/");
  hall.value = r.data;
  loading.value = false;
}

async function fetchStats() {
  loading.value = true;
  const response = await axios.get("/api/halls/stats/");
  stats.value = response.data;
  loading.value = false;
}

onBeforeMount(() => {
  axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken");
})

onBeforeMount(async () => {
  await fetchHalls()
  await fetchStats()
})

async function onHallAdd() {
  await axios.post("/api/halls/", {
    ...hallToAdd.value,
  });
  await fetchHalls();
  hallToAdd.value = {}; 
}

async function onRemoveClick(hall) {
  await axios.delete(`/api/halls/${hall.id}/`);
  await fetchHalls(); 
}

async function onHallsEditClick(hall) {
  hallToEdit.value = { ...hall };
}

async function onUpdateHall() {
  await axios.put(`/api/halls/${hallToEdit.value.id}/`, {
    ...hallToEdit.value,
  });
  await fetchHalls();
}

</script>

<template>
    <div class="container-fluid">
        <div class="modal fade" id="editHallModal" tabindex="-1">
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
                        v-model="hallToEdit.name" required
                      />
                      <label for="floatingInput">Название</label>
                    </div>
                  </div>
                  <div class="col-12">
                    <div class="form-floating mb-2"> 
                      <textarea
                        class="form-control"
                        v-model="hallToEdit.description"
                      ></textarea>
                      <label for="floatingInput">Описание</label>
                    </div>
                  </div>

                  <div class="col-12">
                    <div class="form-floating mb-2"> 
                      <textarea
                        class="form-control"
                        v-model="hallToEdit.location"
                      ></textarea>
                      <label for="floatingInput">Местоположение</label>
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
              @click="onUpdateHall"
            >
              Сохранить
            </button>
          </div>
        </div>
      </div>
    </div>


    <form @submit.prevent.stop="onHallAdd" class="mt-4">
      <div class="row g-3" style="background-color: rgba(255, 255, 255, 0.8); padding: 1rem; border-radius: 8px;">
        <div class="col"> 
          <div class="form-floating">
            <input type="text" class="form-control"
              v-model="hallToAdd.name"
              required
            />
            <label for="floatingInput">Название</label>
          </div>
        </div>
        <div class="col">
            <div class="form-floating mb-2"> 
              <textarea
                class="form-control"
                v-model="hallToAdd.description"
              ></textarea>
              <label for="floatingInput">Описание</label>
            </div>
          </div>
          <div class="col">
            <div class="form-floating mb-2"> 
              <textarea
                class="form-control"
                v-model="hallToAdd.location"
              ></textarea>
              <label for="floatingInput">Местоположение</label>
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
          <div v-for="item in hall" class="hall-item" :key="item.id">
            <div class="hall-details">
              <div class="hall-name">{{ item.name }}</div> 
              <div class="hall-location">Местоположение: {{ item.location }}</div>
              <div class="hall-description">{{ item.description }}</div>
            </div>
            <button class="btn btn-success" @click="onHallsEditClick(item)" data-bs-toggle="modal" data-bs-target="#editHallModal">
              <i class="bi bi-pen-fill"></i>
            </button>
            <button class="btn btn-danger" @click="onRemoveClick(item)"><i class="bi bi-x"></i></button>
          </div>
        </div>
        <div class="col-3 stats">         
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

.hall-item{
  padding: 0.5rem;
  margin: 0.5rem 0;
  border: 1px solid silver;
  border-radius: 8px;
  display: grid;
  grid-template-columns: 1fr auto auto auto;
  align-content: center;
  align-items: center;
  gap: 16px;
  background-color: rgba(255, 255, 255, 0.8);
}


.hall-content {
  display: flex;
  align-items: center;
  flex-grow: 1;
  gap: 32px;
  
  }
  
  .hall-details {
  flex-grow: 1;
  }
  
  .hall-name {
  font-weight: bold;
  }

  .hall-description {
  color: #422F28;
  font-size: 14px;
  }

  .hall-location {
    color: #422F28;
    }
  
  .hall-actions {
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
