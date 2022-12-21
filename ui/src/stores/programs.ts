import { defineStore } from "pinia";
import axios from "axios";
import config from "../config";
import { useAuthStore } from "@/stores/auth";

export const useProgramsStore = defineStore({
  id: "programs",
  state: () => ({
    apache: null as any,
    nginx: null,
    certbot: null,
  }),

  actions: {
    async init() {
      await this.getApache();
      await this.getNginx();
    },

    async getApache() {
      const authStore = useAuthStore();

      try {
        const response = await axios.request({
          method: "GET",
          baseURL: config.apiBaseEndpoint,
          url: "/api/apache/status",
          headers: { Authorization: authStore.accessToken },
        });

        this.apache = response.data.data;
      } catch (e: any) {
        if (e.response.status !== 404) {
          throw e;
        }

        this.apache = null;
      }
    },

    async getNginx() {
      const authStore = useAuthStore();

      try {
        const response = await axios.request({
          method: "GET",
          baseURL: config.apiBaseEndpoint,
          url: "/api/nginx/status",
          headers: { Authorization: authStore.accessToken },
        });

        this.nginx = response.data;
      } catch (e: any) {
        if (e.response.status !== 404) {
          throw e;
        }

        this.nginx = null;
      }
    },
  },
});
