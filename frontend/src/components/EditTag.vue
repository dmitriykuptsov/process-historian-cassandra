<template>
  <div class="modal-mask">
    <OkModal
      v-if="showError"
      v-bind:message="errorMessage"
      v-bind:header="errorHeader"
      v-on:confirm="hideErrorMessage"
    />
    <EditFilter
      v-if="showEditFilter"
      v-bind:tag="tag"
      v-bind:type="selectedType"
      v-bind:name="selectedNmae"
      v-bind:threshold="threshold"
      v-on:save="hideEditFilter"
      v-on:cancel="hideEditFilter"
    />
    <AddFilter
      v-if="showAddFilter"
      v-bind:tag="tag"
      v-on:save="hideEditFilter"
      v-on:cancel="hideEditFilter"
    />
    <Spinner v-if="showSpinner" />
    <div class="modal-window">
      <div class="header">Editing of existing tag</div>
      <div class="body">
        <form class="login-form">
          <div class="form-group">
            <label>Tag name</label>
            <input
              type="text"
              class="form-control form-control-lg"
              v-model="sensor.tag"
              disabled
            />
          </div>
          <div class="form-group">
            <label>Tag description</label>
            <input
              type="text"
              class="form-control form-control-lg"
              v-model="sensor.description"
            />
          </div>
          <div class="form-group">
            <label>Master secret</label>
            <input
              type="text"
              class="form-control form-control-lg"
              v-model="sensor.secret"
            />
          </div>
          <div class="form-group">
            <label>Is public</label>
            <select
              class="form-select"
              v-model="sensor.is_public"
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
            <span v-for="a in sensor.attributes" v-bind:key="a" class="badge rounded-pill bg-danger">
                {{a}} <a href="#" @click="removeAttribute(e, a)">X</a>
            </span>
          </div>
          <div class="form-group">
            <button class="btn btn-danger" @click="addFilter($event, sensor.tag)">Add filter</button>
            <br/>
            <label>Added filters</label><br/>
            <table class="table table-striped">
              <thead>
                <tr>
                  <th>Filter type</th>
                  <th>Filter threshold</th>
                  <th>Action</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="f in sensor.filters" v-bind:key="f.filter_name">
                  <td>{{f.filter_name}} </td>
                  <td>{{f.value}} </td>
                  <td>
                    <button class="btn btn-danger" @click="editFilter($event, sensor.tag, f.filter_name, f.filter, f.value)">Edit</button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
          <div class="form-group" style="margin-top: 10px">
            <button @click="save" class="btn btn-dark btn-lg btn-block save">
              Update tag
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
import EditFilter from "../components/EditFilter.vue";
import AddFilter from "../components/AddFilter.vue";

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
      selectedType: null,
      threshold: 0.0,
      selectedNmae: null,
      showAddFilter: false,
      showEditFilter: false,
      errorHeader: "Error",
      errorMessage: "",
      showSpinner: false,
      selectedTag: "",
      sensor: {}
    };
  },
  methods: {
    editFilter(e, tag, filter_name, type, value) {
      this.selectedTag = tag
      this.selectedNmae = filter_name
      this.selectedType = type
      this.threshold = value
      this.showEditFilter = true;
      e.preventDefault()
    },
    addFilter(e, tag) {
      this.selectedTag = tag
      this.showAddFilter = true;
      e.preventDefault()
    },
    hideEditFilter() {
      this.showAddFilter = false;
      this.showEditFilter = false;
      this.getSensor()
    },
    hideErrorMessage() {
        this.showError = false;
    },
    addAttribute(e) {
        if (this.attribute != null || this.attribute != "") {
            this.sensor.attributes.push(this.attribute);    
        }
        this.attribute = ""
        e.preventDefault();
    },
    removeAttribute(e, a) {
        var n = []
        for (var i = 0; i < this.sensor.attributes.length; i++) {
            if (a != this.sensor.attributes[i]) {
                n.push(this.sensor.attributes[i])
            }
        }
        this.sensor.attributes = n;
        e.preventDefault();
    },
    getSensor() {
      this.showSpinner = true;
      const token = sessionStorage.getItem("token");
      const headers = {
        "Content-Type": "application/json",
        Authorization: "Bearer " + token,
      };
      const url = this.$BASE_URL + "/api/get_sensor_own/";
      axios.post(url, {
          tag: this.tag
        }, { headers }).then((response) => {
        if (!response.data.auth_fail) {
          this.sensor = response.data.result;
          if (this.sensor.is_public) {
            this.sensor.is_public = "1"
          } else {
            this.sensor.is_public = "0"
          }
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
      var url = this.$BASE_URL + "/api/update_sensor/";
      axios
        .post(url, { 
            tag: this.sensor.tag, 
            description: this.sensor.description,  
            is_public_read: this.sensor.is_public,
            secret: this.sensor.secret,
            attributes: this.sensor.attributes
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
    OkModal,
    EditFilter,
    AddFilter
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
  height: 800px;
  top: 50%;
  left: 50%;
  margin-top: -400px;
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
