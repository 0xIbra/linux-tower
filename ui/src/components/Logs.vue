<script setup lang="ts">
import {
  ref,
  onMounted,
  defineProps,
  defineExpose,
  getCurrentInstance,
} from "vue";
import axios from "axios";
import { useAuthStore } from "@/stores/auth";
import config from "../config";

const props = defineProps({
  rawLogs: String,
  arrayLogs: Array,
  displayLines: Boolean,
  defaultBgColor: {
    type: String,
    default: "#1b1e22",
  },
});

const logsEndpoint = ref();
const textLogs = ref(props.rawLogs);
const logsArray = ref(props.arrayLogs);
const startLine = ref();
const endLine = ref();
const renderedLogs = ref("");

const previousLogsLabel = ref("Previous logs");
const newerLogsLabel = ref("Newer logs");

const authStore = useAuthStore();

function render() {
  if (textLogs.value != null) {
    renderedLogs.value = textLogs.value;
  } else if (logsArray.value != null && logsArray.value.length > 0) {
    let tempLogArray = [];
    const logsArrayTemp: Array<any> = logsArray.value;
    for (let i = 0; i < logsArrayTemp.length; i++) {
      let { line, log } = logsArrayTemp[i];
      let insertLog = log;
      if (props.displayLines) {
        insertLog = `${line}: ${log}`;
      }

      tempLogArray[i] = insertLog;
    }
    renderedLogs.value = tempLogArray.join("\r\n");
  }
}

async function getLogs() {
  if (textLogs.value == null && (logsArray.value == null || logsArray.value.length === 0) && logsEndpoint.value != null) {
    try {
      const response = await axios.request({
        method: "GET",
        baseURL: config.apiBaseEndpoint,
        url: logsEndpoint.value,
        headers: { Authorization: authStore.accessToken },
      });

      logsArray.value = response.data["logs"];
      startLine.value = response.data["start_line"];
      endLine.value = response.data["end_line"];
    } catch (e: any) {
      console.error(e);
    }
  }

  render();
}

async function getPreviousLogs() {
  try {
    let startLineTemp = startLine.value - 50;
    let endLineTemp = startLine.value;

    const url = logsEndpoint.value + `&start_line=${startLineTemp}&end_line=${endLineTemp}`;
    const response: any = await axios.request({
      method: "GET",
      baseURL: config.apiBaseEndpoint,
      url,
      headers: { Authorization: authStore.accessToken },
    });

    let logs = response.data["logs"];
    if (Array.isArray(logs) && logs.length > 0) {
      logsArray.value = logs.concat(logsArray.value);
      startLine.value = startLineTemp;
      render();
    } else {
      previousLogsLabel.value = "No older logs...";

      setTimeout(() => {
        previousLogsLabel.value = "Previous logs";
      }, 3000);
    }
  } catch (e) {
    // todo
  }
}

async function getNewerLogs() {
  try {
    let startLineTemp = endLine.value;
    let endLineTemp = startLineTemp + 50;

    const url = logsEndpoint.value + `&start_line=${startLineTemp}&end_line=${endLineTemp}`;
    const response: any = await axios.request({
      method: "GET",
      baseURL: config.apiBaseEndpoint,
      url,
      headers: { Authorization: authStore.accessToken },
    });

    let logs = response.data["logs"];
    if (Array.isArray(logs) && logs.length > 0) {
      if (logsArray.value == null) {
        logsArray.value = [];
      }

      logsArray.value = logsArray.value.concat(logs);
      endLine.value = endLineTemp;
      render();
    } else {
      newerLogsLabel.value = "No new logs...";

      setTimeout(() => {
        newerLogsLabel.value = "Newer logs";
      }, 3000);
    }
  } catch (e) {
    // todo
  }
}

async function reloadLogs() {
  logsArray.value = [];
  await getLogs();

  const instance = getCurrentInstance();
  instance?.proxy?.$forceUpdate();
}

function setEndpoint(endpoint: any) {
  logsEndpoint.value = endpoint;
}

onMounted(() => {
  getLogs();
});

defineExpose({
  reloadLogs,
  setEndpoint,
});
</script>

<template>
  <div v-if="renderedLogs != null" id="code-wrap" :style="{ background: defaultBgColor }">
    <div v-if="logsEndpoint != null && renderedLogs != ''" id="previous-logs" class="logs-btn" @click="getPreviousLogs()">{{ previousLogsLabel }}</div>
    <pre v-if="renderedLogs != ''"><code>{{ renderedLogs }}</code></pre>
    <pre v-if="renderedLogs == null || renderedLogs == ''"><code>no logs found</code></pre>
    <div v-if="logsEndpoint != null && renderedLogs != ''" id="newer-logs" class="logs-btn" @click="getNewerLogs()">{{ newerLogsLabel }}</div>
  </div>
</template>

<style scoped>
#code-wrap {
  width: 100%;
  padding: 5px 10px;
  border-radius: 8px;
  box-shadow: 0px 0px 17px -10px #111;
  margin-bottom: 0 !important;
  height: 90% !important;
}

#code-wrap > pre {
  max-height: 500px;
  margin-bottom: 0 !important;
  margin-top: 10px;
}

#code-wrap .logs-btn {
  text-align: center;
  user-select: none;
  -moz-user-select: none;
  -webkit-user-select: none;
  -ms-user-select: none;
  cursor: pointer;
  background: #24282e;
  padding: 5px 0;
  font-size: 13px;
  line-height: 1;
  border-radius: 20px;
}

#code-wrap .logs-btn:hover {
  background: #353b45;
}

#code-wrap #newer-logs {
  margin-top: 5px;
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
