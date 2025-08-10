<template>
  <div class="main_content">
    <div class="data">
      <div style="font-weight: bold; text-align: center">
        Data explorer
      </div>
      <form class="data-options-form">
          <div class="form-group" style="width: 30%; float:left; margin-right: 20px;">
            <label>Start time</label>
            <input
              type="datetime-local"
              class="form-control form-control-lg"
              v-model="start"
            />
          </div>
          <div class="form-group" style="width: 30%; float:left; margin-right: 20px;">
            <label>End time</label>
            <input
              type="datetime-local"
              class="form-control form-control-lg"
              v-model="end"
            />
          </div>
          <div class="form-group" style="width: 30%; float:left; margin-right: 20px;">
            <label>Tag name</label>
            <input
              type="text"
              class="form-control form-control-lg"
              v-model="tag"
              @keyup="getSensor"
            />
            <ul style="list-style-type: none;">
              <li 
                v-for="(sensor, index) in sensors" 
                :key="index" 
                @click="selectTag(sensor.tag)"
                :class="{ 'highlighted': index === highlightedIndex }"
              >
                <span @click="selectTag(sensor.tag)" class="badge rounded-pill bg-danger">{{ sensor.tag }}</span>
              </li>
            </ul>
          </div>
          
          <div class="form-group" style="margin-top: 10px">
            <button @click="showData" class="btn btn-danger btn-lg btn-block">
              Show data
            </button>
          </div>
        </form>
        <div v-if="chartData.length > 1">
          <div style="width: 45%; float:left; margin-right: 20px;">
            <GChart
              type="LineChart"
              :data="chartData"
              :options="chartOptions"
              :height="400" 
            />
          </div>
          <div style="width: 45%; float:left; margin-right: 20px;">
            <GChart
              type="Histogram"
              :data="histogramData"
              :options="histChartOptions"
              :height="400" 
            />
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
        <div v-if="chartData.length <= 1">
          <p style="font-weight: bold; font-size: 20px;">No data available for the selected period and tag</p>
        </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { GChart } from 'vue-google-charts';
export default {
  name: "DataExplorer",
  data() {
    return {
      loaded: true,
      data: [],
      sensors: [],
      start: null,
      end: null,
      min: 0,
      max: 0,
      sum: 0,
      mean: 0,
      std: 0,
      n: 0,
      chartData: [['Date', 'Measurement']],
      histogramData: [['Measurement']],
      chartOptions: {
        height: 400,
        hAxis: {
          title: 'Date',
          format: 'MMM d, y',
        },
        vAxis: {
          title: 'Tag values',
        },
        legend: { position: 'bottom' },
      },
      histChartOptions: {
        height: 400,
        title: 'Distribution of values over time',
        legend: { position: 'none' },
        histogram: { bucketSize: 1 },
        vAxis: { title: 'Count' }
      }
    };
  },
  methods: {
    selectTag(tag) {
      this.sensors = [];
      this.tag = tag;
    },
    getSensor() {
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
          if(response.data.result) {
            this.sensors = response.data.result;
          }
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
    showData(e) {
      var start = new Date(this.start);
      var end = new Date(this.end)
      const data = {tag: this.tag, start: this.format_date(start), end: this.format_date(end)}
      const token = sessionStorage.getItem("token");
      const headers = {
        "Content-Type": "application/json",
        Authorization: "Bearer " + token,
      };
      axios
        .post(this.$BASE_URL + "/api/get_data_raw/", data, { headers })
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
      e.preventDefault();
    },},
  components: {
    GChart
  },
  mounted() {},
};
</script>

<style scoped>
.data {
  width: 100%;
  height: 100%;
  float: right;
  display: inline;
  margin-left: 0px;
  margin-right: 0px;
}

.summary_title {
  color:darkgray;
  width: 50%;
  margin-left: 25%;
}
</style>
