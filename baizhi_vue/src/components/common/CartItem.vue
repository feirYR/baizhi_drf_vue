<template>
    <div>
        <div class="cart_item">
            <div class="cart_column column_1">
                <el-checkbox class="my_el_checkbox" v-model="course.select" ></el-checkbox>
            </div>
            <div class="cart_column column_2">
                <img :src="course.course_img" alt="">
                <!--            <img src="/static/image/python.jpg" alt="">-->
                <span>
                    <span><router-link to="/course/detail/1">{{course.name}}</router-link></span>&nbsp&nbsp&nbsp
                    <span class="discount-type" v-if="course.discount_name">{{course.discount_name}}</span>
<!--                    <div class="pay-box">-->
<!--                            <span class="discount-type" v-if="course.discount_name">{{course.discount_name}}</span>-->
<!--                    </div>-->
                </span>


            </div>

            <div class="cart_column column_3">
                <el-select v-model="course.expire_id" size="mini" placeholder="请选择购买有效期" class="my_el_select">
                    <el-option :label="item.expire_text" :value="item.expire_id" :key="item.expire_id"
                               v-for="item in course.expire_list">

                    </el-option>

                </el-select>
            </div>
            <div class="cart_column column_4">{{course.final_expire_price}}</div>
<!--            <div class="cart_column column_4">{{// this.$store.state.expire_price}}</div>-->
            <!--        <div class="cart_column column_4" @click="del_cart">删除</div>-->
            <a href="javascript:;" class="cart_column column_4" @click="del_cart">删除</a>
        </div>
    </div>
</template>

<script>
    export default {
        props: ['course','chang'],
        name: "CartItem",
        data() {
            return {
                // expire_id:0,
                // all_radio:this.chang,
                expire: '请选择购买有效期',
            }
        },
        watch: {
            'course.select'() {
                this.select_cart()
            },
            'course.expire_id'() {
               this.course_expire()

            },
            'chang'(){
                this.all_radio()
            }
        },
        methods: {
            select_cart() {
                let token = localStorage.token || sessionStorage.token
                this.$axios({
                    url: this.$settings.HOST + 'cart/cart/',
                    method: 'patch',
                    headers:{
                         'Authorization':'jwt ' + token
                    },
                    data: {
                        course_id: this.course.id,
                        user_id: localStorage.user_id || sessionStorage.user_id,
                        select: this.course.select
                    }
                }).then(re => {
                    // this.$message.success(re.data.message)

                     // console.log(re.data)
                     // console.log(re.data.select_all)
                    // let select_all = re.data.select_all
                    this.$emit('change_select')
                    // this.$parent.radio_all(select_all)
                    // this.$emit('change',this.course.select)
                    // console.log(this.course.select)

                }).catch(error => {
                    // this.$message.error('切换失败')
                })


            },
            all_radio(){

                this.course.select = this.chang
            },
            del_cart() {
                let token = localStorage.token || sessionStorage.token
                this.$axios({
                    url: this.$settings.HOST + 'cart/cart/',
                    method: 'delete',
                    headers:{
                         'Authorization':'jwt ' + token
                    },
                    data: {
                        course_id: this.course.id,
                        user_id: localStorage.user_id || sessionStorage.user_id,
                        select: this.course.select
                    }
                }).then(re => {
                    this.$message.success(re.data.message)
                    this.$emit("del")
                    // this.$message.success('成功')
                    // if (this.course.select) {
                    //     let self = this
                    //     this.$confirm('确认删除？', {
                    //         callback() {
                    //             // self.$router.push("/cart")
                    //             self.$emit("del")
                    //         }
                    //
                    //     })
                    // } else {
                    //     this.$message.error('请先选中')
                    // }

                    // this.$emit("del")
                    // console.log(re.data)
                }).catch(error => {
                    this.$message.error('删除失败')
                })
            },
            course_expire(){
                let token = localStorage.token || sessionStorage.token
                this.$axios({
                    url: this.$settings.HOST + 'cart/cart/',
                    method:'put',
                    headers:{
                         Authorization:'jwt ' + token
                    },
                    data:{
                        course_id:this.course.id,
                        expire_id:this.course.expire_id,
                        user_id: localStorage.user_id || sessionStorage.user_id,
                    }
                }).then(re=>{
                    this.$message.success('切换有效期成功')
                    // console.log(re.data)
                    // console.log(re.data['expire_price'])
                    let final_expire_price = re.data.final_expire_price
                    // let expire_id = re.data.expire_id
                    // console.log(final_expire_price)
                    this.course.final_expire_price = final_expire_price
                    this.$emit("expire")

                }).catch(error=>{
                    this.$message.error(error)
                })
            }
        },
        created() {
            // console.log(this.all_radio)
             console.log(this.chang)
            // this.course_expire()
        }
    }
</script>

<style scoped>
    .cart_item::after {
        content: "";
        display: block;
        clear: both;
    }

    .cart_column {
        float: left;
        height: 250px;
    }

    .cart_item .column_1 {
        width: 88px;
        position: relative;
    }

    .my_el_checkbox {
        position: absolute;
        left: 0;
        right: 0;
        bottom: 0;
        top: 0;
        margin: auto;
        width: 16px;
        height: 16px;
    }

    .cart_item .column_2 {
        padding: 67px 10px;
        width: 520px;
        height: 116px;
    }

    .cart_item .column_2 img {
        width: 175px;
        height: 115px;
        margin-right: 35px;
        vertical-align: middle;
    }

    .cart_item .column_3 {
        width: 197px;
        position: relative;
        padding-left: 10px;
    }

    .my_el_select {
        width: 117px;
        height: 28px;
        position: absolute;
        top: 0;
        bottom: 0;
        margin: auto;
    }

    .cart_item .column_4 {
        padding: 67px 10px;
        height: 116px;
        width: 142px;
        line-height: 116px;
    }

    .discount-type {
        padding: 6px 10px;
        font-size: 16px;
        color: #fff;
        text-align: center;
        margin-right: 8px;
        background: #fa6240;
        border: 1px solid #fa6240;
        border-radius: 10px 0 10px 0;
        /*float: left;*/
    }
    .pay-box::after {
        content: "";
        display: block;
        clear: both;
    }

</style>
