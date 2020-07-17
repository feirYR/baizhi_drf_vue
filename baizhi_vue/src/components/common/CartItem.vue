<template>
    <div>
        <div class="cart_item">
            <div class="cart_column column_1">
                <el-checkbox class="my_el_checkbox" v-model="course.select"></el-checkbox>
            </div>
            <div class="cart_column column_2">
                <img :src="course.course_img" alt="">
                <!--            <img src="/static/image/python.jpg" alt="">-->
                <span><router-link to="/course/detail/1">{{course.name}}</router-link></span>
            </div>
            <div class="cart_column column_3">
                <el-select v-model="expire" size="mini" placeholder="请选择购买有效期" class="my_el_select">
                    <el-option label="1个月有效" value="30" key="30"></el-option>
                    <el-option label="2个月有效" value="60" key="60"></el-option>
                    <el-option label="3个月有效" value="90" key="90"></el-option>
                    <el-option label="永久有效" value="10000" key="10000"></el-option>
                </el-select>
            </div>
            <div class="cart_column column_4">{{course.price}}</div>
            <!--        <div class="cart_column column_4" @click="del_cart">删除</div>-->
            <a href="javascript:;" class="cart_column column_4" @click="del_cart">删除</a>
        </div>
    </div>
</template>

<script>
    export default {
        props: ['course'],
        name: "CartItem",
        data() {
            return {
                courses: [],

                expire: '永久有效',
            }
        },
        watch: {
            'course.select': function () {
                this.select_cart()
            }
        },
        methods: {
            select_cart() {
                this.$axios({
                    url: this.$settings.HOST + 'cart/cart/',
                    method: 'patch',
                    data: {
                        course_id: this.course.id,
                        user_id: localStorage.user_id || sessionStorage.user_id,
                        select: this.course.select
                    }
                }).then(re => {
                    this.$message.success(re.data.message)
                    // this.$message.success('成功')
                    console.log(re.data)
                }).catch(error => {
                    this.$message.error('切换失败')
                })


            },
            del_cart() {
                this.$axios({
                    url: this.$settings.HOST + 'cart/cart/',
                    method: 'delete',
                    data: {
                        course_id: this.course.id,
                        user_id: localStorage.user_id || sessionStorage.user_id,
                        select: this.course.select
                    }
                }).then(re => {
                    // this.$message.success(re.data.message)
                    // this.$message.success('成功')
                    if (this.course.select) {
                        let self = this
                        this.$confirm('确认删除？', {
                            callback() {
                                // self.$router.push("/cart")
                                self.$emit("del")
                            }

                        })
                    } else {
                        this.$message.error('请先选中')
                    }

                    // this.$emit("del")
                    console.log(re.data)
                }).catch(error => {
                    this.$message.error('删除失败')
                })
            }
        },
        created() {
            // console.log(course.id)
            // console.log(this.course.id)
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

</style>
