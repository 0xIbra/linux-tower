import { defineStore } from "pinia";
import axios from "axios";
import config from "../config";
import { useAuthStore } from "@/stores/auth";

export const useMetricsStore = defineStore({
  id: "metrics",
  state: () => ({
    authStore: useAuthStore(),
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
      const response = await axios.request({
        method: "GET",
        baseURL: config.apiBaseEndpoint,
        url: "/api/system_metrics",
        headers: { Authorization: this.authStore.accessToken },
      });
      this.metrics = response.data;

      return response.data;
    },

    async getCpuMetricsData() {
      try {
        const response = await axios.request({
          method: "GET",
          baseURL: config.apiBaseEndpoint,
          url: "/api/metrics/cpu",
          headers: { Authorization: this.authStore.accessToken },
        });

        return response.data;
      } catch (e) {
        // TODO
      }
    },

    async getMemoryMetricsData() {
      try {
        const response = await axios.request({
          method: "GET",
          baseURL: config.apiBaseEndpoint,
          url: "/api/metrics/memory",
          headers: { Authorization: this.authStore.accessToken },
        });

        return response.data;
      } catch (e) {
        // TODO
      }
    },

    async getDiskMetricsData() {
      try {
        const response = await axios.request({
          method: "GET",
          baseURL: config.apiBaseEndpoint,
          url: "/api/metrics/disk",
          headers: { Authorization: this.authStore.accessToken },
        });

        return response.data;
      } catch (e) {
        // TODO
      }
    },
  },
});
