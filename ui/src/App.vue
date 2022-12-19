<script setup lang="ts">
import { RouterLink, RouterView } from "vue-router";
import Toolbar from "./components/Toolbar.vue";
import Sidebar from "./components/Sidebar.vue";
import { useAuthStore } from "@/stores/auth";

const authStore: any = useAuthStore();
authStore.isSessionActive().then((val: boolean) => {
  if (!val) {
    authStore.reset();
  }
});
</script>

<template>
  <Toolbar />

  <div class="d-flex align-items-stretch">
    <Sidebar />

    <div class="page-content">
      <RouterView />
    </div>
  </div>
</template>
