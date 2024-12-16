<script setup>

</script>
<template>
  <div class="app-container">
    <div class="container">
      <nav class="navbar navbar-expand-lg navbar-light navbar-transparent" style="border-radius: 8px;">
        <div class="container-fluid">
          <router-link class="nav-link" to="/"><img src="../../media/223351.png" style="max-height: 25px;"  alt="Музей"></router-link>
          <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNavDropdown" aria-controls="navbarNavDropdown" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
          </button>
          <div class="collapse navbar-collapse" id="navbarNavDropdown">
            <ul class="navbar-nav">
              <li class="nav-item">
                <router-link class="nav-link" to="/">Экспонаты</router-link>
              </li>
              <li class="nav-item">
                <router-link class="nav-link" to="/authors">Авторы</router-link>
              </li>
              <li class="nav-item">
                <router-link class="nav-link" to="/halls">Залы</router-link>
              </li>
              <li class="nav-item">
                <router-link class="nav-link" to="/collections">Коллекции</router-link>
              </li>
              <li class="nav-item">
                <router-link class="nav-link" to="/exhibitions">Выставки</router-link>
              </li>
              <li class="nav-item">
                <router-link class="nav-link" to="/visitors">Посетители</router-link>
              </li>
            </ul>

            <ul class="navbar-nav">
              <li class="nav-item dropdown">
                <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                  Пользователь
                </a>
                <ul class="dropdown-menu">
                  <li>
                    <a class="dropdown-item" href="/admin">
                      Админка
                    </a>
                  </li>
                </ul>
              </li>
            </ul>
          </div>
        </div>
      </nav>
      <div class="container content-container">
        <router-view/>
      </div>
    </div>
  </div>
</template>

<style scoped>
.app-container {
  background-color:rgba(142, 134, 131, 0.929); 
  background-size: cover; 
  background-repeat: no-repeat;
  background-position: center;
  display: flex;
  flex-direction: column;
  min-height: 100vh; 
  background-attachment: fixed;
}

.content-container {
  flex-grow: 1;
}

.navbar-transparent {
  background-color: rgba(255, 255, 255, 0.85);
}

</style>
