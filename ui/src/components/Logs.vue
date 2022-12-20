<script lang="ts">
export default {
  props: {
    rawLogs: String,
    arrayLogs: Array,
    displayLines: Boolean,
    defaultBgColor: {
      type: String,
      default: "#1b1e22",
    },
  },

  methods: {
    showLogs() {
      let logs: String;

      if (this.rawLogs != null) {
        logs = this.rawLogs;
      } else if (this.arrayLogs.length > 0) {
        let tempLogArray = [];
        for (let i = 0; i < this.arrayLogs.length; i++) {
          let { line, log } = this.arrayLogs[i];
          let insertLog = log;
          if (this.displayLines) {
            insertLog = `${line}: ${log}`
          }

          tempLogArray[i] = insertLog;
        }
        logs = tempLogArray.join("\r\n");
      } else {
        logs = "";
      }

      return logs;
    },
  },
};
</script>

<template>
  <div id="code-wrap" :style="{ background: defaultBgColor }">
    <pre><code>{{ showLogs() }}</code></pre>
  </div>
</template>

<style scoped>
#code-wrap {
  padding: 10px 10px;
  border-radius: 8px;
  box-shadow: 0px 0px 17px -10px #111;
  margin-bottom: 0 !important;
}

#code-wrap > pre {
  margin-bottom: 0 !important;
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
</style>
