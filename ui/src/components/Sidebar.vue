<script setup lang="ts">
import { useAuthStore } from "@/stores/auth";
import { useApacheStore } from "@/stores/apache";
import { useNginxStore } from "@/stores/nginx";
import { useMysqlStore } from "@/stores/mysql";

const authStore = useAuthStore();
const apacheStore = useApacheStore();
const nginxStore = useNginxStore();
const mysqlStore = useMysqlStore();

if (authStore.accessToken != null) {
  apacheStore.init();
  nginxStore.init();
  mysqlStore.init();
}

const programsUpdateInterval = setInterval(async () => {
  if (authStore.accessToken != null) {
    if (apacheStore.installed) {
      await apacheStore.init();
    }

    if (nginxStore.installed) {
      await nginxStore.init();
    }

    if (mysqlStore.installed) {
      await mysqlStore.init();
    }
  }
}, 20000);
</script>

<template>
  <!-- Sidebar Navigation-->
  <nav v-if="authStore.isAuthenticated()" id="sidebar">
    <!-- Sidebar Header-->
    <div class="sidebar-header d-flex align-items-center p-4"><img class="avatar shadow-0 img-fluid rounded-circle"
        src="/img/avatar-6.jpg" alt="...">
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
            <use xlink:href="#imac-screen-1"></use>
          </svg>
          <span>Host</span>
        </router-link>
      </li>
      <li v-if="apacheStore.data != null" class="sidebar-item" :class="{active: $route.name === 'apache'}">
        <router-link class="sidebar-link" to="/apache">
          <svg class="svg-icon svg-icon-sm svg-icon-heavy">
            <use xlink:href="#browser-window-1"></use>
          </svg>
          <span>Apache</span>
        </router-link>
      </li>
      <li v-if="nginxStore.data != null" class="sidebar-item" :class="{active: $route.name === 'nginx'}">
        <router-link class="sidebar-link" to="/nginx">
          <svg class="svg-icon svg-icon-sm svg-icon-heavy">
            <use xlink:href="#browser-window-1"></use>
          </svg>
          <span>Nginx</span>
        </router-link>
      </li>
      <li v-if="mysqlStore.data != null" class="sidebar-item" :class="{active: $route.name === 'mysql'}">
        <router-link class="sidebar-link" to="/mysql">
          <svg class="svg-icon svg-icon-sm svg-icon-heavy">
            <use xlink:href="#paper-stack-1"></use>
          </svg>
          <span>MySQL</span>
        </router-link>
      </li>
      <li class="sidebar-item" :class="{active: ['alerts', 'createAlert', 'editAlert'].includes($route.name)}">
        <router-link class="sidebar-link" to="/alerts">
          <svg class="svg-icon svg-icon-sm svg-icon-heavy">
            <use xlink:href="#survey-1"></use>
          </svg>
          <span>Alerts</span>
        </router-link>
      </li>
      <li class="sidebar-item" :class="{ active: $route.name === 'logs' }">
        <router-link class="sidebar-link" to="/logs">
          <svg class="svg-icon svg-icon-sm svg-icon-heavy">
            <use xlink:href="#disable-1"></use>
          </svg>
          <span>Logs</span>
        </router-link>
      </li>
    </ul>
  </nav>
</template>
