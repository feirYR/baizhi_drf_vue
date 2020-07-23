<template>
     <div class="cart">
      <headers></headers>
      <div class="cart_info">
        <div class="cart_title">
          <span class="text">我的购物车</span>
          <span class="total">共{{cart_length}}门课程</span>
        </div>
        <div class="cart_table">
          <div class="cart_head_row">
            <span class="doing_row"></span>
            <span class="course_row">课程</span>
            <span class="expire_row">有效期</span>
            <span class="price_row">单价</span>
            <span class="do_more">操作</span>
          </div>
          <div class="cart_course_list" >
<!--          <div class="cart_course_list" v-for="course in courses">-->
<!--            <CartItem>{{course.course_img}}</CartItem>-->
<!--            <CartItem>{{course.name}}</CartItem>-->

            <CartItem v-for="(course,index) in courses" :course="course" :key="index"
                      @del="show_cart" @change_select="show_cart" @expire="show_cart"  @change="radio_all" :chang="all_radio"></CartItem>
          </div>
          <div class="cart_footer_row">
            <span class="cart_select"><label> <el-checkbox v-model="select_all" ></el-checkbox><span>全选</span></label></span>
            <span class="cart_delete"><i class="el-icon-delete"></i> <span>删除</span></span>
<!--            <span class="goto_pay">去结算</span>-->
              <router-link to="/order" class="goto_pay">去结算</router-link>
            <span class="cart_total">总计：¥{{total_price}}</span>
          </div>
        </div>
      </div>
      <foot></foot>
    </div>
</template>

<script>
    import headers from "./common/headers";
    import foot from "./common/foot";
    import CartItem from "./common/CartItem";
    export default {
        name: "cats",
        data(){
          return{
              select_all:'',
              courses:[],
              total_price:0.00,
              cart_length:0,
              all_radio:''

          }
        },
        components:{
           headers,foot,CartItem
        },
        watch:{
            'select_all'(){
                this.select_all_cart()
                // console.log(this.select_all,typeof this.select_all)
            }
        },
        methods:{
            check_user(){
             let token = localStorage.token || sessionStorage.token
                if (token){
                    return token
                }else {
                    let self = this
                    this.$confirm('请先登陆',{
                        callback(){
                            self.$router.push('/login')
                        }
                    })
                }
            },
            show_cart(){
                let token = this.check_user()
                this.$axios({
                    url:'http://127.0.0.1:8000/cart/cart/',
                    method: 'get',
                    headers:{
                         'Authorization':'jwt ' + token
                    },
                    params:{
                        user_id: localStorage.user_id ||sessionStorage.user_id,
                    },
                }).then(re=>{
                    // console.log(re.data)
                    this.courses = re.data['courses']
                    this.cart_length = re.data.cart_length
                    this.$store.commit('add_goods',re.data.cart_length)
                    this.get_total_price()
                    this.radio_all()

                    // this.select_all = select_all

                }).catch(error=>{
                    console.log(error)
                })
            },
            select_all_cart(){

                if (this.select_all === true){
                    this.all_radio = true
                }else{}

                // let token = this.check_user()
                // this.$axios({
                //     url: this.$settings.HOST + 'cart/select_all/',
                //     method: 'post',
                //      headers:{
                //          'Authorization':'jwt ' + token
                //     },
                //     data: {
                //         user_id: localStorage.user_id || sessionStorage.user_id,
                //         select_all: this.select_all
                //         // select: this.select_all
                //     }
                // }).then(re => {
                //     this.$message.success(re.data.message)
                //     // this.$message.success('成功')
                //     // this.show_cart()
                //     this.select_all = re.data['select_all']
                //     // console.log(re.data['select_all'])
                // }).catch(error => {
                //     this.$message.error(error.response.data.message)
                // })
            },
            radio_all(){
                // if(course_select){this.select_all = true}
                // else {this.select_all = false}
                // console.log(course_select)
                // this.select_all = course_select
                this.courses.forEach((course,key)=>{
                    if(!course.select){
                        this.select_all = false
                        forEach.breakAfter
                    }else {this.select_all = true}
                })
                // this.courses.every(function (course) {
                //    if(course.select === false){
                //        console.log(2222222)
                //         this.select_all = false
                //         return false
                //     }else{
                //         this.select_all = true
                //         return true
                //    }
                //
                // })
            },
            get_total_price(){
                // data = this.show_cart()
                // console.log(data);
                let total= 0
                this.courses.forEach((course,key)=>{
                    if(course.select){
                        total += parseFloat(course.final_expire_price)

                    }
                })
                // console.log(total)
                this.total_price = total
            }
        },
        created() {
            this.show_cart()
            this.get_total_price()
        }

    }
</script>

<style scoped>
  .cart_info {
    width: 1200px;
    margin: 0 auto 200px;
  }

  .cart_title {
    margin: 25px 0;
  }

  .cart_title .text {
    font-size: 18px;
    color: #666;
  }

  .cart_title .total {
    font-size: 12px;
    color: #d0d0d0;
  }

  .cart_table {
    width: 1170px;
  }

  .cart_table .cart_head_row {
    background: #F7F7F7;
    width: 100%;
    height: 80px;
    line-height: 80px;
    padding-right: 30px;
  }

  .cart_table .cart_head_row::after {
    content: "";
    display: block;
    clear: both;
  }

  .cart_table .cart_head_row .doing_row,
  .cart_table .cart_head_row .course_row,
  .cart_table .cart_head_row .expire_row,
  .cart_table .cart_head_row .price_row,
  .cart_table .cart_head_row .do_more {
    padding-left: 10px;
    height: 80px;
    float: left;
  }

  .cart_table .cart_head_row .doing_row {
    width: 78px;
  }

  .cart_table .cart_head_row .course_row {
    width: 530px;
  }

  .cart_table .cart_head_row .expire_row {
    width: 188px;
  }

  .cart_table .cart_head_row .price_row {
    width: 162px;
  }

  .cart_table .cart_head_row .do_more {
    width: 162px;
  }

  .cart_footer_row {
    padding-left: 30px;
    background: #F7F7F7;
    width: 100%;
    height: 80px;
    line-height: 80px;
  }

  .cart_footer_row .cart_select span {
    margin-left: -7px;
    font-size: 18px;
    color: #666;
  }

  .cart_footer_row .cart_delete {
    margin-left: 58px;
  }

  .cart_delete .el-icon-delete {
    font-size: 18px;
  }

  .cart_delete span {
    margin-left: 15px;
    cursor: pointer;
    font-size: 18px;
    color: #666;
  }

  .cart_total {
    float: right;
    margin-right: 62px;
    font-size: 18px;
    color: #666;
  }

  .goto_pay {
    float: right;
    width: 159px;
    height: 80px;
    outline: none;
    border: none;
    background: #ffc210;
    font-size: 18px;
    color: #fff;
    text-align: center;
    cursor: pointer;
  }
</style>
