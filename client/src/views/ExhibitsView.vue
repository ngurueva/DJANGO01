<script setup>
import { onBeforeMount } from 'vue';
import { computed, ref } from 'vue';
import axios from 'axios';
import Cookies from 'js-cookie';
import _ from 'lodash';

const exhibits = ref([]);
const authors = ref([]);
const collections = ref([]);
const halls = ref([]);
const exhibitToAdd = ref({});
const exhibitToEdit = ref({});
const exhibitToView = ref({});
const loading = ref(false)
const exhibitsPictureRef = ref();
const exhibitAddImageUrl = ref();
const exhibitEditImageUrl = ref();
const stats = ref({})

const authorsById = computed(() => {
  return _.keyBy(authors.value, 'id');
});
const hallsById = computed(() => {
  return _.keyBy(halls.value, 'id');
});
const collectionsById = computed(() => {
  return _.keyBy(collections.value, 'id');
});

async function fetchExhibits() {
  loading.value = true;
  const r = await axios.get("/api/exhibits/");
  exhibits.value = r.data;
  loading.value = false;
}
async function fetchStats() {
  loading.value = true;
  const response = await axios.get("/api/exhibits/stats/");
  stats.value = response.data;
  loading.value = false;
}
async function fetchAuthors() {
  loading.value = true;
  const r = await axios.get("/api/authors/");
  authors.value = r.data;
  loading.value = false;
}
async function fetchCollections() {
  loading.value = true;
  const r = await axios.get("/api/collections/");
  collections.value = r.data;
  loading.value = false;
}
async function fetchHalls() {
  loading.value = true;
  const r = await axios.get("/api/halls/");
  halls.value = r.data;
  loading.value = false;
}

onBeforeMount(() => {
  axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken");
})

onBeforeMount(async () => {
  await fetchExhibits()
  await fetchAuthors()
  await fetchCollections()
  await fetchHalls()
  await fetchStats()
})

async function onExhibitAdd() {
  const formData = new FormData();

  if (exhibitsPictureRef.value.files[0]) {
    formData.append('picture', exhibitsPictureRef.value.files[0]);
  }

  formData.set('name', exhibitToAdd.value.name)
  formData.set('author', exhibitToAdd.value.author)
  formData.set('collection', exhibitToAdd.value.collection)
  formData.set('hall', exhibitToAdd.value.hall)
  formData.set('cost', exhibitToAdd.value.cost)
  formData.set('description', exhibitToAdd.value.description)
  formData.set('creation_year', exhibitToAdd.value.creation_year)

  await axios.post("/api/exhibits/", formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  });
  await fetchExhibits(); 
  exhibitToAdd.value = {};
  exhibitAddImageUrl.value = null;
  exhibitsPictureRef.value.value = null; 
}

async function onUpdateExhibit() {
 const formData = new FormData();

 if (exhibitToEdit.value.picture) {
  formData.append('picture', exhibitToEdit.value.picture); 
 }

 formData.set('name', exhibitToEdit.value.name);
 formData.set('author', exhibitToEdit.value.author);
 formData.set('collection', exhibitToEdit.value.collection);
 formData.set('hall', exhibitToEdit.value.hall);
 formData.set('cost', exhibitToEdit.value.cost);
 formData.set('description', exhibitToEdit.value.description);
 formData.set('creation_year', exhibitToEdit.value.creation_year);

 try {
  await axios.put(`/api/exhibits/${exhibitToEdit.value.id}/`, formData, {
   headers: {
    'Content-Type': 'multipart/form-data'
   }
  });

  await fetchExhibits();

  exhibitToEdit.value = {};
  exhibitEditImageUrl.value = null;
  exhibitsPictureRef.value.value = null; 
 } catch (error) {
  console.error("Ошибка обновления экспоната:", error);
 }
}

function onExhibitImageChange(event) {
 if (event.target.files[0]) {
  exhibitEditImageUrl.value = URL.createObjectURL(event.target.files[0]);
  exhibitToEdit.value.picture = event.target.files[0];
 } else {
  exhibitEditImageUrl.value = null; 
  exhibitToEdit.value.picture = null;
 }
}

async function onRemoveClick(exhibit) {
  await axios.delete(`/api/exhibits/${exhibit.id}/`);
  await fetchExhibits(); 
}
async function onExhibitEditClick(exhibit) {
  exhibitToEdit.value = { ...exhibit };
}
async function onExhibitPictureClick(exhibit) {
  exhibitToView.value = { ...exhibit };
}

async function exhibitsAddPictureChange() {
  if (exhibitAddImageUrl.value) {
    URL.revokeObjectURL(exhibitAddImageUrl.value); 
  }

  if (exhibitsPictureRef.value.files[0]) { 
    exhibitAddImageUrl.value = URL.createObjectURL(exhibitsPictureRef.value.files[0])
  } else {
    exhibitAddImageUrl.value = null; 
  }
}

function exhibitImageChangeClose() {
  exhibitEditImageUrl.value = null; 
}

</script>
<template>
  <div class="container-fluid">
    <div class="modal fade" id="editExhibitModal" tabindex="-1">
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
            <div class="row" style="background-color: rgba(255, 255, 255, 0.8); padding: 1rem; border-radius: 8px;">
              <div class="col-12 text-center" style="margin-top: 20px; margin-bottom: 20px;">
                <label for="fileInput">
                  <img
                    v-if="exhibitEditImageUrl"
                    :src="exhibitEditImageUrl"
                    style="max-height: 200px; cursor: pointer;"
                  />
                  <img
                    v-else-if="exhibitToEdit.picture"
                    :src="exhibitToEdit.picture"
                    style="max-height: 200px; cursor: pointer;"
                  />
                  <img
                    v-else
                    src="../../../media/Экспонат.png"
                    style="max-height: 200px; cursor: pointer;"
                  />
                </label>
                <input
                  type="file"
                  class="form-control"
                  id="fileInput"
                  @change="onExhibitImageChange"
                  style="display: none;"
                />
              </div>
              <div class="col-12">
                <div class="form-floating mb-2"> 
                  <input
                    type="text"
                    class="form-control"
                    v-model="exhibitToEdit.name" required
                  />
                  <label for="floatingInput">Название</label>
                </div>
              </div>
              <div class="col-12">
                <div class="form-floating mb-2"> 
                  <select class="form-select" v-model="exhibitToEdit.author" required>
                    <option :value="a.id" v-for="a in authors">{{ a.name + " " + a.surname }}</option>
                  </select>
                  <label for="floatingInput">Автор</label>
                </div>
              </div>

              <div class="col-12">
                <div class="form-floating mb-2"> 
                  <select class="form-select" v-model="exhibitToEdit.collection" required>
                    <option :value="c.id" v-for="c in collections">{{ c.name }}</option>
                  </select>
                  <label for="floatingInput">Коллекция</label>
                </div>
              </div>
              <div class="col-12">
                <div class="form-floating mb-2"> 
                  <select class="form-select" v-model="exhibitToEdit.hall" required>
                    <option :value="h.id" v-for="h in halls">{{ h.name }}</option>
                  </select>
                  <label for="floatingInput">Зал</label>
                </div>
              </div>
              <div class="col-6">
                <div class="form-floating mb-2"> 
                  <input
                    class="form-control"
                    v-model="exhibitToEdit.cost"
                  />
                  <label for="floatingInput">Стоимость</label>
                </div>
              </div>
              <div class="col-6">
                <div class="form-floating mb-2"> 
                  <input
                    type="number"
                    class="form-control"
                    v-model="exhibitToEdit.creation_year" required
                  />
                  <label for="floatingInput">Год создания</label>
                </div>
              </div>
              <div class="col-12">
                <div class="form-floating mb-2"> 
                  <textarea
                    class="form-control"
                    v-model="exhibitToEdit.description" 
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
              @click="exhibitImageChangeClose"
            >
              Закрыть
            </button>
            <button
              data-bs-dismiss="modal"
              type="button"
              class="btn btn-primary"
              @click="onUpdateExhibit"
            >
              Сохранить
            </button>
          </div>
        </div>
      </div>
    </div>

    <div class="modal" id="pictureExhibitModal" tabindex="-1">
      <div class="modal-dialog modal-dialog-centered"> <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">
            Экспонат - "{{exhibitToView.name}}"
          </h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Закрыть"></button>
        </div>
        <div class="modal-body">
          <div class="d-flex justify-content-center"> <img :src="exhibitToView.picture" style="max-height: 300px;" class="img-fluid">
          </div>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Закрыть</button>
        </div>
      </div>
    </div>
  </div>






  <form @submit.prevent.stop="onStudentAdd" class="mt-4">
    <div class="row g-3" style="background-color: rgba(255, 255, 255, 0.8); padding: 1rem; border-radius: 8px;">
      <div class="col"> 
        <div class="form-floating">
          <input type="text" class="form-control"
            v-model="exhibitToAdd.name"
            required
          />
          <label for="floatingInput">Название</label>
        </div>
      </div>
      <div class="col">
        <div class="form-floating">
          <select class="form-select" v-model="exhibitToAdd.author" required>
            <option :value="a.id" v-for="a in authors">{{ a.name + " " + a.surname }}</option>
          </select>
          <label for="floatingInput">Автор</label>
        </div>
      </div>
      <div class="col-md-2">
        <div class="form-floating">
          <select class="form-select" v-model="exhibitToAdd.collection" required>
            <option :value="c.id" v-for="c in collections">{{ c.name }}</option>
          </select>
          <label for="floatingInput">Коллекция</label>
        </div>
      </div>
      <div class="col-md-2">
        <div class="form-floating">
          <select class="form-select" v-model="exhibitToAdd.hall" required>
            <option :value="h.id" v-for="h in halls">{{ h.name }}</option>
          </select>
          <label for="floatingInput">Зал</label>
        </div>
      </div>
      <div class="col-md-2">
        <div class="form-floating">
          <input
            class="form-control"
            v-model="exhibitToAdd.cost"
          />
          <label for="floatingInput">Стоимость</label>
        </div>
      </div>
      <div class="col-md-2">
        <div class="form-floating">
          <input
            type="number"
            class="form-control"
            v-model="exhibitToAdd.creation_year" required
          />
          <label for="floatingInput">Год создания</label>
        </div>
      </div>

      <div class="col-auto">
        <input type="file" class="form-control" ref="exhibitsPictureRef" @change="exhibitsAddPictureChange">
      </div>

      <div class="col-auto">
        <img v-if="exhibitAddImageUrl" :src="exhibitAddImageUrl" style="max-height: 60px;" alt="">
      </div>

      <div class="col-md-4">
        <div class="form-floating">
          <textarea
            class="form-control"
            v-model="exhibitToAdd.description"
          ></textarea>
          <label for="floatingInput">Описание</label>
        </div>
      </div>
      <div class="col-auto">
        <button class="btn btn-primary" @click="onExhibitAdd">
          Добавить
        </button>
      </div>
    </div>
  </form>


  <div class="row">
    <div class="col-9">
      <div v-for="item in exhibits" class="exhibit-item" :key="item.id">
        <div class="exhibit-content">
          <div class="exhibit-image">
            <img 
              v-if="item.picture" 
              :src="item.picture" 
              style="max-height: 100px; cursor: pointer;"
              @click="onExhibitPictureClick(item)" 
              data-bs-toggle="modal" 
              data-bs-target="#pictureExhibitModal" 
            />
            <img v-else src="../../../media/Экспонат.png" style="max-height: 100px;" /> 
          </div>
          <div class="exhibit-details">
            <div class="exhibit-name">{{ item.name }}</div> 
            <div class="exhibit-author">{{ authorsById[item.author]?.name + ' ' + authorsById[item.author]?.surname }}</div>
            <div class="exhibit-collection">{{ collectionsById[item.collection]?.name }}</div>
            <div class="exhibit-hall">{{ hallsById[item.hall]?.name }}</div>
            <div v-if="item.cost!='undefined'" class="exhibit-cost">Стоимость: {{ item.cost }}</div>
            <div v-if="item.description!='undefined'" class="exhibit-description">{{ item.description }}</div>
            <div class="exhibit-year">Год создания: {{ item.creation_year }}</div>
          </div>
        </div>
        <div class="exhibit-actions">
          <button class="btn btn-success" @click="onExhibitEditClick(item)" data-bs-toggle="modal" data-bs-target="#editExhibitModal">
            <i class="bi bi-pen-fill"></i>
          </button>
          <button class="btn btn-danger" @click="onRemoveClick(item)"><i class="bi bi-x"></i></button>
        </div>
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


<style>

.exhibit-item {
padding: 1rem;
margin: 1rem 0;
border: 1px solid #ddd;
border-radius: 8px;
display: flex;
gap: 16px;
background-color: rgba(255, 255, 255, 0.85) ;
}

.exhibit-content {
display: flex;
align-items: center;
flex-grow: 1;
gap: 32px;

}

.exhibit-image {
width: 120px;
height: 120px;
display: flex;
align-items: center;
justify-content: center;
border: 1px solid #ddd;
border-radius: 8px;
background-color: white;
}

.exhibit-image img {
max-width: 100%;
max-height: 100%;
object-fit: cover;
}

.placeholder {
font-size: 24px;
color: #ccc;
}

.exhibit-details {
flex-grow: 1;
}

.exhibit-name {
font-weight: bold;
}

.exhibit-author {
color: #422F28;
}

.exhibit-collection {
color: #422F28;
}

.exhibit-hall {
color: #422F28;
}

.exhibit-cost {
color: #422F28;
}

.exhibit-description {
color: #422F28;
font-size: 14px;
}

.exhibit-year {
color: #422F28;
}

.exhibit-actions {
display: flex;
align-items: flex-start; 
gap: 8px;
}
.btn {
background-color: #422F28; 
border: none; 
color: white; 
}
.btn-success {
background-color: #6A6F4C; 
border: none; 
color: white;
}

.btn-danger {
background-color: #5E2611; 
border: none; 
color: white; 
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