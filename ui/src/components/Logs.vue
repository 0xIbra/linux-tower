<script lang="ts">
import axios from "axios";
import { useAuthStore } from "@/stores/auth";
import config from "../config";

export default {
  props: {
    rawLogs: String,
    arrayLogs: Array,
    displayLines: Boolean,
    defaultBgColor: {
      type: String,
      default: "#1b1e22",
    },
    logsEndpoint: String,
  },

  data() {
    return {
      textLogs: this.rawLogs,
      logsArray: this.arrayLogs,
      startLine: null,
      endLine: null,
      renderedLogs: null,
    };
  },

  async mounted() {
    await this.getLogs();
  },

  methods: {
    async getLogs() {
      if (this.textLogs == null && this.logsArray == null) {
        const authStore = useAuthStore();
        try {
          const response = await axios.request({
            method: "GET",
            baseURL: config.apiBaseEndpoint,
            url: this.logsEndpoint,
            headers: { Authorization: authStore.accessToken },
          });

          this.logsArray = response.data["logs"];
          this.startLine = response.data["start_line"];
          this.endLine = response.data["end_line"];
        } catch (e) {
          console.error(e);
        }
      }

      this.render();
    },

    render() {
      // console.log(this.arrayLogs);

      if (this.textLogs != null) {
        this.renderedLogs = this.textLogs;
      } else if (this.logsArray != null && this.logsArray.length > 0) {
        let tempLogArray = [];
        for (let i = 0; i < this.logsArray.length; i++) {
          let {line, log} = this.logsArray[i];
          let insertLog = log;
          if (this.displayLines) {
            insertLog = `${line}: ${log}`
          }

          tempLogArray[i] = insertLog;
        }
        this.renderedLogs = tempLogArray.join("\r\n");
      }
    },

    async getPreviousLogs() {
      const authStore = useAuthStore();
      try {
        let startLine = this.startLine - 50;
        let endLine = this.startLine;

        const response: any = await axios.request({
          method: "GET",
          baseURL: config.apiBaseEndpoint,
          url: this.logsEndpoint + `&start_line=${startLine}&end_line=${endLine}`,
          headers: { Authorization: authStore.accessToken },
        });

        let logs = response.data["logs"];
        // for (let i = 0; i < logs.length; i++) {
        //   let item = logs.length;
        //   this.logsArray.unshift(item);
        // }

        this.logsArray = logs.concat(this.logsArray);

        this.startLine = startLine;
        this.render();
      } catch (e) {
        // todo
      }
    },

    getNextLogs() {

    },
  },
};
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
