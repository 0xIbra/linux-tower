import { defineStore } from "pinia";
import axios from "axios";
import config from "../config";
import router from "../router";

// @ts-ignore
export const useAuthStore = defineStore("auth", {
  state: () => ({
    user: null,
    accessToken: localStorage.getItem("access_token"),
    issuedAt: null,
    expiresIn: null,
  }),
  persist: true,

  actions: {
    async login(username: string, password: string) {
      const headers = { "Content-Type": "application/json" };

      try {
        const response: any = await axios.request({
          method: "POST",
          baseURL: config.apiBaseEndpoint,
          url: "/api/auth",
          data: { username, password },
          headers,
        });

        // authentication happens very fast, waiting 1 second for ux purpose
        await new Promise((resolve) => setTimeout(resolve, 1000));

        this.accessToken = response.data["access_token"];
        if (this.accessToken != null) {
          localStorage.setItem("access_token", this.accessToken);
        }

        return true;
      } catch (e: any) {
        if (e.response.status != null) {
          const code = e.response.status;
          const detail = e.response.data.detail;

          return { error: true, code, detail };
        }

        return null;
      }
    },

    isAuthenticated(): boolean {
      return this.accessToken != null;
    },

    async isSessionActive() {
      if (this.accessToken == null) {
        return false;
      }

      try {
        const response: any = await axios.request({
          method: "GET",
          baseURL: config.apiBaseEndpoint,
          url: "/api/system_metrics",
          headers: { Authorization: this.accessToken },
        });

        if (response.status !== 200) {
          return false;
        }
      } catch (e) {
        return false;
      }

      return true;
    },

    reset() {
      localStorage.clear();
      this.accessToken = null;
      router.push("/login");
    },
  },
});
