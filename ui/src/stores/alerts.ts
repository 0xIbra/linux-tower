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

    async getAlert(id: Number) {
      try {
        const response = await axios.request({
          method: "GET",
          baseURL: config.apiBaseEndpoint,
          url: "/api/alerts/" + id,
          headers: { Authorization: this.authStore.accessToken },
        });

        if (response.status === 200) {
          return response.data;
        }
      } catch (e) {}

      return null;
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

    async updateAlert(alert: any) {
      try {
        const response = await axios.request({
          method: "PUT",
          baseURL: config.apiBaseEndpoint,
          url: "/api/alerts/" + alert.id,
          headers: { Authorization: this.authStore.accessToken },
          data: alert,
        });

        if (response.status === 200) {
          return true;
        }
      } catch (e) {}

      return false;
    },

    async deleteAlert(id: Number) {
      try {
        const response = await axios.request({
          method: "DELETE",
          baseURL: config.apiBaseEndpoint,
          url: "/api/alerts/" + id,
          headers: { Authorization: this.authStore.accessToken },
        });

        if (response.status === 200) {
          return true;
        }
      } catch (e) {}

      return false;
    }
  },
});
