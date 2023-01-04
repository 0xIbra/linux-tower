import { defineStore } from "pinia";
import axios from "axios";
import config from "../config";
import { useAuthStore } from "@/stores/auth";

export const useAlertsStore = defineStore({
  id: "alerts",
  state: () => ({
    data: null as any,
    authStore: useAuthStore(),
  }),

  actions: {
    async getAlerts() {
      try {
        const response = await axios.request({
          method: "GET",
          baseURL: config.apiBaseEndpoint,
          url: "/api/alerts",
          headers: { Authorization: this.authStore.accessToken },
        });

        if (Array.isArray(response.data)) {
          this.data = response.data;
        }

        return this.data;
      } catch (e: any) {
        this.data = null;

        throw e;
      }
    },

    async createAlert(alert: any) {
      try {
        const response = await axios.request({
          method: "POST",
          baseURL: config.apiBaseEndpoint,
          url: "/api/alerts",
          headers: { Authorization: this.authStore.accessToken, "Content-Type": "application/json" },
          data: alert,
        });

        if (response.status === 200) {
          return true;
        }
      } catch (e) {}

      return false;
    },
  },
});
