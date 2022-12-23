<script setup lang="ts">
import { getCurrentInstance, ref, onMounted, onBeforeUnmount } from "vue";
import { useNginxStore } from "@/stores/nginx";
import Logs from "@/components/Logs.vue";
import { metricTextColorClass, metricBgColorClass } from "@/utils/dynamicClasses";

const nginxStore = useNginxStore();
const nginx = ref();
const nginxState = ref();
const selectedLogFile = ref("/var/log/nginx/error.log");

const logsComponentRef = ref();

const refreshInterval = ref();

onMounted(async () => {
  await nginxStore.init();
  if (nginxStore.data != null && nginxStore.data.details != null) {
    nginx.value = nginxStore.data;
    nginxState.value = nginxStore.data.details.state;
  }

  updateLogs();

  await nginxStore.getMetrics();
  refreshInterval.value = setInterval(() => {
    nginxStore.getMetrics().catch((e) => console.error(e));
  }, 5000);
});

onBeforeUnmount(() => {
  clearInterval(refreshInterval.value);
});

const updateLogs = () => {
  if (logsComponentRef.value != null) {
    logsComponentRef.value.setEndpoint("/api/logs/tail?log_file=" + selectedLogFile.value);
    logsComponentRef.value.reloadLogs();
  }
  const instance = getCurrentInstance();
  instance?.proxy?.$forceUpdate();
};
</script>

<template>
  <div class="page-content">
    <div class="bg-dash-dark-2 py-4">
      <div class="container-fluid">
        <h2 class="h5 mb-0">Nginx Server</h2>
      </div>
    </div>

    <section v-if="nginxStore.data != null">
      <div class="container-fluid">
        <div class="row gy-4">
          <div class="col-md-4 col-sm-6">
            <div class="row gy-4">
              <div class="col-md-12">
                <div class="cpu-usage-wrapper card mb-0">
                  <div class="card-body">
                    <p class="text-xxl lh-1 mb-0" :class="{'text-color-primary': nginxStore.data.details.state === 'running', 'text-color-danger': nginxState !== 'running'}">
                      {{ nginxStore.data.details.state }}
                    </p>
                    <div class="me-2">
                      <p class="text-sm text-gray-600 mt-2 mb-0">Since {{ nginxStore.data.details.started_at }}</p>
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
                    <Logs v-if="nginx != null" :raw-logs="nginxStore.data.status" :display-lines="false" />
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div class="col-md-6">
            <div class="row gy-4">
              <div class="col-12">
                <div class="row">
                  <div class="col-6">

                    <div v-if="nginxStore.metrics != null" class="cpu-usage-wrapper card mb-0">
                      <div class="card-body">
                        <div class="d-flex align-items-end justify-content-between mb-2">
                          <div class="me-2">
                            <img class="svg-icon svg-icon-sm svg-icon-heavy text-gray-600 mb-2" src="icons/processor-32.png" />
                            <p class="text-sm text-uppercase text-gray-600 lh-1 mb-0">CPU Usage</p>
                          </div>
                          <p class="text-xxl lh-1 mb-0" :class="metricTextColorClass(nginxStore.metrics.cpu_usage)" >{{ nginxStore.metrics.cpu_usage }}%</p>
                        </div>
                        <div class="progress" style="height: 3px">
                          <div class="progress-bar" :class="metricBgColorClass(nginxStore.metrics.cpu_usage)" role="progressbar" :style="{width: Math.ceil(nginxStore.metrics.cpu_usage).toString() + '%'}" :aria-valuenow="parseInt(nginxStore.metrics.cpu_usage).toString()" aria-valuemin="0" aria-valuemax="100"></div>
                        </div>
                      </div>
                    </div>
                  </div>

                  <div class="col-6">
                    <div v-if="nginxStore.metrics != null" class="card mb-0">
                      <div class="card-body">
                        <div class="d-flex align-items-end justify-content-between mb-2">
                          <div class="me-2">
                            <svg class="svg-icon svg-icon-sm svg-icon-heavy text-gray-600 mb-2">
                              <use xlink:href="#stack-1"></use>
                            </svg>
                            <p class="text-sm text-uppercase text-gray-600 lh-1 mb-0">Memory</p>
                          </div>
                          <p class="text-xxl lh-1 mb-0" :class="metricTextColorClass(nginxStore.metrics.memory.percent)">{{ parseInt(nginxStore.metrics.memory.used).toString() }} MB</p>
                        </div>
                        <div class="progress" style="height: 3px">
                          <div class="progress-bar" :class="metricBgColorClass(nginxStore.metrics.memory.percent)" role="progressbar" :style="{width: parseInt(nginxStore.metrics.memory.percent).toString() + '%'}" :aria-valuenow="parseInt(nginxStore.metrics.memory.percent).toString()" aria-valuemin="0" aria-valuemax="100"></div>
                        </div>
                      </div>
                    </div>
                  </div>

                </div>
              </div>
              <div class="col-12">
                <div class="cpu-usage-wrapper card mb-0">
                  <div class="card-body">
                    <div class="me-2 mb-2">
<!--                      <p class="text-sm text-gray-600 mt-2 mb-0">Logs:</p>-->
                      <select v-model="selectedLogFile" @change="updateLogs()" class="form-select mb-3" name="account">
                        <option selected value="/var/log/nginx/error.log">Error logs (/var/log/nginx/error.log)</option>
                        <option value="/var/log/nginx/access.log">Access logs (/var/log/nginx/access.log)</option>
                      </select>
                    </div>
                    <Logs v-if="selectedLogFile != null" ref="logsComponentRef" :display-lines="true" />
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
