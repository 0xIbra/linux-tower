<script setup lang="ts">
import { onMounted, ref } from "vue";
import { useRouter, useRoute } from "vue-router";
import { useAlertsStore } from "@/stores/alerts";

const router = useRouter();
const route = useRoute();
const alertsStore = useAlertsStore();

const formError = ref(false);
const formErrorMessage = ref();
const formErrorMessages = ref({
  logfile: "",
  regex: "",
  serviceName: "",
  metricTarget: "",
});
const alertId = ref();
const selectedAlertType = ref("log");
const logFilePath = ref();
const logRegex = ref();
const serviceName = ref();
const slackWebhook = ref();
const discordWebhook = ref();
const webhookUrl = ref();
const webhookMethod = ref("GET");
const cooldownTime = ref(30);

const metricName = ref("cpu_usage");
const metricOperator = ref("gte");
const metricTargetValue = ref();

onMounted(async () => {
  if (route.name === "editAlert") {
    const id: any = route.params.id;
    const alert = await alertsStore.getAlert(id);
    if (alert == null) {
      await router.back();
    }

    alertId.value = alert.id;
    selectedAlertType.value = alert.alert_type;
    logFilePath.value = alert.logfile_path;
    logRegex.value = alert.regex;
    serviceName.value = alert.service_name;
    slackWebhook.value = alert.slack_webhook_url;
    discordWebhook.value = alert.discord_webhook_url;
    cooldownTime.value = alert.cooldown_time;
    metricName.value = alert.metric_name;
    if (alert.metric_rule != null) {
      metricOperator.value = alert.metric_rule.operator;
      metricTargetValue.value = alert.metric_rule.target_value;
    }
  }
});

const submitForm = async (submitEvent: any) => {
  submitEvent.preventDefault();

  formError.value = false;
  formErrorMessages.value.logfile = "";
  formErrorMessages.value.regex = "";
  formErrorMessages.value.serviceName = "";
  formErrorMessages.value.metricTarget = "";

  const alert: any = {
    alert_type: selectedAlertType.value,
  };

  if (route.name === "editAlert") {
    alert.id = alertId.value;
  }

  if (selectedAlertType.value === "log") {
    if (logFilePath.value == null) {
      formErrorMessages.value.logfile = "Please provide the log file path";
      formError.value = true;
    }

    if (logRegex.value == null) {
      formErrorMessages.value.regex = "Please provide a valid regex";
      formError.value = true;
    }

    alert.logfile_path = logFilePath.value;
    alert.regex = logRegex.value;
  } else if (selectedAlertType.value === "metric") {
    if (metricTargetValue.value == null) {
      formErrorMessages.value.metricTarget = "Please provide a number between 1 and 100";
      formError.value = true;
    }

    alert.metric_name = metricName;
    alert.metric_rule = {
      operator: metricOperator.value,
      target_value: metricTargetValue.value,
    };
  } else if (selectedAlertType.value === "service") {
    if (serviceName.value == null) {
      formErrorMessages.value.serviceName = "Please provide the name of the service you want to monitor";
      formError.value = true;
    }

    alert.service_name = serviceName.value;
  } else {
    // todo error
  }

  alert.cooldown_time = cooldownTime.value;
  alert.slack_webhook_url = slackWebhook.value;
  alert.discord_webhook_url = discordWebhook.value;

  if (formError.value !== false) {
    return;
  }

  if (route.name === "createAlert") {
    const creation = await alertsStore.createAlert(alert);
    if (creation) {
      await router.push("/alerts");
    } else {
      formErrorMessage.value = "could not create alert.";
    }
  } else {
    const update = await alertsStore.updateAlert(alert);
    if (update) {
      await router.push("/alerts");
    } else {
      formErrorMessage.value = "could not update alert.";
    }
  }
};

const deleteAlert = async () => {
  let result = await alertsStore.deleteAlert(alertId.value);
  if (result) {
    await router.push("/alerts");
  }
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
            <li class="breadcrumb-item">
              <router-link to="/">Host</router-link>
            </li>
            <li class="breadcrumb-item">
              <router-link to="/alerts">Alerts</router-link>
            </li>
            <li v-if="alertId == null" class="breadcrumb-item active" aria-current="page">Create</li>
            <li v-if="alertId != null" class="breadcrumb-item active" aria-current="page">#{{alertId}}</li>
          </ol>
        </nav>
      </div>
    </div>
    <section class="tables py-0">
      <div class="container-fluid">
        <div class="row gy-4">
          <div class="col-lg-12">
            <div class="card mb-0">
              <div class="card-header">
              </div>
              <div class="card-body pt-0">
                <div class="my-3"></div>
                <form class="form-horizontal" @submit="submitForm">
                  <div class="row">
                    <label class="col-sm-3 form-label">Alert type</label>
                    <div class="col-sm-9">
                      <select v-model="selectedAlertType" class="form-select mb-3" name="alert_type">
                        <option value="log">Log</option>
                        <option value="metric">Metric</option>
                        <option value="service">Service</option>
                      </select>
                    </div>

                    <label v-if="selectedAlertType === 'log'" class="col-sm-3 form-label">Log file</label>
                    <div v-if="selectedAlertType === 'log'" class="col-sm-9 mb-3">
                      <input v-model="logFilePath" class="form-control" :class="{'is-invalid': formErrorMessages.logfile != ''}" type="text" placeholder="example: /var/log/apache2/error.log">
                      <div v-if="formErrorMessages.logfile != ''" class="invalid-feedback">{{ formErrorMessages.logfile }}</div>
                    </div>

                    <label v-if="selectedAlertType === 'log'" class="col-sm-3 form-label">Regex</label>
                    <div v-if="selectedAlertType === 'log'" class="col-sm-9 mb-3">
                      <input v-model="logRegex" class="form-control" :class="{'is-invalid': formErrorMessages.regex != ''}" type="text" placeholder="(error|critical)">
                      <div v-if="formErrorMessages.regex != ''" class="invalid-feedback">{{ formErrorMessages.regex }}</div>
                      <small>regex to test for triggering this alert, for example detecting error logs.</small>
                    </div>

                    <label v-if="selectedAlertType === 'service'" class="col-sm-3 form-label">Service name</label>
                    <div v-if="selectedAlertType === 'service'" class="col-sm-9 mb-3">
                      <input v-model="serviceName" class="form-control" :class="{'is-invalid': formErrorMessages.serviceName != ''}" type="text" placeholder="nginx">
                      <div v-if="formErrorMessages.serviceName != ''" class="invalid-feedback">{{ formErrorMessages.serviceName }}</div>
                      <small>SystemD service like <b>apache2</b> or <b>nginx</b>, this alert will be triggered if the provided service goes down.</small>
                    </div>

                    <label v-if="selectedAlertType === 'metric'" class="col-sm-3 form-label">Choose metric</label>
                    <div v-if="selectedAlertType === 'metric'" class="col-sm-9 col-lg-2 mb-2">
                      <select v-model="metricName" class="form-select">
                        <option value="cpu_usage" selected>CPU usage</option>
                        <option value="memory_percent">Memory usage</option>
                        <option value="disk_percent">Disk usage</option>
                      </select>
                    </div>

                    <div v-if="selectedAlertType === 'metric'" class="col-sm-9 col-lg-1 mb-2">
                      <select v-model="metricOperator" class="form-select">
                        <option value="eq" selected>==</option>
                        <option value="gt">&gt;</option>
                        <option value="lt">&lt;</option>
                        <option value="gte">&gt;=</option>
                        <option value="lte">&lt;=</option>
                      </select>
                    </div>

                    <div v-if="selectedAlertType === 'metric'" class="col-sm-9 col-lg-2 mb-3">
                      <input v-model="metricTargetValue" class="form-control" :class="{'is-invalid': formErrorMessages.metricTarget != ''}" type="number" placeholder="90%">
                      <div v-if="formErrorMessages.metricTarget != ''" class="invalid-feedback">{{ formErrorMessages.metricTarget }}</div>
                    </div>

                    <div class="col-12"></div>

                    <label class="col-sm-3 form-label">Cooldown time</label>
                    <div class="col-sm-9 mb-3">
                      <input v-model="cooldownTime" class="form-control" type="number" placeholder="default: 30">
                      <small>Time (seconds) to wait before triggering the alert again. To avoid spam</small>
                    </div>

                    <label class="col-sm-3 form-label">Slack webhook URL</label>
                    <div class="col-sm-9">
                      <input v-model="slackWebhook" class="form-control mb-3" type="text" placeholder="slack webhook...">
                    </div>

                    <label class="col-sm-3 form-label">Discord webhook URL</label>
                    <div class="col-sm-9">
                      <input v-model="discordWebhook" class="form-control mb-3" type="text" placeholder="discord webhook...">
                    </div>

                    <div class="col-sm-9 ms-auto">
                      <div v-if="formErrorMessage != null" class="error-wrapper mt-3 mb-3">
                        <div class="js-validate-error-label" style="color: #B81111">{{ formErrorMessage }}</div>
                      </div>
                    </div>

                    <div class="my-2"></div>

                    <div class="col-sm-9 ms-auto">
                      <button v-if="alertId == null" class="btn btn-primary" type="submit">Save</button>
                      <button v-if="alertId != null" class="btn btn-primary" type="submit">Save changes</button>
                      <button v-if="alertId != null" class="btn btn-danger" @click="deleteAlert">Delete</button>
                    </div>

                    <div class="my-2"></div>
                  </div>
                </form>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<style scoped>
.btn {
  margin-right: 5px;
}
</style>
