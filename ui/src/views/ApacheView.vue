<script setup lang="ts">
import { ref, onMounted } from "vue";
import { useProgramsStore } from "@/stores/programs";
import Logs from "@/components/Logs.vue";

const programsStore = useProgramsStore();
const apache = ref();
const apacheState = ref();

onMounted(async () => {
  await programsStore.getApache();
  if (programsStore.apache != null && programsStore.apache.details != null) {
    apache.value = programsStore.apache;
    apacheState.value = programsStore.apache.details.state;
  }
});
</script>

<template>
  <div class="page-content">
    <div class="bg-dash-dark-2 py-4">
      <div class="container-fluid">
        <h2 class="h5 mb-0">Apache HTTP Server</h2>
      </div>
    </div>

    <section v-if="programsStore.apache != null">
      <div class="container-fluid">
        <div class="row gy-4">
          <div class="col-md-4 col-sm-6">
            <div class="row gy-4">
              <div class="col-md-12">
                <div class="cpu-usage-wrapper card mb-0">
                  <div class="card-body">
                    <p class="text-xxl lh-1 mb-0" :class="{'text-color-primary': programsStore.apache.details.state === 'running', 'text-color-danger': apacheState !== 'running'}">
                      {{ programsStore.apache.details.state }}
                    </p>
                    <div class="me-2">
                      <p class="text-sm text-gray-600 mt-2 mb-0">Since {{ programsStore.apache.details.started_at }}</p>
                    </div>
                  </div>
                </div>
              </div>

              <div class="col-md-12">
                <div class="cpu-usage-wrapper card mb-0">
                  <div class="card-body">
                    <div class="me-2 mb-2">
                      <p class="text-sm text-gray-600 mt-2 mb-0">Status logs:</p>
                    </div>
                    <Logs v-if="apache != null" :raw-logs="programsStore.apache.status" :display-lines="false" />
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div class="col-md-6">
            <div class="row gy-4">
              <div class="col-12">
                <div class="cpu-usage-wrapper card mb-0">
                  <div class="card-body">
                    <div class="me-2 mb-2">
                      <p class="text-sm text-gray-600 mt-2 mb-0">Logs:</p>
                    </div>
                    <Logs v-if="apache != null" logs-endpoint="/api/logs/tail?log_file=/var/log/syslog" :display-lines="true" />
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>
