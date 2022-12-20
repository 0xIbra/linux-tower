<script setup lang="ts">
import { useAuthStore } from "@/stores/auth";
import { useProgramsStore } from "@/stores/programs";

const authStore = useAuthStore();
const programsStore = useProgramsStore();

if (authStore.accessToken != null) {
  programsStore.getApache();
  programsStore.getNginx();
}

const programsUpdateInterval = setInterval(async () => {
  if (authStore.accessToken != null) {
    await programsStore.getApache();
    await programsStore.getNginx();
  }
}, 20000);
</script>

<template>
  <!-- Sidebar Navigation-->
  <nav v-if="authStore.isAuthenticated()" id="sidebar">
    <!-- Sidebar Header-->
    <div class="sidebar-header d-flex align-items-center p-4"><img class="avatar shadow-0 img-fluid rounded-circle"
        src="img/avatar-6.jpg" alt="...">
      <div class="ms-3 title">
        <h1 class="h5 mb-1">ibra</h1>
        <p class="text-sm text-gray-700 mb-0 lh-1">Linux user</p>
      </div>
    </div>
    <span class="text-uppercase text-gray-600 text-xs mx-3 px-2 heading mb-2">Main</span>
    <ul class="list-unstyled">
      <li class="sidebar-item" :class="{active: $route.name === 'home'}">
        <router-link to="/" class="sidebar-link">
          <svg class="svg-icon svg-icon-sm svg-icon-heavy">
            <use xlink:href="#real-estate-1"></use>
          </svg>
          <span>Dashboard</span>
        </router-link>
      </li>
      <li v-if="programsStore.apache != null" class="sidebar-item" :class="{active: $route.name === 'apache'}">
        <router-link class="sidebar-link" to="/apache">
          <svg class="svg-icon svg-icon-sm svg-icon-heavy">
            <use xlink:href="#portfolio-grid-1"></use>
          </svg>
          <span>Apache</span>
        </router-link>
      </li>
      <li v-if="programsStore.nginx != null" class="sidebar-item" :class="{active: $route.name === 'nginx'}">
        <a class="sidebar-link" href="charts.html">
          <svg class="svg-icon svg-icon-sm svg-icon-heavy">
            <use xlink:href="#sales-up-1"></use>
          </svg>
          <span>Nginx</span>
        </a>
      </li>
      <li class="sidebar-item">
        <a class="sidebar-link" href="forms.html">
          <svg class="svg-icon svg-icon-sm svg-icon-heavy">
            <use xlink:href="#survey-1"></use>
          </svg>
          <span>Alerts</span>
        </a>
      </li>
      <li class="sidebar-item">
        <a class="sidebar-link" href="login.html">
          <svg class="svg-icon svg-icon-sm svg-icon-heavy">
            <use xlink:href="#disable-1"></use>
          </svg>
          <span>Logs</span>
        </a>
      </li>
      <li class="sidebar-item">
        <a class="sidebar-link" href="#exampledropdownDropdown" data-bs-toggle="collapse">
          <svg class="svg-icon svg-icon-sm svg-icon-heavy">
            <use xlink:href="#browser-window-1"></use>
          </svg>
          <span>Example dropdown </span>
        </a>
        <ul class="collapse list-unstyled " id="exampledropdownDropdown">
          <li><a class="sidebar-link" href="#">Page</a></li>
          <li><a class="sidebar-link" href="#">Page</a></li>
          <li><a class="sidebar-link" href="#">Page</a></li>
        </ul>
      </li>
    </ul>
    <span class="text-uppercase text-gray-600 text-xs mx-3 px-2 heading mb-2">Extras</span>
    <ul class="list-unstyled">
      <li class="sidebar-item">
        <a class="sidebar-link" href="#">
          <svg class="svg-icon svg-icon-sm svg-icon-heavy">
            <use xlink:href="#imac-screen-1"></use>
          </svg>
          <span>Demo </span>
        </a>
      </li>
      <li class="sidebar-item">
        <a class="sidebar-link" href="#">
          <svg class="svg-icon svg-icon-sm svg-icon-heavy">
            <use xlink:href="#chart-1"></use>
          </svg>
          <span>Demo </span>
        </a>
      </li>
      <li class="sidebar-item">
        <a class="sidebar-link" href="#">
          <svg class="svg-icon svg-icon-sm svg-icon-heavy">
            <use xlink:href="#quality-1"></use>
          </svg>
          <span>Demo </span>
        </a>
      </li>
      <li class="sidebar-item">
        <a class="sidebar-link" href="#">
          <svg class="svg-icon svg-icon-sm svg-icon-heavy">
            <use xlink:href="#security-shield-1"></use>
          </svg>
          <span>Demo </span>
        </a>
      </li>
    </ul>
  </nav>
</template>
