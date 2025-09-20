<template>
  <div class="login-main" style="background-color: #f1f2c2;">
    
    <div class="login-div" style="background-color: #f1f2c2;">
      <div class="login-text" style="left: -50%; top: 0%; position: relative;">
        <h3>
          Time-series storage and analytics service
        </h3>
      </div>
      <OkModal
        v-bind:header="header"
        v-bind:message="message"
        v-if="showDsModal"
        v-on:confirm="closeOkModal"
      />
      <form class="login-form" style="background-color: #f1f2c2;">
        <div class="form-group">
          <label>Username</label>
          <div class="input-group input-group-lg">
            <div class="input-group-addon">
              <span class="input-group-text">
                <BootstrapIcon icon="person" size="2x" />
              </span>
            </div>
            <input
              type="username"
              class="form-control form-control-lg"
              v-model="username"
            />
          </div>
        </div>
        <div class="form-group">
          <label>Password</label>
          <div class="input-group input-group-lg">
            <div class="input-group-append">
              <span class="input-group-text">
                <BootstrapIcon icon="lock" size="2x" />
              </span>
            </div>
            <input
              type="password"
              class="form-control form-control-lg"
              v-model="password"
            />
          </div>
        </div>
        <div class="form-group" style="margin-top: 10px">
          <button @click="login" class="btn btn-dark btn-lg btn-block btn-add">
            <BootstrapIcon icon="arrow-right-square" size="1x" />
            Login
          </button>
        </div>
        <div class="form-group" v-if="failed" style="margin-top: 10px">
          <div class="alert alert-danger" role="alert">
            Invalid username or password
          </div>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import OkModal from "../components/OkModal.vue";
import BootstrapIcon from "@dvuckovic/vue3-bootstrap-icons";

export default {
  name: "Login",
  data() {
    return {
      username: "",
      password: "",
      failed: false,
      message: "",
      header: "",
    };
  },
  methods: {
    login(e) {
      const data = { username: this.username, password: this.password };
      const headers = {
        "Content-Type": "application/json",
      };
      axios
        .post(this.$BASE_URL + "/auth/signin/", data, { headers })
        .then((response) => {
          if (response.data.success) {
            sessionStorage.setItem("token", response.data.token);
            this.$parent.isAuthenticated = true;
            this.$router.push("/sensors/");
          }
          this.failed = !response.data.success;
        });
      e.preventDefault();
    },
    closeOkModal() {
      this.showDsModal = false;
    },
  },
  components: {
    OkModal,
    BootstrapIcon,
  },
};
</script>

<style scoped>
h3 {
  color: #372d69;
  text-align: center;
}

@media (min-width: 768px) {
  .login-div {
    position: absolute;

    width: 450px;
    height: 300px;

    /* Center form on page horizontally & vertically */
    top: 300px;
    left: 50%;
    margin-top: -150px;
    margin-left: -225px;
  }

  .login-form {
    width: 450px;
    height: 300px;

    background: white;
    border-radius: 10px;

    margin: 0;
    padding: 0;
  }

  .login-text {
    margin: 10% auto;
    width: 900px;
  }
}

@media (max-width: 768px) {
  .login-text {
    margin-left: 50%;
    margin-top: 10%;
    width: 100%;
  }

  .login-div {
    position: absolute;

    width: 100%;
    height: 100%;

    /* Center form on page horizontally & vertically */
    top: 450px;
    margin-top: -300px;
  }

  .login-form {
    width: 100%;
    height: 100%;

    background: white;
    border-radius: 10px;

    margin: 0;
    padding: 0;
  }
}

.login-main {
  background-color: cadetblue;
}

</style>
