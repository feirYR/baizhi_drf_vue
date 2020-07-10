<template>

  <div>
  <headers></headers>
  <banner></banner>
  <foot></foot>
  </div>
</template>

<script>
    import headers from "./common/headers";
    import banner from "./common/banner";
    import foot from "./common/foot";

    export default {
        name: "home",
        components:{
          headers:headers,
          banner:banner,
          foot:foot,
        }
    }
</script>

<style scoped>

</style>
