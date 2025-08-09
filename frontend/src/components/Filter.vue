<template>
  <div class="filter">
    <table style="border-style: none !important; width: 100%">
      <tr style="border-style: none !important; width: 100%">
        <td style="border-style: none !important">
          <button
            @click="applyFilter"
            class="btn btn-secondary btn-lg"
            style="float: left; width: 200px"
          >
            <BootstrapIcon icon="filter" />
            Отфильтровать
          </button>
        </td>
        <td style="border-style: none !important">
          <button
            @click="clearFilter"
            class="btn btn-dark btn-lg btn-clear"
            style="float: left; width: 200px"
          >
            <BootstrapIcon icon="arrow-clockwise" />
            Очистить
          </button>
        </td>
        <td style="width: 100%">
          <input
            type="text"
            class="form-control form-control-lg"
            style="display: inline; width: calc(100%)"
            v-model="filter"
            placeholder="Введите для фильтрации"
          />
        </td>
      </tr>
    </table>
  </div>
</template>

<script>
import BootstrapIcon from "@dvuckovic/vue3-bootstrap-icons";

export default {
  name: "Filter",
  props: ["filterVal"],
  watch: {
    filterVal: {
      deep: true,
      handler(n) {
        this.filter = n;
      },
    },
  },
  data() {
    return {
      filter: "",
    };
  },
  methods: {
    applyFilter(e) {
      this.$emit("filter", this.filter);
      e.preventDefault();
    },
    clearFilter(e) {
      this.filter = "";
      this.$emit("filter", this.filter);
      e.preventDefault();
    },
  },
  components: {
    BootstrapIcon,
  },
  mounted() {},
};
</script>

<style scoped>
.filter {
  width: calc(100%);
  height: 50px;
  margin-bottom: 15px;
  padding-bottom: 65px;
  border-bottom: 3px dotted grey;
  font-weight: bolder;
  font-family: "Gill Sans", "Gill Sans MT", Calibri, "Trebuchet MS", sans-serif;
  /* border-style: none !important; */
}
</style>
