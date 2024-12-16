
<script setup>
import { onBeforeMount, ref } from "vue";
import axios from "axios";
import Cookies from "js-cookie";

const exhibitions = ref([]);
const exhibits = ref([]);
const exhibitionToAdd = ref({
name: "",
description: "",
opening_date: "",
closing_date: "",
exhibits: [],
});
const exhibitionToEdit = ref({
name: "",
description: "",
opening_date: "",
closing_date: "",
exhibits: [],
});
const loading = ref(false);
const stats = ref({})

async function fetchExhibitions() {
loading.value = true;
const r = await axios.get("/api/exhibitions/");
exhibitions.value = r.data;
loading.value = false;
}

async function fetchStats() {
  loading.value = true;
  const response = await axios.get("/api/exhibitions/stats/");
  stats.value = response.data;
  loading.value = false;
}

async function fetchExhibits() {
loading.value = true;
const r = await axios.get("/api/exhibits/");
exhibits.value = r.data;
loading.value = false;
}

onBeforeMount(async () => {
axios.defaults.headers.common["X-CSRFToken"] = Cookies.get("csrftoken");
await fetchExhibitions();
await fetchExhibits();
await fetchStats();
});

async function onExhibitionsAdd() {
await axios.post("/api/exhibitions/", {
  ...exhibitionToAdd.value,
});
await fetchExhibitions();

exhibitionToAdd.value = {
  name: "",
  description: "",
  opening_date: "",
  closing_date: "",
  exhibits: [], // Сбрасываем массив exhibits
};
}

async function onRemoveClick(exhibition) {
await axios.delete(`/api/exhibitions/${exhibition.id}/`);
await fetchExhibitions();
}

async function onExhibitionsEditClick(exhibition) {
exhibitionToEdit.value = { ...exhibition };
}
async function onUpdateExhibition() {
await axios.put(`/api/exhibitions/${exhibitionToEdit.value.id}/`, {
  ...exhibitionToEdit.value,
});
await fetchExhibitions();
}
</script>
<template>
  <div class="container-fluid">
    <div class="modal fade" id="editExhibitionModal" tabindex="-1">
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
                    v-model="exhibitionToEdit.name"
                    required
                  />
                  <label for="floatingInput">Название</label>
                </div>
              </div>
              <div class="col-12">
                <div class="form-floating mb-2">
                  <textarea
                    class="form-control"
                    v-model="exhibitionToEdit.description"
                    required
                  ></textarea>
                  <label for="floatingInput">Описание</label>
                </div>
              </div>
              <div class="col-6">
                <div class="form-floating mb-2">
                  <input
                    type="date"
                    class="form-control"
                    v-model="exhibitionToEdit.opening_date"
                    required
                  />
                  <label for="floatingInput">Дата открытия</label>
                </div>
              </div>
              <div class="col-6">
                <div class="form-floating mb-2">
                  <input
                    type="date"
                    class="form-control"
                    v-model="exhibitionToEdit.closing_date"
                    required
                  />
                  <label for="floatingInput">Дата закрытия</label>
                </div>
              </div>

              <div class="col-12">
                <div class="form-floating">
                  <select
                    class="form-select"
                    v-model="exhibitionToEdit.exhibits"
                    multiple
                  >
                    <option
                      :value="e.id"
                      v-for="e in exhibits"
                      :key="e.id"
                    >
                      {{ e.name }}
                    </option>
                  </select>
                  <label for="floatingInput">Экспонаты</label>
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
              @click="onUpdateExhibition"
            >
              Сохранить
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>

  <form @submit.prevent.stop="onExhibitionsAdd" class="mt-4">
    <div
      class="row g-3"
      style="
        background-color: rgba(255, 255, 255, 0.8);
        padding: 1rem;
        border-radius: 8px;
      "
    >
      <div class="col">
        <div class="form-floating">
          <input
            type="text"
            class="form-control"
            v-model="exhibitionToAdd.name"
            required
          />
          <label for="floatingInput">Название</label>
        </div>
      </div>
      <div class="col">
        <div class="form-floating mb-2">
          <textarea
            class="form-control"
            v-model="exhibitionToAdd.description"
          ></textarea>
          <label for="floatingInput">Описание</label>
        </div>
      </div>

      <div class="col">
        <div class="form-floating mb-2">
          <input
            type="date"
            class="form-control"
            v-model="exhibitionToAdd.opening_date"
          />
          <label for="floatingInput">Дата открытия</label>
        </div>
      </div>
      <div class="col">
        <div class="form-floating mb-2">
          <input
            type="date"
            class="form-control"
            v-model="exhibitionToAdd.closing_date"
          />
          <label for="floatingInput">Дата закрытия</label>
        </div>
      </div>

      <div class="col-12">
        <div class="form-floating">
          <select
          class="form-select"
          v-model="exhibitionToAdd.exhibits"
          multiple
        >
          <option
            :value="e.id"
            v-for="e in exhibits"
            :key="e.id"
          >
            {{ e.name }}
          </option>
        </select>
        <label for="floatingInput">Экспонаты</label>
      </div>
    </div>

    <div class="col-auto">
      <button class="btn btn-primary">Добавить</button>
    </div>
  </div>
</form>



<div class="row">
  <div class="col-9">
    <div
    v-for="item in exhibitions"
    class="exhibition-item"
    :key="item.id"
  >
    <div class="exhibition-content">
      <div class="exhibition-details">
        <div class="exhibition-name">{{ item.name }}</div>
        <div class="exhibition-opening_date">
          Дата открытия: {{ item.opening_date }}
        </div>
        <div class="exhibition-closing_date">
          Дата закрытия: {{ item.closing_date }}
        </div>
        <div class="exhibition-description">
          {{ item.description }}
        </div>
        <div v-if="item.exhibits.length > 0">
          Экспонаты:
          <div
            v-for="e in exhibits.filter(exhibit => item.exhibits.includes(exhibit.id))"
            :key="e.id"
            class="exhibition-exhibits"
          >
            {{ e.name }}
          </div>
        </div>
      </div>

      <div class="exhibition-actions">
        <button
          class="btn btn-success"
          @click="onExhibitionsEditClick(item)"
          data-bs-toggle="modal"
          data-bs-target="#editExhibitionModal"
        >
          <i class="bi bi-pen-fill"></i>
        </button>
        <button
          class="btn btn-danger"
          @click="onRemoveClick(item)"
        >
          <i class="bi bi-x"></i>
        </button>
      </div>
    </div>
  </div>
  </div>
  <div class="col-3 stats">    <h4>Статистика</h4>
    <p>Количество: {{ stats.count }}</p>
    <p>Средний ID: {{ stats.avg }}</p>
    <p>Максимальный ID: {{ stats.max }}</p>
    <p>Минимальный ID: {{ stats.min }}</p>
</div>
</div>
</template>


<style lang="scss" scoped>
.exhibition-item {
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
.form-select[multiple] {
min-height: 150px;
}

.exhibition-content {
display: flex;
align-items: center;
flex-grow: 1;
gap: 32px;
}

.exhibition-details {
flex-grow: 1;
}

.exhibition-name {
font-weight: bold;
}

.exhibition-description {
color: #422f28;
font-size: 14px;
}

.exhibition-opening_date {
color: #422f28;
}
.exhibition-closing_date {
color: #422f28;
}
.exhibition-exhibits {
color: #422f28;
font-style: italic;
text-indent: 20px;
}

.exhibition-actions {
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