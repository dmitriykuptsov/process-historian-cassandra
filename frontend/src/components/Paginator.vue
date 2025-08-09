<template>
  <div class="paginator" style="border-style: none" v-if="numPages > 1">
    <div
      class="paginator-page1"
      v-bind:class="autoMargin == true ? 'container' : ''"
      style="border-style: none"
    >
      <div class="info">
        Total number of pages: {{ numPages }} Number of tags:
        {{ count }} Current page: {{ currentPage }}
      </div>
      <button
        @click="prev"
        class="btn btn-dark btn-lg btn-block paginator-btn"
        style="float: left"
        v-if="showArrows"
      >
        <!-- BootstrapIcon icon="arrow-left" / -->
        &lt;
      </button>
      <button
        v-for="page in pageRange"
        v-bind:key="page"
        @click="navigate($event, page)"
        class="btn btn-dark btn-lg btn-block paginator-btn"
        style="float: left"
        v-bind:class="page == selected ? 'active' : ''"
      >
        {{ page }}
      </button>
      <button
        @click="next"
        class="btn btn-dark btn-lg btn-block paginator-btn"
        style="float: left"
        v-if="showArrows"
      >
        <!-- BootstrapIcon icon="arrow-right" / -->
        &gt;
      </button>
      <div style="margin-bottom: 30px; height: 30px"></div>
    </div>
  </div>
</template>

<script>
//import BootstrapIcon from "@dvuckovic/vue3-bootstrap-icons";

export default {
  name: "Paginator",
  props: ["count", "ipp", "currentPage", "autoMargin"],
  data() {
    return {
      maxPages: 10,
      numPages: Math.ceil(this.count / this.ipp),
      pageRange: [],
      selected: 1,
      showArrows: false,
    };
  },
  watch: {
    count: {
      deep: true,
      handler(n) {
        this.numPages = Math.ceil(n / this.ipp);
        this.pageRange = [];
        if (this.maxPages < this.numPages) {
          this.showArrows = true;
          for (var i = 1; i <= this.maxPages; i++) {
            this.pageRange.push(i);
          }
        } else {
          for (var j = 1; j <= this.numPages; j++) {
            this.pageRange.push(j);
          }
        }
      },
    },
    currentPage: {
      deep: true,
      handler(n) {
        if (n == 1) {
          this.pageRange = [];
          if (this.maxPages < this.numPages) {
            this.showArrows = true;
            for (var i = 1; i <= this.maxPages; i++) {
              this.pageRange.push(i);
            }
          } else {
            for (var j = 1; j <= this.numPages; j++) {
              this.pageRange.push(j);
            }
          }
        }
        this.selected = n;
      },
    },
  },
  methods: {
    next() {
      if (
        this.selected == this.pageRange[this.maxPages - 1] &&
        this.selected + 1 <= this.numPages
      ) {
        this.pageRange.shift();
        this.pageRange.push(this.selected + 1);
        this.selected++;
        this.$emit("page-click", { page: this.selected });
      } else if (this.selected + 1 <= this.numPages) {
        this.selected++;
        this.$emit("page-click", { page: this.selected });
      }
    },
    prev() {
      if (this.selected == this.pageRange[0] && this.selected - 1 > 0) {
        this.pageRange.pop();
        this.pageRange.unshift(this.selected - 1);
        this.selected--;
        this.$emit("page-click", { page: this.selected });
      } else if (this.selected - 1 > 0) {
        this.selected--;
        this.$emit("page-click", { page: this.selected });
      }
    },
    navigate(e, page) {
      e.preventDefault();
      this.selected = page;
      this.$emit("page-click", { page: page });
    },
  },
  components: {
    //BootstrapIcon,
  },
  mounted() {
    console.log("Number of pages " + this.numPages);
    this.selected = 1;
    if (this.maxPages < this.numPages) {
      this.showArrows = true;
      for (var i = this.selected; i < this.selected + this.maxPages; i++) {
        this.pageRange.push(i);
      }
    } else {
      for (var j = 1; j <= this.numPages; j++) {
        this.pageRange.push(j);
      }
    }
  },
  updated() {
    console.log("Number of pages " + this.numPages);
    if (this.pageRange.length == 0) {
      this.selected = 1;
      if (this.maxPages < this.numPages) {
        this.showArrows = true;
        for (var i = this.selected; i < this.selected + this.maxPages; i++) {
          this.pageRange.push(i);
        }
      } else {
        for (var j = 1; j <= this.numPages; j++) {
          this.pageRange.push(j);
        }
      }
      this.$emit("page-click", { page: this.selected });
    }
  },
};
</script>

<style scoped>
.container {
  margin: auto;
  width: 820px;
  height: 30px;
  font-weight: bolder;
  font-family: "Gill Sans", "Gill Sans MT", Calibri, "Trebuchet MS", sans-serif;
  border-style: none !important;
  border-top: none !important;
  border-bottom: none !important;
  margin-bottom: 30px !important;
  padding-bottom: 30px !important;
}

.paginator {
  width: calc(100%);
  height: 30px;
  font-weight: bolder;
  font-family: "Gill Sans", "Gill Sans MT", Calibri, "Trebuchet MS", sans-serif;
  border-style: none !important;
  border-top: none !important;
  border-bottom: none !important;
}

.active {
  background-color: #180e49 !important;
  color: #fff9a4;
}

.paginator-btn {
  background-color: #372d69;
  width: 60px;
  margin-right: 5px;
  border-style: none !important;
  border-top: none !important;
  border-bottom: none !important;
}
/* .paginator-page1 {
  width: auto !important;
  margin: 0 auto;
} */
.add {
  border-top: none !important;
  border-bottom: none !important;
}
</style>
