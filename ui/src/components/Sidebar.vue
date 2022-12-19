<script setup lang="ts">
import { useAuthStore } from "@/stores/auth";

const authStore = useAuthStore();
</script>

<template>
  <!-- Sidebar Navigation-->
  <nav v-if="authStore.isAuthenticated()" id="sidebar">
    <!-- Sidebar Header-->
    <div class="sidebar-header d-flex align-items-center p-4"><img class="avatar shadow-0 img-fluid rounded-circle" src="img/avatar-6.jpg" alt="...">
      <div class="ms-3 title">
        <h1 class="h5 mb-1">ibra</h1>
        <p class="text-sm text-gray-700 mb-0 lh-1">Linux user</p>
      </div>
    </div>
    <span class="text-uppercase text-gray-600 text-xs mx-3 px-2 heading mb-2">Main</span>
    <ul class="list-unstyled">
      <li class="sidebar-item active">
        <router-link to="/" class="sidebar-link">
          <svg class="svg-icon svg-icon-sm svg-icon-heavy"><use xlink:href="#real-estate-1"></use></svg>
          <span>Home</span>
        </router-link>
      </li>
      <li class="sidebar-item"><a class="sidebar-link" href="tables.html">
        <svg class="svg-icon svg-icon-sm svg-icon-heavy">
          <use xlink:href="#portfolio-grid-1"></use>
        </svg>
        <span>Tables </span></a></li>
      <li class="sidebar-item"><a class="sidebar-link" href="charts.html">
        <svg class="svg-icon svg-icon-sm svg-icon-heavy">
          <use xlink:href="#sales-up-1"></use>
        </svg>
        <span>Charts </span></a></li>
      <li class="sidebar-item"><a class="sidebar-link" href="forms.html">
        <svg class="svg-icon svg-icon-sm svg-icon-heavy">
          <use xlink:href="#survey-1"></use>
        </svg>
        <span>Forms </span></a></li>
      <li class="sidebar-item"><a class="sidebar-link" href="#exampledropdownDropdown" data-bs-toggle="collapse">
        <svg class="svg-icon svg-icon-sm svg-icon-heavy">
          <use xlink:href="#browser-window-1"></use>
        </svg>
        <span>Example dropdown </span></a>
        <ul class="collapse list-unstyled " id="exampledropdownDropdown">
          <li><a class="sidebar-link" href="#">Page</a></li>
          <li><a class="sidebar-link" href="#">Page</a></li>
          <li><a class="sidebar-link" href="#">Page</a></li>
        </ul>
      </li>
      <li class="sidebar-item"><a class="sidebar-link" href="login.html">
        <svg class="svg-icon svg-icon-sm svg-icon-heavy">
          <use xlink:href="#disable-1"></use>
        </svg>
        <span>Login page </span></a></li>
    </ul>
    <span class="text-uppercase text-gray-600 text-xs mx-3 px-2 heading mb-2">Extras</span>
    <ul class="list-unstyled">
      <li class="sidebar-item"><a class="sidebar-link" href="#">
        <svg class="svg-icon svg-icon-sm svg-icon-heavy">
          <use xlink:href="#imac-screen-1"></use>
        </svg>
        <span>Demo </span></a></li>
      <li class="sidebar-item">
        <a class="sidebar-link" href="#">
          <svg class="svg-icon svg-icon-sm svg-icon-heavy">
            <use xlink:href="#chart-1"></use>
          </svg>
          <span>Demo </span>
        </a>
      </li>
      <li class="sidebar-item"><a class="sidebar-link" href="#">
        <svg class="svg-icon svg-icon-sm svg-icon-heavy">
          <use xlink:href="#quality-1"></use>
        </svg>
        <span>Demo </span></a></li>
      <li class="sidebar-item"><a class="sidebar-link" href="#">
        <svg class="svg-icon svg-icon-sm svg-icon-heavy">
          <use xlink:href="#security-shield-1"></use>
        </svg>
        <span>Demo </span></a></li>
    </ul>
  </nav>
</template>