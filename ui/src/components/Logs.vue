<script setup lang="ts">
import { ref, onMounted, defineProps } from "vue";
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
  logsEndpoint: String,
});

const textLogs = ref(props.rawLogs);
const logsArray = ref(props.arrayLogs);
const startLine = ref();
const endLine = ref();
const renderedLogs = ref("");

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
  if (textLogs.value == null && logsArray.value == null) {
    try {
      const response = await axios.request({
        method: "GET",
        baseURL: config.apiBaseEndpoint,
        url: props.logsEndpoint,
        headers: { Authorization: authStore.accessToken },
      });

      logsArray.value = response.data["logs"];
      startLine.value = response.data["start_line"];
      endLine.value = response.data["end_line"];
    } catch (e) {
      console.error(e);
    }
  }

  render();
}

async function getPreviousLogs() {
  try {
    let startLineTemp = startLine.value - 50;
    let endLineTemp = startLine.value;

    const url = props.logsEndpoint + `&start_line=${startLineTemp}&end_line=${endLineTemp}`;
    const response: any = await axios.request({
      method: "GET",
      baseURL: config.apiBaseEndpoint,
      url,
      headers: { Authorization: authStore.accessToken },
    });

    let logs = response.data["logs"];
    logsArray.value = logs.concat(logsArray.value);

    startLine.value = startLineTemp;
    render();
  } catch (e) {
    // todo
  }
}

onMounted(() => {
  getLogs();
});
</script>

<template>
  <div v-if="renderedLogs != null" id="code-wrap" :style="{ background: defaultBgColor }">
    <div v-if="logsEndpoint != null" id="previous-logs" @click="getPreviousLogs()">Previous logs</div>
    <pre><code>{{ renderedLogs }}</code></pre>
  </div>
</template>

<style scoped>
#code-wrap {
  width: 100%;
  padding: 10px 10px;
  border-radius: 8px;
  box-shadow: 0px 0px 17px -10px #111;
  margin-bottom: 0 !important;
  height: 90% !important;
}

#code-wrap > pre {
  max-height: 500px;
  margin-bottom: 0 !important;
}

#code-wrap #previous-logs {
  text-align: center;
  cursor: pointer;
  background: #24282e;
  padding: 2px 0;
  font-size: 14px;
}

#code-wrap #previous-logs:hover {
  background: #353b45;
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
