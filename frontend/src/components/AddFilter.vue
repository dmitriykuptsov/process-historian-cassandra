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
      <div class="header">Add filter to tag</div>
      <div class="body">
        <form class="login-form">
          <div class="form-group">
            <label>Tag name</label>
            <input
              type="text"
              class="form-control form-control-lg"
              v-model="selectedTag"
              disabled
            />
          </div>
          <div class="form-group">
            <label>Filer name</label>
            <select
              class="form-select"
              v-model="selectedFilter"
              aria-label="Filter name"
            >
              <option
                v-for="f in filters"
                v-bind:value="f.filter"
                v-bind:key="f.filter_name"
              >
                {{ f.filter_name }}
              </option>
            </select>
          </div>
          <div class="form-group">
            <label>Threshold</label>
            <input
              type="text"
              class="form-control form-control-lg"
              v-model="threshold"
            />
          </div>
          <div class="form-group" style="margin-top: 10px">
            <button @click="save" class="btn btn-dark btn-lg btn-block save">
              Update filter
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
  name: "AddFilter",
  props: ["tag"],
  data() {
    return {
      selectedTag: this.tag,
      selectedFilter: null,
      threshold: 0.0,
      filters: [],
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
    getFilters() {
      this.showSpinner = true;
      const token = sessionStorage.getItem("token");
      const headers = {
        "Content-Type": "application/json",
        Authorization: "Bearer " + token,
      };
      var url = this.$BASE_URL + "/api/get_filters/";
      axios
        .post(url, { 
        }, { headers })
        .then((response) => {
          this.showSpinner = false;     
          if (response.data.result) {
            this.filters = response.data.result
          } else {
            this.showError = true;
            this.errorMessage = response.data.reason
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
      var url = this.$BASE_URL + "/api/add_or_update_sensor_alerts_filter/";
      axios
        .post(url, { 
            tag: this.selectedTag, 
            filter: this.selectedFilter,
            value: this.threshold
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
    this.getFilters()
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
  width: 600px;
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
