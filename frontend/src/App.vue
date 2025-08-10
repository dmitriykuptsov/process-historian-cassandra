<template>
  <div>
    <div v-if="isAuthenticated">
      <header>
        <div class="title">
          <span id="caption-text">Time-series storage and analytics service by StrangeBit</span>
        </div>
        <EditUser
          v-if="showEditUser"
          v-on:save="hideEditUser"
          v-on:cancel="hideEditUser"
        />
        <div class="menu_container">
          <div class="menu">
            <div id="nav">
              <router-link to="/sensors" class="nav-btn" @click="setActive('sensors')" v-bind:class="
                menuItemsActive['sensors'] ? 'selected-menu-item' : ''
              ">Sensors</router-link>
              <router-link to="/data" class="nav-btn" @click="setActive('data')" v-bind:class="
                menuItemsActive['data'] ? 'selected-menu-item' : ''
              ">Data explorer</router-link>
              <button class="btn btn-danger" style="margin-right: 20px;">
                <a href="#" @click="callEditUser()" >Edit user</a>
              </button>
              <button id="exit-btn">
                <a href="#" @click="logout()">Logout</a>
              </button>
            </div>
          </div>
        </div>
      </header>
      <div class="main_content_container">
        <div class="main_content"></div>
      </div>
      <footer></footer>

      <router-view></router-view>
    </div>
    <div v-if="!isAuthenticated">
      <img class="strangebit" src="@/assets/distributed-database.png" alt="Database"/>
      <Login />
      <pre><code>
      # Python client usage example
      client = PHClient("https://process-historian.strangebit.io/")
      # Open the connection and authenticate
      client.open("admin", "password")
      data = []
      # Add data points
      current_datetime = datetime.now(UTC)
      value = random.randint(0, 100)
      data.append({
        "timestamp": current_datetime.timestamp() * 1000,
        "value": value
      })
      # Store the data in the cloud
      client.add_data_batch("demo_temperature_tag", data, "master-secret")

      </code></pre>
      <div class="demo" id="demo">
        <p class="demo_title">
          Demo temperature reading from the internal sensor of NanoPi R2S
          Tag: demo_temperature_tag, start time: {{format_date(start)}}, end time: {{format_date(end)}} UTC
        </p>
        <!-- p class="demo_title" style="font-weight: bold;">
          Summary statistics: Mean={{Math.round(mean*10)/10}}, max={{Math.round(max*10)/10}}, min={{Math.round(min*10)/10}}
        </p-->
        
        <div v-if="chartData.length > 1">
          <GChart
            type="LineChart"
            :data="chartData"
            :options="chartOptions"
          />
        </div>
        <div v-if="chartData.length <= 1">
          <p style="font-weight: bold; font-size: 20px;">No data available for the selected period and tag</p>
        </div>
        <div>
          <p class="summary_title" style="font-weight: bold;">
            Summary statistics
          </p>
          <table class="table table-striped">
            <thead>
              <tr>
                <th>Statistic</th>
                <th>Measurement</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>Number of measurements</td>
                <td>{{n}}</td>
              </tr>
              <tr>
                <td>Minimum value</td>
                <td>{{Math.round(min*10)/10}}</td>
              </tr>
              <tr>
                <td>Maximum value</td>
                <td>{{Math.round(max*10)/10}}</td>
              </tr>
              <tr>
                <td>Mean value</td>
                <td>{{Math.round(mean*10)/10}}</td>
              </tr>
              <tr>
                <td>Standard deviation</td>
                <td>{{Math.round(std*10)/10}}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
      <div style="position: absolute; top: 10px; left: 10px; font-weight: bold; font-size: 12px;">
        Powered by StrangeBit company
      </div>
      <div style="position: absolute; top: 30px; left: 10px; font-weight: bold; font-size: 12px;">
        <a href="https://github.com/dmitriykuptsov/process-historian-cassandra"><img src="@/assets/github.png" height="40"/></a>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import Login from "@/views/Login.vue";
import { GChart } from 'vue-google-charts';
import EditUser from "./components/EditUser.vue";

export default {
  name: "App",
  data() {
    return {
      isAuthenticated: false,
      loaded: false,
      menuItemsActive: {},
      showEditUser: false,
      data: [],
      min: 0,
      max: 0,
      sum: 0,
      mean: 0,
      std: 0,
      n: 0,
      start: Date(),
      end: Date(),
      chartData: [['Date', 'Value']],
      chartOptions: {
        title: 'Temperature sensor demo real-time data',
        width: document.getElementById("demo"),
        hAxis: {
          title: 'Date',
          format: 'MMM d, y', // Example date format
        },
        vAxis: {
          title: 'Temperature, Celcius',
        },
        legend: { position: 'bottom' },
      }
    };
  },
  methods: {
    callEditUser() {
      this.showEditUser = true;
    },
    hideEditUser() {
      this.showEditUser = false;
    },
    checkAuth() {
      const token = sessionStorage.getItem("token");
      const headers = {
        "Content-Type": "application/json",
        Authorization: "Bearer " + token,
      };
      const url = this.$BASE_URL + "/auth/validate_token/";
      axios.post(url, {}, { headers }).then((response) => {
        this.loaded = true;
        if (response.data.valid) {
          this.isAuthenticated = true;
        } else {
          this.isAuthenticated = false;
        }
      });
    },
    comlete_number(n) {
      if (n < 10) {
        return "0" + n
      } else {
        return n;
      }
    },
    format_date(date) {
      if (!date) return;
      try {
        const year = date.getFullYear();
        const month = date.getMonth() + 1;
        const day = date.getDate();
        const hours = date.getHours();
        const minutes = date.getMinutes();
        const seconds = date.getSeconds();
        var fd = year + "-" + this.comlete_number(month) + 
          "-" + this.comlete_number(day) + " " + this.comlete_number(hours) + ":" + 
          this.comlete_number(minutes) + ":" + this.comlete_number(seconds)
        return fd
      } catch(e) {
        return ""
      }      
    },
    getDemoTagData() {
      var start = new Date();
      var end = new Date()
      start.setHours(start.getHours() - 6);
      this.start = start;
      this.end = end;
      const data = {tag: "demo_temperature_tag", start: this.format_date(start), end: this.format_date(end)}
      const headers = {
        "Content-Type": "application/json"
      };
      axios
        .post(this.$BASE_URL + "/api/get_data_raw_public/", data, { headers })
        .then((response) => {
            this.data = response.data.result;
            this.chartData = [['Date', 'Value']];
            this.sum = 0;
            this.mean = 0;
            this.min = 1000000;
            this.max = -1000000;
            this.n = 0
            this.std = 0
            for (var i = 0; i < this.data.length; i++) {
              this.histogramData.push([this.data[i]["value"]]);
              this.chartData.push([new Date(this.data[i]["timestamp"] * 1000), this.data[i]["value"]]);
              this.sum += this.data[i]["value"]
              if (this.data[i]["value"] > this.max) {
                this.max = this.data[i]["value"]
              }
              if (this.data[i]["value"] < this.min) {
                this.min = this.data[i]["value"]
              }
              this.n += 1  
            }

            this.mean = this.sum / this.n;

            for (i = 0; i < this.data.length; i++) {
              this.std += (this.data[i]["value"] - this.mean) * (this.data[i]["value"] - this.mean)
            }
            this.std = this.std / this.n
            this.std = Math.sqrt(this.std)
        });
    },
    logout() {
      sessionStorage.setItem("token", null);
      this.isAuthenticated = false;
      this.$router.push("/");
      this.initializeSelectedMenu();
    },
    pollAuthData() {
      this.polling = setInterval(() => {
        this.checkAuth();
      }, 60000);
    },
    pollDemoTagData() {
      this.polling = setInterval(() => {
        this.getDemoTagData()
      }, 60000);
    },
    setActive(item) {
      this.menuItemsActive["sensors"] = false;
      this.menuItemsActive["data"] = false;
      this.menuItemsActive[item] = true;
    },
    initializeSelectedMenu() {
      this.menuItemsActive["sensors"] = true;
      this.menuItemsActive["data"] = false;
      
    },
  },
  mounted() {
    this.getDemoTagData();
    this.checkAuth();
    this.pollAuthData();
    this.pollDemoTagData();
    this.$router.push("/sensors");
    this.initializeSelectedMenu();
  },
  components: {
    Login,
    GChart,
    EditUser,
  },
};
</script>

<style scoped>

pre {
    position: absolute;
    bottom: 300px;
    width: 400px;
    background-color: #f4f4f4;
    color: darkgreen;
    border: 1px solid #ccc;
    padding: 10px;
    border-radius: 10px;
    overflow-x: auto; 
}

code {
    font-size: 8px;
    color: darkgreen;
    font-family: "Courier New", Courier, monospace;
}

.strangebit {
  position: absolute;
  left: 45%;
  top: 50px;
}

#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  width: 100%;
}

.demo_title {
  color:darkgray;
  width: 50%;
  margin-left: 25%;
}

.demo {
  position: absolute;
  top: 600px;
  width: 80%;
  margin-left: 10%;
}

#nav {
  padding: 25px 30px;
  margin: 0 auto;
}

#nav a {
  font-weight: bold;
  color: #ffffff;
  /* min-height: 75px; */
  font-family: "Dazzed", sans-serif;
  /* align-items: center; */
  text-decoration: none;
  margin: 0 1px;
}

#caption-text {
  font-size: 18px;
}

#logo {
  position: absolute;
  bottom: 20px;
  margin-left: 20px;
}

#logo_top {
  position: absolute;
  display: block;
  margin-left: 3.4%;
}

.nav-btn {
  display: inline-block;
  height: 35px;
  max-width: 100%;
  align-items: center;
  line-height: 2.28571em;
  vertical-align: middle;
  padding: 0 6px;
}

.nav-btn:hover {
  color: rgb(255, 255, 255);
  box-shadow: transparent 0px 0px 0px 2px;
  background-color: rgba(120, 119, 125, 0.6);
  transition: background 0.1s ease-out 0s,
    box-shadow 0.15s cubic-bezier(0.47, 0.03, 0.49, 1.38) 0s;
  border-radius: 3px;
}

.nav-btn:focus {
  background-color: rgba(106, 103, 121, 0.6);
  border-radius: 3px;
}

#exit-btn {
  background-color: rgb(79, 67, 140);
  border-style: none;
  border-radius: 3px;
  display: inline-flex;
  height: 35px;
  max-width: 100%;
  align-items: center;
  line-height: 2.28571em;
  vertical-align: middle;
  padding: 0 6px;
}

#exit-btn:hover {
  background-color: rgba(79, 67, 140, 0.8);
  box-shadow: transparent 0px 0px 0px 2px;
  transition: background 0.1s ease-out 0s,
    box-shadow 0.15s cubic-bezier(0.47, 0.03, 0.49, 1.38) 0s;
  border-radius: 3px;
}

#exit-btn:focus {
  background-color: inherit;
}

.title {
  width: 100%;
  display: block;
  position: fixed;
  top: 0%;
  z-index: 1;
  background: #ffffff;
  text-align: center;
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  font-weight: bold;
}

.selected-menu-item {
  color: rgb(255, 255, 255);
  box-shadow: transparent 0px 0px 0px 2px;
  background-color: rgba(120, 119, 125, 0.6);
  transition: background 0.1s ease-out 0s,
    box-shadow 0.15s cubic-bezier(0.47, 0.03, 0.49, 1.38) 0s;
  border-radius: 3px;
}
</style>
