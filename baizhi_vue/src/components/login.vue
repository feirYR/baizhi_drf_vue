<template>
    <div class="login box">
        <img src="../../static/image/1111.jpg" alt="">
        <div class="login">
            <div class="login-title">
                <img src="../../static/image/logo.png" alt="">
                <p>百知教育给你最优质的学习体验!</p>
            </div>
            <div class="login_box">
                <div class="title">
                    <span>密码登录</span>
                    <span>短信登录</span>
                </div>
                <div class="inp" v-if="">
                    <input type="text" placeholder="用户名 / 手机号码" class="user" v-model="username">
                    <input type="password" name="" class="pwd" placeholder="密码" v-model="password">
                    <div id="popup-captcha"></div>
                    <div class="rember">
                        <p>
                            <input type="checkbox" class="no" v-model="remeber_me"/>
                            <span>记住密码</span>
                        </p>
                        <p>忘记密码</p>
                    </div>
                    <button class="login_btn btn btn-primary" @click="get_captche">登录</button>
                    <p class="go_login">没有账号
                        <router-link to="/register">立即注册</router-link>
                    </p>
                </div>
                <div class="inp" v-show="">
                    <input type="text" placeholder="手机号码" class="user">
                    <input type="text" class="pwd" placeholder="短信验证码">
                    <button id="get_code" class="btn btn-primary">获取验证码</button>
                    <button class="login_btn">登录</button>
                    <span class="go_login">没有账号
                    <router-link to="/register">立即注册</router-link>
                </span>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    export default {
        name: "login",
        data() {
            return {
                username: '',
                password: '',
                remeber_me: false
            }
        },
        methods: {
            get_captche() {
                this.$axios({
                    url: 'http://127.0.0.1:8000/user/captche/',
                    method: 'get',
                    params: {
                        username: this.username
                    },
                }).then(re => {
                    console.log(re.data)
                    let data = JSON.parse(re.data.results)
                    console.log(data)
                    initGeetest({
                        gt: data.gt,
                        challenge: data.challenge,
                        product: "popup", // 产品形式，包括：float，embed，popup。注意只对PC版验证码有效
                        offline: !data.success, // 表示用户后台检测极验服务器是否宕机，一般不需要关注
                        new_captcha: data.new_captcha
                    }, this.handlerPopup);
                }).catch(error => {
                    console.log(2222222)
                    this.$message.error('用户名或密码错误')
                })

            },
            handlerPopup(captchaObj) {
                let self = this;
                captchaObj.onSuccess(function () {
                    let validate = captchaObj.getValidate()
                    self.$axios({
                        url: 'http://127.0.0.1:8000/user/captche/',
                        method: 'post',
                        data: {
                            username:self.username,
                            geetest_challenge: validate.geetest_challenge,
                            geetest_validate: validate.geetest_validate,
                            geetest_seccode: validate.geetest_seccode
                        }
                    }).then(re=>{
                        console.log(re.data);
                        if (re.data.status){
                            console.log('验证成功')
                            console.log(re.data.status)
                            self.login()
                            // self.$router.push('/')
                        }else {
                            self.$message.error('验证失败')
                        }

                    }).catch(error=>{
                        console.log(error)
                    })
                })
                document.getElementById("popup-captcha").innerHTML = "";
                captchaObj.appendTo("#popup-captcha");
            },
            login() {
                this.$axios({
                    url: 'http://127.0.0.1:8000/user/login/',
                    method: 'post',
                    data: {
                        username: this.username,
                        password: this.password
                    }
                }).then(re => {
                    console.log(re.data['username'], re.data['token']);
                    this.$message({
                        message: '恭喜你，登陆成功',
                        type: 'success'
                    });
                    if (this.remeber_me) {
                        localStorage.username = this.username
                        localStorage.token = re.data['token']
                        localStorage.user_id = re.data['user_id']
                        sessionStorage.removeItem('username')
                        sessionStorage.removeItem('token')
                        sessionStorage.removeItem('user_id')
                    } else {
                        sessionStorage.username = this.username
                        sessionStorage.token = re.data['token']
                        sessionStorage.user_id = re.data['user_id']
                        localStorage.removeItem('username')
                        localStorage.removeItem('token')
                        localStorage.removeItem('user_id')
                    }

                    this.$router.push('/home')
                }).catch(error => {
                    console.log(11111111)
                    this.$message.error('用户名或密码错误')

                })
            }
        }
    }
</script>

<style scoped>
    .box {
        width: 100%;
        height: 100%;
        position: relative;
        overflow: hidden;
    }

    .box img {
        width: 100%;
        min-height: 100%;
    }

    .box .login {
        position: absolute;
        width: 500px;
        height: 400px;
        top: 0;
        left: 0;
        margin: auto;
        right: 0;
        bottom: 0;
        top: -338px;
    }

    .login .login-title {
        width: 100%;
        text-align: center;
    }

    .login-title img {
        width: 190px;
        height: auto;
    }

    .login-title p {
        font-family: PingFangSC-Regular;
        font-size: 18px;
        color: #fff;
        letter-spacing: .29px;
        padding-top: 10px;
        padding-bottom: 50px;
    }

    .login_box {
        width: 400px;
        height: auto;
        background: #fff;
        box-shadow: 0 2px 4px 0 rgba(0, 0, 0, .5);
        border-radius: 4px;
        margin: 0 auto;
        padding-bottom: 40px;
    }

    .login_box .title {
        font-size: 20px;
        color: #9b9b9b;
        letter-spacing: .32px;
        border-bottom: 1px solid #e6e6e6;
        display: flex;
        justify-content: space-around;
        padding: 50px 60px 0 60px;
        margin-bottom: 20px;
        cursor: pointer;
    }

    .login_box .title span:nth-of-type(1) {
        color: #4a4a4a;
        border-bottom: 2px solid #84cc39;
    }

    .inp {
        width: 350px;
        margin: 0 auto;
    }

    .inp input {
        border: 0;
        outline: 0;
        width: 100%;
        height: 45px;
        border-radius: 4px;
        border: 1px solid #d9d9d9;
        text-indent: 20px;
        font-size: 14px;
        background: #fff !important;
    }

    .inp input.user {
        margin-bottom: 16px;
    }

    .inp .rember {
        display: flex;
        justify-content: space-between;
        align-items: center;
        position: relative;
        margin-top: 10px;
    }

    .inp .rember p:first-of-type {
        font-size: 12px;
        color: #4a4a4a;
        letter-spacing: .19px;
        margin-left: 22px;
        display: -ms-flexbox;
        display: flex;
        -ms-flex-align: center;
        align-items: center;
        /*position: relative;*/
    }

    .inp .rember p:nth-of-type(2) {
        font-size: 14px;
        color: #9b9b9b;
        letter-spacing: .19px;
        cursor: pointer;
    }

    .inp .rember input {
        outline: 0;
        width: 30px;
        height: 45px;
        border-radius: 4px;
        border: 1px solid #d9d9d9;
        text-indent: 20px;
        font-size: 14px;
        background: #fff !important;
    }

    .inp .rember p span {
        display: inline-block;
        font-size: 12px;
        width: 100px;
        /*position: absolute;*/
        /*left: 20px;*/

    }

    #geetest {
        margin-top: 20px;
    }

    .login_btn {
        width: 100%;
        height: 45px;
        background: #84cc39;
        border-radius: 5px;
        font-size: 16px;
        color: #fff;
        letter-spacing: .26px;
        margin-top: 30px;
    }

    .inp .go_login {
        text-align: center;
        font-size: 14px;
        color: #9b9b9b;
        letter-spacing: .26px;
        padding-top: 20px;
    }

    .inp .go_login span {
        color: #84cc39;
        cursor: pointer;
    }
</style>
