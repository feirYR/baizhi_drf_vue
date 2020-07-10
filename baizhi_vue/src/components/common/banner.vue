<template>
<el-carousel height="720px" :interval="3000" arrow="always">
    <el-carousel-item v-for="(banner,index) in banners" :key="index" >
        <img :src="banner.image" alt="">
    </el-carousel-item>

</el-carousel>
</template>

<script>
    export default {
        name: "banner",
        data(){
          return{
            banners:[]
          }
        },
        created() {
          this.$axios({
            url:'http://127.0.0.1:8000/home/banner/',
            method:'get',
          }).then(re=>{
            // console.log('查询轮播成功',re.data)
            this.banners = re.data

          }).catch(error=>{
            console.log(error);
          })
        }
    }
</script>

<style scoped>
  .el-carousel__item h3 {
    color: #475669;
    font-size: 18px;
    opacity: 0.75;
    line-height: 300px;
    margin: 0;
  }

  .el-carousel__item:nth-child(2n) {
    background-color: #99a9bf;
  }

  .el-carousel__item:nth-child(2n+1) {
    background-color: #d3dce6;
  }
</style>
