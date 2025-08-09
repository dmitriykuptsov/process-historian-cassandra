<template>
  <div class="main_content">
    <div class="sensors">
      <div style="font-weight: bold; text-align: center">Your tags</div>
    </div>
  </div>
</template>

<script>

export default {
  name: "Sensors",
  data() {
    return {
      loaded: true,
    };
  },
  methods: {},
  components: {
  },
  mounted() {},
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
