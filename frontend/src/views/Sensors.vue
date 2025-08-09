<template>
  <div class="main_content">
    <div class="sensors">
      <Spinner v-if="showSpinner" />
      <OkModal
        v-if="showAuthError"
        v-bind:message="authMessage"
        v-bind:header="authHeader"
        v-on:confirm="hideAuthMessage"
      />
      <AddTag
        v-if="showAddTag"
        v-on:save="hideAddTag"
        v-on:cancel="hideAddTag"
      />
      <EditTag
        v-if="showEditTag"
        v-bind:tag="selectedTag"
        v-on:save="hideEditTag"
        v-on:cancel="hideEditTag"
      />
      <Filter v-on:filter="filterTable" v-bind:filterVal="filter" />
      <div style="font-weight: bold; text-align: center">Your tags</div>
      <div>
        <button class="btn btn-danger" @click="addNewTag">Add tag</button>
        <Paginator
          v-bind:count="totalTags"
          v-bind:ipp="ipp"
          v-bind:currentPage="page"
          v-on:page-click="changePage"
          v-bind:autoMargin="true"
        />
        <table class="table table-striped">
          <thead>
            <tr>
              <th scope="col">#</th>
              <th scope="col">
                Tag name
              </th>
              <th scope="col">
                Tag description
              </th>
              <th scope="col">
                Is public
              </th>
              <th scope="col">
                Master secret
              </th>
              <th scope="col">
                Attributes
              </th>
              <th>
                Delete tag
              </th>
              <th>
                Edit tag
              </th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(s, index) in sensors" v-bind:key="s.tag">
              <th scope="row">{{index + 1}}</th>
              <td>{{s.tag}}</td>
              <td>{{s.description}}</td>
              <td>
                <span class="badge rounded-pill bg-danger">
                  {{s.is_public != 0}}
                </span>
                
              </td>
              <td>{{s.secret}}</td>
              <td>
                <span v-for="a in s.attributes" v-bind:key="a" class="badge rounded-pill bg-danger">
                  {{a}}
                </span>
              </td>
              <td>
                <button class="btn btn-danger" @click="remoteTag(s.tag)">Delete</button>
              </td>
              <td>
                <button class="btn btn-primary"  @click="callEditTag(s.tag)">Edit</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>

import axios from "axios";
import Paginator from "../components/Paginator.vue";
import Filter from "../components/Filter.vue";
import Spinner from "../components/Spinner.vue";
import OkModal from "../components/OkModal.vue";
import AddTag from "../components/AddTag.vue";
import EditTag from "../components/EditTag.vue";

export default {
  name: "Sensors",
  data() {
    return {
      loaded: true,
      page: 1,
      ipp: 10,
      filter: "",
      totalTags: 0,
      loadedTags: 0,
      showSpinner: true,
      sensors: [],
      showAddTag: false,
      showEditTag: false,
      selectedTag: null
    };
  },
  methods: {
    addNewTag() {
      this.showAddTag = true;
    },
    hideAddTag() {
      this.showAddTag = false;
      this.countSensors()
      this.getSensors()
    },
    callEditTag(tag) {
      this.selectedTag = tag;
      this.showEditTag = true;
      
    },
    hideEditTag() {
      this.showEditTag = false;
      this.countSensors()
      this.getSensors()
    },
    remoteTag(tag) {
      const token = sessionStorage.getItem("token");
      const headers = {
        "Content-Type": "application/json",
        Authorization: "Bearer " + token,
      };
      const url = this.$BASE_URL + "/api/delete_sensor/";
      axios.post(url, {
          tag: tag
        }, { headers }).then((response) => {
        if (!response.data.auth_fail) {
          this.page = 1;
          this.countSensors();
          this.getSensors();
        }
      });
    },
    countSensors() {
      const token = sessionStorage.getItem("token");
      const headers = {
        "Content-Type": "application/json",
        Authorization: "Bearer " + token,
      };
      var url = this.$BASE_URL + "/api/count_own_sensors/";
      axios
        .post(url, { tag: this.filter }, { headers })
        .then((response) => {
          if (!response.data.auth_fail) {
            this.totalTags = response.data.result;
          }
        });
    },
    getSensors() {
      const offset = (this.page - 1) * this.ipp;
      const token = sessionStorage.getItem("token");
      const headers = {
        "Content-Type": "application/json",
        Authorization: "Bearer " + token,
      };
      const url = this.$BASE_URL + "/api/get_sensors_own/";
      axios.post(url, {
          tag: this.filter, offset: offset, limit: this.ipp
        }, { headers }).then((response) => {
        if (!response.data.auth_fail) {
          this.sensors = response.data.result;
          this.showSpinner = false;
        }
      });
    },
    changePage(o) {
      this.page = o.page;
      this.getSensors();
    },
    filterTable(filter) {
      this.page = 1;
      this.filter = filter;
      this.countSensors();
      this.getSensors();
    },
  },
  components: {
    Paginator,
    Filter,
    Spinner,
    OkModal,
    AddTag,
    EditTag
  },
  mounted() {
    this.countSensors();
    this.getSensors();
  },
};
</script>

<style scoped>
.sensors {
  width: 100%;
  height: 100%;
  float: left;
  display: block;
  margin-left: 0px;
  margin-right: 0px;
}
</style>
