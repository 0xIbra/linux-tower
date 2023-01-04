<script setup lang="ts">
import { getCurrentInstance, onMounted} from "vue";
import { useRouter } from "vue-router";
import { useAlertsStore } from "@/stores/alerts";

const router = useRouter();
const alertsStore = useAlertsStore();

onMounted(async () => {
  await alertsStore.getAlerts();
});

const showAlert = async (id: Number) => {
  await router.push("/alerts/" + id);
};

const deleteAlert = async (id: Number) => {
  await alertsStore.deleteAlert(id);

  const instance = getCurrentInstance();
  instance?.proxy?.$forceUpdate();
};

const getAlertSource = (alert: any) => {
  if (alert.alert_type === "log") {
    return alert.logfile_path;
  } else if (alert.alert_type === "metric") {
    return alert.metric_name;
  } else if (alert.alert_type === "service") {
    return alert.service_name;
  } else {
    throw new Error(`Unsupported alert type: ${alert.alert_type}`);
  }
};

const getNotificationTarget = (alert: any) => {
  let targets = [];

  if (alert.discord_webhook_url != null) {
    targets.push("discord");
  }

  if (alert.slack_webhook_url != null) {
    targets.push("slack");
  }

  if (alert.webhook_url != null) {
    targets.push("webhook");
  }

  return targets.join(", ");
};
</script>

<template>
  <div class="page-content form-page">
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
            <li class="breadcrumb-item"><router-link to="/">Host</router-link></li>
            <li class="breadcrumb-item active" aria-current="page">Alerts</li>
          </ol>
        </nav>
        <div class="mb-0 py-2">
          <router-link to="/alerts/create" class="btn btn-primary">New Alert</router-link>
        </div>
      </div>
    </div>
    <section class="tables py-0">
      <div class="container-fluid">
        <div class="row gy-4">
          <div class="col-lg-12">
            <div class="card mb-0">
              <div class="card-body pt-0">
                <div class="table-responsive">
                  <table class="table mb-0 table-striped table-hover">
                    <thead>
                      <tr>
                        <th>#</th>
                        <th>Type</th>
                        <th>Source</th>
                        <th>Notification target</th>
                        <th>Actions</th>
                      </tr>
                    </thead>
                    <tbody v-if="alertsStore.data != null">
                      <tr v-for="alertItem in alertsStore.data" class="cursor-pointer" @click="showAlert(alertItem.id)">
                        <th scope="row">{{ alertItem["id"] }}</th>
                        <td>{{ alertItem["alert_type"] }}</td>
                        <td>{{ getAlertSource(alertItem) }}</td>
                        <td>{{ getNotificationTarget(alertItem) }}</td>
                        <td>
                          <button class="btn btn-danger btn-sm btn-small" @click="deleteAlert(alertItem.id)">
                            <svg class="svg-icon svg-icon-sm">
                              <use xlink:href="#bin-1"></use>
                            </svg>
                          </button>
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<style scoped>
.btn-small > svg {
  width: 15px;
  height: 15px;
}
</style>
