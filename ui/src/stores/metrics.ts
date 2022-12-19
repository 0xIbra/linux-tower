import { defineStore } from "pinia";
import axios from "axios";
import config from "../config";
import { useAuthStore } from "@/stores/auth";

export const useMetricsStore = defineStore({
  id: "metrics",
  state: () => ({
    metrics: {
      cpu_usage: 0,
      disk: {
        free: 0,
        percent: 0,
        total: 0,
        used: 0,
      },
      memory: {
        percent: 0,
        active: 0,
        available: 0,
        cached: 0,
        inactive: 0,
        free: 0,
        used: 0,
        total: 0,
      },
    },
  }),

  actions: {
    async getMetrics() {
      const authStore = useAuthStore();

      const response = await axios.request({
        method: "GET",
        baseURL: config.apiBaseEndpoint,
        url: "/api/system_metrics",
        headers: { Authorization: authStore.accessToken },
      });
      this.metrics = response.data;

      return response.data;
    },
  },
});
