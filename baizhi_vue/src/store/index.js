import Vue from 'vue'
import Vuex from 'vuex'
Vue.use(Vuex)

export default new Vuex.Store({
    state:{
        cart_length:''
        // expire_price:0
    },
    mutations:{
        add_goods(state,data){
            this.state.cart_length = data
        },
        expire_price(state,data){
            this.state.expire_price = data
        }
    }
})

