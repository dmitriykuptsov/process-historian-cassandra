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
      <div class="header">Добавление нового пользователя</div>
      <div class="body">
        <form class="login-form">
          <div class="form-group">
            <label>Tag name</label>
            <input
              type="text"
              class="form-control form-control-lg"
              v-model="tag"
              enable="false"
            />
          </div>
          <div class="form-group">
            <label>Tag description</label>
            <input
              type="text"
              class="form-control form-control-lg"
              v-model="description"
            />
          </div>
          <div class="form-group">
            <label>Master secret</label>
            <input
              type="text"
              class="form-control form-control-lg"
              v-model="secret"
            />
          </div>
          <div class="form-group">
            <label>Is public</label>
            <select
              class="form-select"
              v-model="public_read"
              aria-label="Public"
            >
              <option
                value="1"
              >
                True
              </option>
              <option
                value="0"
              >
                False
              </option>
            </select>
          </div>
          <div class="form-group">
            <label>Attribute to add</label>
            <input
              type="text"
              class="form-control form-control-lg"
              v-model="attribute"
            />
            <button class="btn btn-danger" @click="addAttribute">Add attribute</button>
          </div>
          <div class="form-group">
            <label>Added attributes</label><br/>
            <span v-for="a in s.attributes" v-bind:key="a" class="badge rounded-pill bg-danger">
                {{a}} <a href="#" @click="removeAttribute(e, a)">X</a>
            </span>
          </div>
          <div class="form-group" style="margin-top: 10px">
            <button @click="save" class="btn btn-dark btn-lg btn-block save">
              Add tag
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
  name: "EditTag",
  props: ["tag"],
  data() {
    return {
      secret: null,
      description: null,
      public_read: false,
      attributes: [],
      attribute: null,
      showError: false,
      errorHeader: "Error",
      errorMessage: "",
      showSpinner: false
    };
  },
  methods: {
    hideErrorMessage() {
        this.showError = false;
    },
    addAttribute(e) {
        if (this.attribute != null || this.attribute != "") {
            this.attributes.push(this.attribute);    
        }
        this.attribute = ""
        e.preventDefault();
    },
    removeAttribute(e, a) {
        var n = []
        for (var i = 0; i < this.attributes.length; i++) {
            if (a != this.attributes[i]) {
                n.push(this.attributes[i])
            }
        }
        this.attributes = n;
        e.preventDefault();
    },
    getSensor() {
      this.showSpinner = true;
      const token = sessionStorage.getItem("token");
      const headers = {
        "Content-Type": "application/json",
        Authorization: "Bearer " + token,
      };
      const url = this.$BASE_URL + "/api/get_sensors_own/";
      axios.post(url, {
          tag: this.tag
        }, { headers }).then((response) => {
        if (!response.data.auth_fail) {
          this.sensor = response.data.result;
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
      var url = this.$BASE_URL + "/api/add_sensor/";
      axios
        .post(url, { 
            tag: this.tag, 
            description: this.description,  
            is_public_read: this.public_read,
            secret: this.secret,
            attributes: this.attributes
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
    this.getSensor(this.tag)
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
