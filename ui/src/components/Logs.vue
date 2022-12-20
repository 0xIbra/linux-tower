<script lang="ts">
export default {
  props: {
    rawLogs: String,
    displayLines: Boolean,
  },
};
</script>

<template>
  <div id="code-wrap">
    <pre>
      <code>
        {{ this.rawLogs }}
      </code>
    </pre>
  </div>
</template>

<style scoped>
#code-wrap {
  background: #202532 !important;
  padding: 10px 20px;
  border-radius: 8px;
  box-shadow: 0px 0px 17px -10px #111;
}
</style>
