<template>
    <div class="course">
        <headers></headers>
        <div class="main">
            <!-- 筛选条件 -->
            <div class="condition">
                <ul class="cate-list">
                    <li class="title">课程分类:</li>
                    <li @click="cate_style=0" :class="cate_style==0?'this':''">全部</li>
                    <li v-for="cate in cates" @click="cate_style=cate.id" :class="cate_style==cate.id?'this':''">
                        {{cate.name}}
                    </li>

                </ul>

                <div class="ordering">
                    <ul>
                        <li class="title">筛&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;选:</li>
                        <li class="default" @click="order_type('id')" :class="order_class('id')">默认</li>
                        <li class="hot" @click="order_type('students')" :class="order_class('students')">人气</li>
                        <li class="price" @click="order_type('price')" :class="order_class('price')">价格</li>
                    </ul>
                    <p class="condition-result">共21个课程</p>
                </div>

            </div>
            <!-- 课程列表 -->
            <div class="course-list">
                <div class="course-item" v-for="course in courses">
                    <div class="course-image">
                        <img :src="course.course_img" alt="">
                    </div>
                    <div class="course-info">
                        <h3>
<!--                            <router-link to="course/detail">{{course.name}}</router-link>-->
                            <router-link :to="'course/detail/'+course.id">{{course.name}}</router-link>
                            <span><img src="/static/image/avatar1.svg" alt="">{{course.students}}人已加入学习</span>
                        </h3>
                        <p class="teather-info">huxz 百知教育教学总监
                            <span v-if="course.lessons === course.pub_lessons">共{{course.lessons}}课时/更新完成</span>
                            <span v-else>共{{course.lessons}}课时/更新{{course.pub_lessons}}课时</span>
                        </p>
                        <ul class="lesson-list">
                            <li v-for="(lesson,index) in course.lesson_list" :key="index">
                                <span class="lesson-title">0{{index+1}} | 第{{index+1}}节：{{lesson.name}}</span>
                                <span class="free" v-if="lesson.free_trail">免费</span>
                            </li>
                        </ul>
                        <div class="pay-box">
                            <span class="discount-type" v-if="course.discount_name">{{course.discount_name}}</span>
                            <span class="discount-price" >￥{{course.final_price}}元</span>
                            <span class="original-price" v-if="course.discount_name">原价：{{course.price}}元</span>
                            <span class="buy-now">立即购买</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <el-switch v-model="value">
        </el-switch>
        <el-pagination
            :hide-on-single-page="value"
            :total="total"
            :page-size='filters.size'
            :page-sizes=[2,3,5]
            @current-change="page_change"
            @size-change="size_change"
            layout="prev, pager, next,sizes">
        </el-pagination>
        <foot></foot>
    </div>
</template>

<script>
    import headers from "./common/headers";
    import foot from "./common/foot";

    export default {
        name: "Course",
        components: {
            headers: headers,
            foot: foot,
        },
        data() {
            return {
                cates: [],
                courses: [],
                cate_style: 0,
                value:false,
                total:0,
                filters: {
                    type: 'id',
                    order: 'desc',
                    page: 1,
                    size: 2
                }
            }
        },
        watch: {
            cate_style() {
                this.get_courses()
            }
        },
        methods: {
            get_categories() {
                this.$axios({
                    url: this.$settings.HOST + 'course/categories/',
                    method: 'get'
                }).then(re => {
                    // console.log('查询所有分类成功')
                    this.cates = re.data
                }).catch(error => {
                    // console.log('查询所有分类失败')
                })
            },
            get_courses() {
                let filters = {
                    // course_category:'',
                    // ordering:'',
                    page:this.filters.page,
                    size:this.filters.size

                }

                if (this.cate_style > 0) {
                    filters.course_category = this.cate_style
                }

                if (this.filters.order === 'desc') {
                    filters.ordering = '-' + this.filters.type
                } else {
                    filters.ordering = this.filters.type
                }
                // console.log(this.cate_style);
                this.$axios({
                    url: this.$settings.HOST + 'course/courses_filter/',
                    method: 'get',
                    params: filters
                }).then(re => {
                    // console.log('查询所有课程成功')
                    // console.log(re.data.results)
                    // this.courses = re.data
                    this.courses = re.data.results
                    this.total = re.data.count
                    // this.$store.commit('add_goods',re.data.cart_length)
                }).catch(error => {
                    // console.log('查询所有课程失败')
                })
            },
            order_type(type) {
                if (this.filters.type === type && this.filters.order === 'desc') {
                    this.filters.order = 'asc'
                } else if (this.filters.type === type && this.filters.order === 'asc') {
                    this.filters.order = 'desc'
                }
                this.filters.type = type
                this.get_courses()

            },
            order_class(type) {
                if (this.filters.type === type && this.filters.order === 'desc') {
                    return 'this desc'
                } else if (this.filters.type === type && this.filters.order === 'asc') {
                    return 'this asc'
                }

            },
            page_change(page){
                this.filters.page = page
                this.get_courses()
            },
            size_change(size){
                this.filters.size = size
                this.filters.page = 1
                this.get_courses()
            }
        },
        created() {
            this.get_categories()
            this.get_courses()
        }
    }
</script>

<style scoped>
    .course {
        background: #f6f6f6;
    }

    .course .main {
        width: 1100px;
        margin: 35px auto 0;
    }

    .course .condition {
        margin-bottom: 35px;
        padding: 25px 30px 25px 20px;
        background: #fff;
        border-radius: 4px;
        box-shadow: 0 2px 4px 0 #f0f0f0;
    }

    .course .cate-list {
        border-bottom: 1px solid #333;
        border-bottom-color: rgba(51, 51, 51, .05);
        padding-bottom: 18px;
        margin-bottom: 17px;
    }

    .course .cate-list::after {
        content: "";
        display: block;
        clear: both;
    }

    .course .cate-list li {
        float: left;
        font-size: 16px;
        padding: 6px 15px;
        line-height: 16px;
        margin-left: 14px;
        position: relative;
        transition: all .3s ease;
        cursor: pointer;
        color: #4a4a4a;
        border: 1px solid transparent; /* transparent 透明 */
    }

    .course .cate-list .title {
        color: #888;
        margin-left: 0;
        letter-spacing: .36px;
        padding: 0;
        line-height: 28px;
    }

    .course .cate-list .this {
        color: #ffc210;
        border: 1px solid #ffc210 !important;
        border-radius: 30px;
    }

    .course .ordering::after {
        content: "";
        display: block;
        clear: both;
    }

    .course .ordering ul {
        float: left;
    }

    .course .ordering ul::after {
        content: "";
        display: block;
        clear: both;
    }

    .course .ordering .condition-result {
        float: right;
        font-size: 14px;
        color: #9b9b9b;
        line-height: 28px;
    }

    .course .ordering ul li {
        float: left;
        padding: 6px 15px;
        line-height: 16px;
        margin-left: 14px;
        position: relative;
        transition: all .3s ease;
        cursor: pointer;
        color: #4a4a4a;
    }

    .course .ordering .title {
        font-size: 16px;
        color: #888;
        letter-spacing: .36px;
        margin-left: 0;
        padding: 0;
        line-height: 28px;
    }

    .course .ordering .this {
        color: #ffc210;
    }

    .course .ordering .price {
        position: relative;
    }

    .course .ordering .price::before,
    .course .ordering .price::after {
        cursor: pointer;
        content: "";
        display: block;
        width: 0px;
        height: 0px;
        border: 5px solid transparent;
        position: absolute;
        right: 0;
    }

    .course .ordering .price::before {
        border-bottom: 5px solid #aaa;
        margin-bottom: 2px;
        top: 2px;
    }

    .course .ordering .price::after {
        border-top: 5px solid #aaa;
        bottom: 2px;
    }

    .course .course-item:hover {
        box-shadow: 4px 6px 16px rgba(0, 0, 0, .5);
    }

    .course .course-item {
        width: 1050px;
        background: #fff;
        padding: 20px 30px 20px 20px;
        margin-bottom: 35px;
        border-radius: 2px;
        cursor: pointer;
        box-shadow: 2px 3px 16px rgba(0, 0, 0, .1);
        /* css3.0 过渡动画 hover 事件操作 */
        transition: all .2s ease;
    }

    .course .course-item::after {
        content: "";
        display: block;
        clear: both;
    }

    /* 顶级元素 父级元素  当前元素{} */
    .course .course-item .course-image {
        float: left;
        width: 423px;
        height: 210px;
        margin-right: 30px;
    }

    .course .course-item .course-image img {
        width: 100%;
    }

    .course .course-item .course-info {
        float: left;
        width: 596px;
    }

    .course-item .course-info h3 {
        font-size: 26px;
        color: #333;
        font-weight: normal;
        margin-bottom: 8px;
    }

    .course-item .course-info h3 span {
        font-size: 14px;
        color: #9b9b9b;
        float: right;
        margin-top: 14px;
    }

    .course-item .course-info h3 span img {
        width: 11px;
        height: auto;
        margin-right: 7px;
    }

    .course-item .course-info .teather-info {
        font-size: 14px;
        color: #9b9b9b;
        margin-bottom: 14px;
        padding-bottom: 14px;
        border-bottom: 1px solid #333;
        border-bottom-color: rgba(51, 51, 51, .05);
    }

    .course-item .course-info .teather-info span {
        float: right;
    }

    .course-item .lesson-list::after {
        content: "";
        display: block;
        clear: both;
    }

    .course-item .lesson-list li {
        float: left;
        width: 44%;
        font-size: 14px;
        color: #666;
        padding-left: 22px;
        /* background: url("路径") 是否平铺 x轴位置 y轴位置 */
        background: url("/static/image/play-icon-gray.svg") no-repeat left 4px;
        margin-bottom: 15px;
    }

    .course-item .lesson-list li .lesson-title {
        /* 以下3句，文本内容过多，会自动隐藏，并显示省略符号 */
        text-overflow: ellipsis;
        overflow: hidden;
        white-space: nowrap;
        display: inline-block;
        max-width: 200px;
    }

    .course-item .lesson-list li:hover {
        background-image: url("/static/image/play-icon-yellow.svg");
        color: #ffc210;
    }

    .course-item .lesson-list li .free {
        width: 34px;
        height: 20px;
        color: #fd7b4d;
        vertical-align: super;
        margin-left: 10px;
        border: 1px solid #fd7b4d;
        border-radius: 2px;
        text-align: center;
        font-size: 13px;
        white-space: nowrap;
    }

    .course-item .lesson-list li:hover .free {
        color: #ffc210;
        border-color: #ffc210;
    }

    .course-item .pay-box::after {
        content: "";
        display: block;
        clear: both;
    }

    .course-item .pay-box .discount-type {
        padding: 6px 10px;
        font-size: 16px;
        color: #fff;
        text-align: center;
        margin-right: 8px;
        background: #fa6240;
        border: 1px solid #fa6240;
        border-radius: 10px 0 10px 0;
        float: left;
    }

    .course-item .pay-box .discount-price {
        font-size: 24px;
        color: #fa6240;
        float: left;
    }

    .course-item .pay-box .original-price {
        text-decoration: line-through;
        font-size: 14px;
        color: #9b9b9b;
        margin-left: 10px;
        float: left;
        margin-top: 10px;
    }

    .course-item .pay-box .buy-now {
        width: 120px;
        height: 38px;
        background: transparent;
        color: #fa6240;
        font-size: 16px;
        border: 1px solid #fd7b4d;
        border-radius: 3px;
        transition: all .2s ease-in-out;
        float: right;
        text-align: center;
        line-height: 38px;
    }

    .course-item .pay-box .buy-now:hover {
        color: #fff;
        background: #ffc210;
        border: 1px solid #ffc210;
    }

    .el-pagination {
        text-align: center;
        padding-top: 20px;
        padding-bottom: 50px;
    }
</style>
