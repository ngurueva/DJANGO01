<script setup>
import { onBeforeMount } from 'vue';
import { computed, ref } from 'vue';
import axios from 'axios';
import Cookies from 'js-cookie';
import _ from 'lodash';

const authors = ref([]);
const authorToAdd = ref({});
const authorToEdit = ref({});
const authorToView = ref({});
const loading = ref(false)
const authorsPictureRef = ref();
const authorAddImageUrl = ref();
const authorEditImageUrl = ref();
const stats = ref({})

async function fetchAuthors() {
  loading.value = true;
  const r = await axios.get("/api/authors/");
  authors.value = r.data;
  loading.value = false;
}

async function fetchStats() {
  loading.value = true;
  const response = await axios.get("/api/authors/stats/");
  stats.value = response.data;
  loading.value = false;
}

onBeforeMount(() => {
  axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken");
});

onBeforeMount(async () => { 
  await fetchAuthors();
  await fetchStats();
});

async function onAuthorsAdd() {
  const formData = new FormData();

  if (authorsPictureRef.value.files[0]) {
    formData.append('picture', authorsPictureRef.value.files[0]);
  }

  formData.set('name', authorToAdd.value.name)
  formData.set('surname', authorToAdd.value.surname)
  formData.set('birthdate', authorToAdd.value.birthdate)
  formData.set('deathdate', authorToAdd.value.deathdate)

  await axios.post("/api/authors/", formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  });
  await fetchAuthors(); 

  authorToAdd.value = {};
  authorAddImageUrl.value = null;
  authorsPictureRef.value.value = null;
}

async function onRemoveClick(author) {
  await axios.delete(`/api/authors/${author.id}/`);
  await fetchAuthors(); 
}

async function onAuthorEditClick(author) {
  authorToEdit.value = { ...author };
}

async function onUpdateAuthor() {
  const formData = new FormData();

  if (authorToEdit.value.picture) {
    formData.append('picture', authorToEdit.value.picture); 
  }

  formData.set('name', authorToEdit.value.name);
  formData.set('surname', authorToEdit.value.surname);
  formData.set('birthdate', authorToEdit.value.birthdate);
  formData.set('deathdate', authorToEdit.value.deathdate);
//   try {
//   await axios.put(`/api/authors/${authorToEdit.value.id}/`, formData, {
//     headers: {
//       'Content-Type': 'multipart/form-data'
//     }
//   });
//   await fetchAuthors(); 

// } catch (error) {
//   console.error("Ошибка обновления автора:", error);
//  }


//   await axios.put("/api/authors/", formData, {
//     headers: {
//       'Content-Type': 'multipart/form-data'
//     }
//   });
//   await fetchAuthors(); 
//   authorToAdd.value = {};
//   authorAddImageUrlvalue = null;
//   authorsPictureRef.value.value = null; 
// }
try {
  await axios.put(`/api/authors/${authorsToEdit.value.id}/`, formData, {
   headers: {
    'Content-Type': 'multipart/form-data'
   }
  });

  await fetchAuthorss();

  authorToEdit.value = {};
  authorEditImageUrl.value = null;
  authorsPictureRef.value.value = null; 
 } catch (error) {
  console.error("Ошибка обновления author:", error);
 }
}

async function authorsAddPictureChange() {
  if (authorAddImageUrl.value) {
    URL.revokeObjectURL(authorAddImageUrl.value); 
  }

  if (authorsPictureRef.value.files[0]) { 
    authorAddImageUrl.value = URL.createObjectURL(authorsPictureRef.value.files[0])
  } else {
    authorAddImageUrl.value = null; 
  }
}

function authorImageChange(event) {
  if (event.target.files[0]) { 
    authorEditImageUrl.value = URL.createObjectURL(event.target.files[0]);
    authorToEdit.value.picture = event.target.files[0];
  } else {
    authorEditImageUrl.value = null; 
    authorToEdit.value.picture = null;
  }
}

async function onAuthorPictureClick(author) {
  authorToView.value = { ...author };
}

function authorImageChangeClose() {
  authorEditImageUrl.value = null; 
}

</script>

<template>
  <div class="container-fluid">
      <div class="modal fade" id="editAuthorModal" tabindex="-1">
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
                      v-if="authorEditImageUrl"
                      :src="authorEditImageUrl"
                      style="max-height: 150px; cursor: pointer;"
                    />
                    <img
                      v-else-if="authorToEdit.picture"
                      :src="authorToEdit.picture"
                      style="max-height: 150px; cursor: pointer;"
                      />
                      <img
                        v-else
                        src="../../../media/Автор.png"
                        style="max-height: 150px; cursor: pointer;"
                      />
                    </label>
                    <input
                      type="file"
                      class="form-control"
                      id="fileInput"
                      @change="authorImageChange"
                      style="display: none;"
                    />
                  </div>
                  <div class="col-12">
                    <div class="form-floating mb-2"> 
                      <input
                        type="text"
                        class="form-control"
                        v-model="authorToEdit.name" required
                      />
                      <label for="floatingInput">Имя</label>
                    </div>
                  </div>
                  <div class="col-12">
                    <div class="form-floating mb-2"> 
                      <input
                        type="text"
                        class="form-control"
                        v-model="authorToEdit.surname" required
                      />
                      <label for="floatingInput">Фамилия</label>
                    </div>
                  </div>
                  <div class="col-6">
                    <div class="form-floating mb-2"> 
                      <input
                        type="date"
                        class="form-control"
                        v-model="authorToEdit.birthdate"
                    />
                    <label for="floatingInput">Дата рождения</label>
                  </div>
                </div>
                <div class="col-6">
                  <div class="form-floating mb-2"> 
                    <input
                      type="date"
                      class="form-control"
                      v-model="authorToEdit.deathdate" 
                    />
                    <label for="floatingInput">Дата смерти</label>
                  </div>
                </div>
          </div>
        </div>
        <div class="modal-footer">
          <button
            type="button"
            class="btn btn-secondary"
            data-bs-dismiss="modal"
            @click="authorImageChangeClose"
          >
            Закрыть
          </button>
          <button
            data-bs-dismiss="modal"
            type="button"
            class="btn btn-primary"
            @click="onUpdateAuthor"
          >
            Сохранить
          </button>
        </div>
      </div>
    </div>
  </div>

  <div class="modal" id="pictureAuthorModal" tabindex="-1">
    <div class="modal-dialog modal-dialog-centered"> <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">
            {{authorToView.name + " " + authorToView.surname}}
          </h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Закрыть"></button>
        </div>
        <div class="modal-body">
          <div class="d-flex justify-content-center"> <img :src="authorToView.picture" style="max-height: 300px;" class="img-fluid">
          </div>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Закрыть</button>
        </div>
      </div>
    </div>
  </div>



    <form @submit.prevent.stop="onAuthorsAdd" class="mt-4">
      <div class="row g-3" style="background-color: rgba(255, 255, 255, 0.8); padding: 1rem; border-radius: 8px;">
        <div class="col"> 
          <div class="form-floating">
            <input type="text" class="form-control"
              v-model="authorToAdd.name"
              required
            />
            <label for="floatingInput">Имя</label>
          </div>
        </div>
        <div class="col"> 
          <div class="form-floating">
            <input type="text" class="form-control"
              v-model="authorToAdd.surname"
              required
            />
            <label for="floatingInput">Фамилия</label>
          </div>
      </div>
      <div class="col">
          <div class="form-floating mb-2"> 
            <input
              type="date"
              class="form-control"
              v-model="authorToAdd.birthdate" required
            />
            <label for="floatingInput">Дата рождения</label>
          </div>
        </div>
        <div class="col">
          <div class="form-floating mb-2"> 
            <input
              type="date"
              class="form-control"
              v-model="authorToAdd.deathdate"  required
            />
            <label for="floatingInput">Дата смерти</label>
          </div>
        </div>
        <div class="col-auto">
          <input type="file" class="form-control" ref="authorsPictureRef" @change="authorsAddPictureChange">
        </div>

        <div class="col-auto">
          <img v-if="authorAddImageUrl" :src="authorAddImageUrl" style="max-height: 60px;" alt="">
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
        <div  v-for="item in authors" class="author-item" :key="item.id">
          <div class="author-content">
            <div class="author-image">
              <img 
                v-if="item.picture" 
                :src="item.picture" 
                style="max-height: 100px; cursor: pointer;"
                @click="onAuthorPictureClick(item)" 
                data-bs-toggle="modal" 
                data-bs-target="#pictureAuthorModal" 
              />
              <img v-else src="../../../media/Автор.png" style="max-height: 100px;" /> 
            </div>
            <div class="author-details">
              <div class="author-name">{{ item.name + " " + item.surname }}</div> 
              <div class="author-birth">Дата рождения: {{ item.birthdate }}</div>
              <div v-if="item.deathdate" class="author-death">Дата смерти: {{ item.deathdate }}</div>
            </div>
          </div>
          <div class="author-actions">
            <button class="btn btn-success" @click="onAuthorEditClick(item)" data-bs-toggle="modal" data-bs-target="#editAuthorModal">
              <i class="bi bi-pen-fill"></i>
            </button>
            <button class="btn btn-danger" @click="onRemoveClick(item)"><i class="bi bi-x"></i></button>
          </div>
        </div>
      </div>
      <div class="col-3 stats">        <h4>Статистика</h4>
        <p>Количество: {{ stats.count }}</p>
        <p>Средний ID: {{ stats.avg }}</p>
        <p>Максимальный ID: {{ stats.max }}</p>
        <p>Минимальный ID: {{ stats.min }}</p>
      </div>
    </div>
  </div> 



</template>

<style lang="scss" scoped>
.author-item{
  padding: 0.5rem;
  margin: 0.5rem 0;
  border: 1px solid silver;
  border-radius: 8px;
  display: grid;
  grid-template-columns: 1fr auto  auto auto;
  align-content: center;
  align-items: center;
  gap: 16px;
  background-color: rgba(255, 255, 255, 1) ;

}
.author-content {
  display: flex;
  align-items: center;
  flex-grow: 1;
  gap: 32px;
  
}
  
.author-image {
  width: 120px;
  height: 120px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid #ddd;
  border-radius: 8px;
  background-color: white;
}
  
.author-image img {
  max-width: 100%;
  max-height: 100%;
  object-fit: cover;
}
.author-name {
  font-weight: bold;
}
.author-details {
    flex-grow: 1;
}
.author-actions {
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
  