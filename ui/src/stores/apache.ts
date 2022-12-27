import { defineStore } from "pinia";
import axios from "axios";
import config from "../config";
import { useAuthStore } from "@/stores/auth";

export const useApacheStore = defineStore({
  id: "apache",
  state: () => ({
    data: null as any,
    installed: true,
    metrics: {
      cpu_usage: 0.0,
      memory: {
        total: 0,
        used: 0,
        percent: 0,
      },
    },
  }),

  actions: {
    async init() {
      const authStore = useAuthStore();

      try {
        const response = await axios.request({
          method: "GET",
          baseURL: config.apiBaseEndpoint,
          url: "/api/apache/status",
          headers: { Authorization: authStore.accessToken },
        });

        this.data = response.data.data;
      } catch (e: any) {
        if (e.response.status !== 404) {
          throw e;
        }

        this.data = null;
        this.installed = false;
      }
    },

    async getMetrics() {
      const authStore = useAuthStore();

      try {
        const response = await axios.request({
          method: "GET",
          baseURL: config.apiBaseEndpoint,
          url: "/api/apache/metrics",
          headers: { Authorization: authStore.accessToken },
        });

        this.metrics = response.data;
      } catch (e) {
        // todo
      }
    },
  },
});
