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
  },
});
