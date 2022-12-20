<script lang="ts">
import { useProgramsStore } from "@/stores/programs";
import Logs from "@/components/Logs.vue";

export default {
  components: {Logs},
  data() {
    const programsStore = useProgramsStore();

    return {
      programsStore,
      apache: null,
      apacheState: null,
    };
  },

  async mounted() {
    await this.programsStore.getApache();
    this.apache = this.programsStore.apache;
    this.apacheState = this.programsStore.apache.details.state;
  },
};
</script>

<template>
  <div class="page-content">
    <div class="bg-dash-dark-2 py-4">
      <div class="container-fluid">
        <h2 class="h5 mb-0">Apache HTTP Server</h2>
      </div>
    </div>

    <section>
      <div class="container-fluid">
        <div class="row gy-4">
          <div class="col-md-3 col-sm-6">
            <div class="cpu-usage-wrapper card mb-0">
              <div class="card-body">
                <p class="text-xxl lh-1 mb-0" :class="{'text-color-primary': apacheState === 'running', 'text-color-danger': apacheState !== 'running'}">
                  {{ programsStore.apache.details.state }}
                </p>
                <div class="me-2">
                  <p class="text-sm text-gray-600 mt-2 mb-0">Since {{ programsStore.apache.details.started_at }}</p>
                </div>
              </div>
            </div>
          </div>

          <div class="col-md-8 col-sm-6">
            <div class="cpu-usage-wrapper card mb-0">
              <div class="card-body">
                <div class="me-2 mb-2">
                  <p class="text-sm text-gray-600 mt-2 mb-0">Status logs:</p>
                </div>
                <Logs v-if="apache != null" :raw-logs="apache.status" :display-lines="false" />
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>
