<template>
<div class="footer">
    <ul   >
       <li v-for="(foot,index) in foots" :key="index"   v-if=" foot.position == 1"><span style="float: left">{{foot.title}}</span></li>
    </ul>
<!--  <ul class="nav full-left" v-for="(header,index) in foots" :key="index"  v-if=" header.position == 0">-->
<!--                    <li><span>{{header.title}}</span></li>-->
<!--                </ul>-->
<!--      <ul >-->
<!--      <li>关于我们</li>-->
<!--      <li>联系我们</li>-->
<!--      <li>百知教育</li>-->
<!--      <li>帮助中心</li>-->
<!--      <li>意见反馈</li>-->
<!--      <li>新手指南</li>-->
<!--    </ul>-->

  </div>
</template>

<script>
    export default {
        name: "foot",
         data(){
          return{
            foots:[],
          }
        },
        created() {
          this.$axios({
            url:'http://127.0.0.1:8000/home/nav/',
            method:'get',
          }).then(re=>{
            // console.log('查询页尾成功',re.data)
            this.foots = re.data

          }).catch(error=>{
            console.log(error);
          })
        }
    }
</script>

<style scoped>
    .footer {
    width: 100%;
    height: 128px;
    background: #25292e;
    color: #fff;
  }

  .footer ul {
    margin: 0 auto 16px;
    padding-top: 38px;
    width: 810px;
  }

  .footer ul li {
    float: left;
    width: 112px;
    margin: 0 10px;
    text-align: center;
    font-size: 14px;
  }

  .footer ul::after {
    content: "";
    display: block;
    clear: both;
  }

  .footer p {
    text-align: center;
    font-size: 12px;
  }
</style>
