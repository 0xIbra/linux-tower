<script lang="ts">
import { useAuthStore } from "@/stores/auth";

export default {
  data() {
    return {
      username: "",
      password: "",
      errorMessage: "",
      loading: false,
    };
  },

  mounted() {
    const authStore: any = useAuthStore();

    if (authStore.isAuthenticated()) {
      this.$router.push("/");
    }
  },

  methods: {
    async login(submitEvent: any) {
      this.loading = true;
      submitEvent.preventDefault();
      const authStore: any = useAuthStore();
      let data = await authStore.login(this.username, this.password);

      if (data === true) {
        await new Promise(resolve => setTimeout(resolve, 1000));
      }

      this.loading = false;

      if (data.error === true) {
        this.errorMessage = data.detail;
      }

      if (data === true && authStore.isAuthenticated()) {
        this.$router.push("/");
      }
    },
  },
};
</script>

<template>
  <div class="login-page">
    <div class="container d-flex align-items-center position-relative py-5">
      <div class="card shadow-sm w-100 rounded overflow-hidden bg-none">
        <div class="card-body p-0">
          <div class="row gx-0 align-items-stretch">
            <!-- Logo & Information Panel-->
            <div class="col-lg-6">
              <div class="info d-flex justify-content-center flex-column p-4 h-100">
                <div class="py-5">
                  <h1 class="display-6 fw-bold">Linux Tower</h1>
                  <p class="fw-light mb-0">Connect with your linux user.</p>
                </div>
              </div>
            </div>
            <!-- Form Panel    -->
            <div class="col-lg-6 bg-white">
              <div class="d-flex align-items-center px-4 px-lg-5 h-100 bg-dash-dark-2">
                <form class="login-form py-5 w-100" @submit="login">
                  <div class="input-material-group mb-3">
                    <input v-model="username" class="input-material" id="login-username" type="text" name="loginUsername" autocomplete="off" required data-validate-field="loginUsername">
                    <label class="label-material active" for="login-username">Username</label>
                  </div>
                  <div class="input-material-group mb-4">
                    <input v-model="password" class="input-material" id="login-password" type="password" name="loginPassword" required data-validate-field="loginPassword">
                    <label class="label-material active" for="login-password">Password</label>
                  </div>

                  <div v-if="errorMessage != null" class="error-wrapper">
                    <div class="js-validate-error-label" style="color: #B81111">{{ errorMessage }}</div>
                    <br>
                  </div>

                  <button class="btn btn-primary mb-3 button" v-bind:class="(loading)?'button--loading':''" id="login" type="submit">
                    <span class="button__text">Login</span>
                  </button>
                  <br>
                </form>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
