<script setup lang="ts">
import { onMounted, ref } from "vue";
import { useRouter, useRoute } from "vue-router";
import axios from "axios";
import { useAuthStore } from "@/stores/auth";
import config from "../config";

const router = useRouter();
const route = useRoute();

const authStore = useAuthStore();

const logFilePath = ref("/var/log/apache2/access.log");
const logs = ref([]);

const tailLogs = async (logFile: String) => {
  const response = await axios.request({
    method: "GET",
    baseURL: config.apiBaseEndpoint,
    url: "/api/logs/tail?log_file=" + logFile,
    headers: { Authorization: authStore.accessToken },
  });

  return response.data["logs"];
};

const render = () => {
  let raw = logs.value.map((_) => _["log"]);
  return raw.join("\n");
};

const update = async (e: any) => {
  e.preventDefault();

  logs.value = await tailLogs(logFilePath.value);
};

onMounted(async () => {
  logs.value = await tailLogs(logFilePath.value);
});
</script>

<template>
  <div class="page-content form-page">
    <form @submit="update">
      <!-- Page Header-->
      <div class="bg-dash-dark-2 py-4">
        <div class="container-fluid">
          <h2 class="h5 mb-0">Alerts</h2>
        </div>
      </div>
      <!-- Breadcrumb-->
      <div class="container-fluid py-2">
        <div class="flex justify-content-space-between">
          <nav aria-label="breadcrumb">
            <ol class="breadcrumb mb-0 py-3">
              <li class="breadcrumb-item">
                <router-link to="/">Host</router-link>
              </li>
              <li class="breadcrumb-item active" aria-current="page">Logs</li>
            </ol>
          </nav>
        </div>
      </div>
      <section class="tables py-0">
        <div class="container-fluid">
          <div class="row gy-4">
            <div class="col-lg-10">
              <div class="row">
                <div class="col-12">
                  <div class="card">
                    <div class="card-body pt-0 modernize">
                      <div class="input-group">
                        <span class="input-group-text" id="basic-addon1">
                          <svg class="svg-icon svg-icon-sm">
                            <use xlink:href="#document-saved-1"></use>
                          </svg>
                        </span>
                        <input v-model="logFilePath" class="form-control modernize h-modernize" type="text" placeholder="search for logs using regex" />
                      </div>
                    </div>
                  </div>
                </div>

                <div class="col-12">
                  <div class="card mt-2">
                    <div class="card-body pt-0 modernize">
                      <div id="logs-wrapper">
                        <p v-for="logItem in logs" class="log-text">{{ logItem.log }}</p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <div class="col-lg-2">
              <div class="row">
                <div class="col-12">
                  <div class="card mb-0">
                    <div class="card-body p-0">
                      <input class="form-control modernize h-modernize" type="text" placeholder="Filter logs">
                    </div>
                  </div>
                </div>

                <div class="col-12 mt-2">
                  <div class="flex">
                    <button type="submit" class="btn btn-primary w-100">Query</button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>
    </form>
  </div>
</template>

<style scoped>
#logs-wrapper {
  padding: 10px 10px !important;
  font-family: "Arial", sans-serif !important;
}

.log-text {
  font-size: 13px;
  cursor: pointer;
  padding: 3px 5px;
  margin: 0 !important;
  white-space: nowrap;
  text-overflow: ellipsis;
  overflow: hidden;
  border-top: solid 1px #3c414a;
}

.log-text:hover {
  background: #353941;
}

input.modernize {
  background: #22252a !important;
  border: 0 !important;
}

input.h-modernize {
  padding-top: 10px !important;
  padding-bottom: 10px !important;
}

.card-body.modernize {
  padding: 0 !important;
}

/* width */
::-webkit-scrollbar {
  height: 10px;
}

/* Track */
::-webkit-scrollbar-track {
  background: #1b1e22;
}

/* Handle */
::-webkit-scrollbar-thumb {
  background: #2f333a;
  border-radius: 10px;
}

/* Handle on hover */
::-webkit-scrollbar-thumb:hover {
  background: #474d58;
}

::-webkit-scrollbar-corner {
}
</style>
