<script setup>
import { onBeforeMount } from 'vue';
import {computed, ref} from 'vue';
import axios from 'axios';
import Cookies from 'js-cookie';
import _ from 'lodash';

const collections = ref([]);
const collectionToAdd = ref({});
const collectionToEdit = ref({});
const loading = ref(false)
const stats = ref({})

async function fetchCollections() {
  loading.value = true;
  const r = await axios.get("/api/collections/");
  collections.value = r.data;
  loading.value = false;
}

async function fetchStats() {
  loading.value = true;
  const response = await axios.get("/api/collections/stats/");
  stats.value = response.data;
  loading.value = false;
}

onBeforeMount(() => {
  axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken");
})

onBeforeMount(async () => {
  await fetchCollections()
  await fetchStats()
})

async function onCollectionsAdd() {
  await axios.post("/api/collections/", {
    ...collectionToAdd.value,
  });
  await fetchCollections(); 
  collectionToAdd.value = {};
}

async function onRemoveClick(collection) {
  await axios.delete(`/api/collections/${collection.id}/`);
  await fetchCollections(); 
}

async function onCollectionsEditClick(collection) {
  collectionToEdit.value = { ...collection };
}

async function onUpdateCollection() {
  await axios.put(`/api/collections/${collectionToEdit.value.id}/`, {
    ...collectionToEdit.value,
  });
  await fetchCollections();
}

</script>

<template>
    <div class="container-fluid">
        <div class="modal fade" id="editCollectionModal" tabindex="-1">
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
                        v-model="collectionToEdit.name" required
                      />
                      <label for="floatingInput">Название</label>
                    </div>
                  </div>
                  <div class="col-12">
                    <div class="form-floating mb-2"> 
                      <textarea
                        class="form-control"
                        v-model="collectionToEdit.description"
                      ></textarea>
                      <label for="floatingInput">Описание</label>
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
              @click="onUpdateCollection"
            >
              Сохранить
            </button>
          </div>
        </div>
      </div>
    </div>


    <form @submit.prevent.stop="onCollectionsAdd" class="mt-4">
      <div class="row g-3" style="background-color: rgba(255, 255, 255, 0.8); padding: 1rem; border-radius: 8px;">
        <div class="col"> 
          <div class="form-floating">
            <input type="text" class="form-control"
              v-model="collectionToAdd.name"
              required
            />
            <label for="floatingInput">Имя</label>
          </div>
        </div>
        <div class="col">
            <div class="form-floating mb-2"> 
              <textarea
                class="form-control"
                v-model="collectionToAdd.description"
              ></textarea>
              <label for="floatingInput">Описание</label>
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
          <div v-for="item in collections" class="collection-item" :key="item.id">
            <div class="collection-details">
              <div class="collection-name">{{ item.name }}</div> 
              <div class="collection-description">{{ item.description }}</div>
            </div>
            <button class="btn btn-success" @click="onCollectionsEditClick(item)" data-bs-toggle="modal" data-bs-target="#editCollectionModal">
              <i class="bi bi-pen-fill"></i>
            </button>
            <button class="btn btn-danger" @click="onRemoveClick(item)"><i class="bi bi-x"></i></button>
          </div>
        </div>
        <div class="col-3 stats">          <h4>Статистика</h4>
          <p>Количество: {{ stats.count }}</p>
          <p>Средний ID: {{ stats.avg }}</p>
          <p>Максимальный ID: {{ stats.max }}</p>
          <p>Минимальный ID: {{ stats.min }}</p>
        </div>
      </div>
    </div>
</template>

<style lang="scss" scoped>
.collection-item{
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

  .collection-content {
  display: flex;
  align-items: center;
  flex-grow: 1;
  gap: 32px;
  
  }
  
  .collection-details {
  flex-grow: 1;
  }
  
  .collection-name {
  font-weight: bold;
  }

  .collection-description {
  color: #422F28;
  font-size: 14px;
  }
  
  .collection-actions {
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
