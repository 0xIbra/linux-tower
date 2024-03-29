<script setup lang="ts">
import { onMounted, ref } from "vue";
import { useRouter, useRoute } from "vue-router";
import axios from "axios";
import { useAuthStore } from "@/stores/auth";
import config from "../config";

const router = useRouter();
const route = useRoute();

const authStore = useAuthStore();

const liveTail = ref(false);
const currentType = ref("tail");

const logFilePath = ref("/var/log/syslog");
const filterRegex = ref("");
const startLine = ref();
const endLine = ref();

const logFileError = ref("");

const logs = ref([]);

const tailLogs = async (start = null, end = null) => {
  currentType.value = "tail";

  let params: any = {
    log_file: logFilePath.value,
    lines: 100,
  };

  if (start != null) {
    params.start_line = start;
  }
  if (end != null) {
    params.end_line = end;
  }

  params = new URLSearchParams(params);

  const response = await axios.request({
    method: "GET",
    baseURL: config.apiBaseEndpoint,
    url: "/api/logs/tail?" + params.toString(),
    headers: { Authorization: authStore.accessToken },
  });

  return {
    logs: response.data["logs"],
    start: response.data["start_line"],
    end: response.data["end_line"],
  };
};

const queryLogs = async () => {
  currentType.value = "query";

  const params = new URLSearchParams({
    log_file: logFilePath.value,
    query: filterRegex.value,
  }).toString();

  const response = await axios.request({
    method: "GET",
    baseURL: config.apiBaseEndpoint,
    url: "/api/logs/query?" + params,
    headers: { Authorization: authStore.accessToken },
  });

  return {
    logs: response.data["logs"],
    start: response.data["start_line"],
    end: response.data["end_line"],
  };
};

const previous = async () => {
  let start: any;
  let end: any;
  if (currentType.value === "tail") {
    start = startLine.value - 100;
    end = startLine.value;
  }

  const res = await tailLogs(start, end);
  startLine.value = res.start;

  logs.value = res.logs.concat(logs.value);
};

const render = () => {
  let raw = logs.value.map((_) => _["log"]);
  return raw.join("\n");
};

const update = async (e: any) => {
  e.preventDefault();
  logs.value = [];
  logFileError.value = "";

  if (liveTail.value === true) {
    return;
  }

  try {
    let res: any;
    if (filterRegex.value != "" && filterRegex.value != null) {
      res = await queryLogs();
      logs.value = res.logs;
    } else {
      res = await tailLogs();
      logs.value = res.logs;
    }

    if (res) {
      startLine.value = res.start;
      endLine.value = res.end;
    }
  } catch (e: any) {
    logFileError.value = e.response.data["detail"];
  }
};

onMounted(async () => {
  const res = await tailLogs();
  logs.value = res.logs;
  startLine.value = res.start;
  endLine.value = res.end;
});
</script>

<template>
  <div class="page-content form-page h-100">
    <form @submit="update">
      <!-- Breadcrumb-->
      <div class="container-fluid py-2 h-100">
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
          <div class="row">
            <div class="col-lg-10">
              <div class="row">
                <div class="col-lg-12">
                  <div class="card">
                    <div class="card-body pt-0 modernize">
                      <div class="input-group">
                        <span class="input-group-text" id="file-field-icon">
                          <svg class="svg-icon svg-icon-sm">
                            <use xlink:href="#literature-1"></use>
                          </svg>
                        </span>
                        <input v-model="logFilePath" id="logfilePath" class="form-control modernize h-modernize" :class="{'is-invalid': logFileError != ''}" type="text" placeholder="search for logs using regex" />
                      </div>
                    </div>
                  </div>
                </div>

                <div class="col-xl-12">
                  <div class="card mt-2">
                    <div class="card-body pt-0 modernize">
                      <div v-if="!liveTail" class="text-center p-0 m-0 pt-1 pb-1 cursor-pointer load-more" @click="previous">Load more</div>
                      <div id="logs-wrapper">
                        <p v-for="logItem in logs" class="log-text">{{ logItem.log.replace(/(.{220})..+/, "$1&hellip;") }}</p>
                      </div>
                      <div v-if="liveTail" class="text-center p-0 m-0 pt-1 pb-1 bg-color-primary text-white">
                        waiting on live logs...
                        <span class="spinner"></span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <div class="col-lg-2">
              <div class="row sticky-top">
                <div class="col-12">
                  <div class="card mb-0">
                    <div class="card-body p-0">
                      <input v-model="filterRegex" class="form-control modernize h-modernize" type="text" placeholder="Filter logs">
                    </div>
                  </div>
                </div>

                <div class="col-12 mt-2">
                  <div class="flex">
                    <a class="btn w-100" :class="{'btn-outline-secondary': !liveTail, 'btn-secondary': liveTail}" @click="liveTail = !liveTail">Live tail</a>
                  </div>
                </div>

                <div class="col-12 mt-2">
                  <div class="flex">
                    <button type="submit" class="btn btn-primary w-100" v-bind:disabled="liveTail">Query</button>
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
html, body {
  height: 100%;
}
#file-field-icon {
  background: #1b1e22 !important;
  border: none !important;
}

#logs-wrapper {
  padding: 10px 10px !important;
  font-family: "Arial", sans-serif !important;
  height: 72vh;
  overflow-y: scroll;
}

input::selection {
  color: #d9d9d9;
  background: #0c63e4;
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

input.modernize:not(.is-invalid) {
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

.load-more {
  cursor: pointer;
}

.load-more:hover {
  background: #2f333a;
}

.btn-primary[disabled] {
  background: #589b83 !important;
  border-color: #589b83 !important;
}

.sticky-top {
  top: 20px !important;
}

button:focus, input:focus {
  box-shadow: none !important;
}
</style>
