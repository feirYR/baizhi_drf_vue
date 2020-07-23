import Vue from 'vue'
import Router from 'vue-router'
import home from "../components/home";
import header from "../components/common/headers";
import banner from "../components/common/banner";
import login from "../components/login";
import register from "../components/register";
import Course from "../components/Course";
import CourseDetail from "../components/CourseDetail";
import cart from "../components/cart";
import order from "../components/order";
import OrderSuccess from "../components/OrderSuccess";


Vue.use(Router)

export default new Router({
    mode:'history',
    routes: [
        {
            path: '/',
            name: 'home',
            component: home
        },
        {
            path: '/home',
            name: 'home',
            component: home
        },
        {
            path: '/login',
            name: 'login',
            component: login
        },
        {
            path: '/register',
            name: 'register',
            component: register
        },
        {
            path: '/course',
            name: 'course',
            component: Course
        },
        {
            path: '/course/detail/:id',
            name: 'CourseDetail',
            component: CourseDetail
        },
        {
            path: '/cart',
            name: 'cart',
            component: cart
        },
        {
            path: '/order',
            name: 'order',
            component: order
        },
        {
            path: '/payments/result',
            name: 'result',
            component: OrderSuccess
        },

    ]
})
