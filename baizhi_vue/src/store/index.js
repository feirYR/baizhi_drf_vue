import Vue from 'vue'
import Vuex from 'vuex'
Vue.use(Vuex)

export default new Vuex.Store({
    state:{
        cart_length:0,
    },
    mutations:{
        add_goods(state,data){
            this.state.cart_length = data
        }
    }
})
