<template>
  <div class="modal-mask">
    <OkModal
      v-if="showError"
      v-bind:message="errorMessage"
      v-bind:header="errorHeader"
      v-on:confirm="hideErrorMessage"
    />
    <Spinner v-if="showSpinner" />
    <div class="modal-window">
      <div class="header">Editing user information</div>
      <div class="body">
        <form class="login-form">
          <div class="form-group">
            <label>Username</label>
            <input
              type="text"
              class="form-control form-control-lg"
              v-model="user.username"
              disabled
            />
          </div>
          <div class="form-group">
            <label>Email</label>
            <input
              type="text"
              class="form-control form-control-lg"
              v-model="user.email"
              disabled
            />
          </div>
          <div class="form-group">
            <label>New password</label>
            <input
              type="text"
              class="form-control form-control-lg"
              v-model="user.password"
            />
          </div>
          <div class="form-group" style="margin-top: 10px">
            <button @click="save" class="btn btn-dark btn-lg btn-block save">
              Update user
            </button>
            <button @click="cancel" class="btn btn-dark btn-lg btn-block close">
              Cancel
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import Spinner from "../components/Spinner.vue";
import OkModal from "../components/OkModal.vue";

export default {
  name: "EditUser",
  props: [],
  data() {
    return {
      username: null,
      email: null,
      password: null,
      showError: false,
      errorHeader: "Error",
      errorMessage: "",
      showSpinner: false,
      user: {}
    };
  },
  methods: {
    hideErrorMessage() {
        this.showError = false;
    },
    getUser() {
      this.showSpinner = true;
      const token = sessionStorage.getItem("token");
      const headers = {
        "Content-Type": "application/json",
        Authorization: "Bearer " + token,
      };
      const url = this.$BASE_URL + "/api/get_user/";
      axios.post(url, {
        }, { headers }).then((response) => {
        if (!response.data.auth_fail) {
          this.user = response.data.result;
          this.showSpinner = false;
        }
      });
    },
    save(e) {
      this.showSpinner = true;
      const token = sessionStorage.getItem("token");
      const headers = {
        "Content-Type": "application/json",
        Authorization: "Bearer " + token,
      };
      var url = this.$BASE_URL + "/api/update_password/";
      axios
        .post(url, { 
            username: this.user.username, 
            password: this.user.password
        }, { headers })
        .then((response) => {
          this.showSpinner = false;
          if (response.data.result) {
            this.$emit("save", {});
            e.preventDefault();
          } else {
            this.showError = true;
            this.errorMessage = response.data.reason
            e.preventDefault();
          }
        });
        e.preventDefault();
    },
    cancel(e) {
      this.$emit("cancel", {});
      e.preventDefault();
    }
  },
  mounted() {
    this.getUser()
  },
  components: {
    Spinner,
    OkModal
  }
};
</script>

<style scoped>
.modal-mask {
  position: fixed;
  z-index: 9998;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  transition: opacity 0.3s ease;
}

.modal-window {
  border: rgb(169, 255, 202);
  background-color: white;
  position: fixed;
  width: 500px;
  height: 600px;
  top: 50%;
  left: 50%;
  margin-top: -250px;
  margin-left: -250px;
  z-index: 100;
}

.header {
  height: 30px;
  width: 100%;
  background-color: rgb(143, 150, 150);
  text-align: center;
  font-weight: bold;
}

.body {
  font-weight: bolder;
  color: black;
  text-align: center;
}

.close {
  position: absolute;
  bottom: 10px;
  right: 10px;
}

.save {
  position: absolute;
  bottom: 10px;
  left: 10px;
}
</style>
