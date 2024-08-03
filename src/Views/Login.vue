<template>
    <div class="login_page">
        <div class="background_overlay"></div>
        <div class="content">
            <div class="text_section">
                <h1>P-Sticker: SDK隐私声明合规检测平台</h1>
                <p>一键生成SDK不合规数据声明报告, 上传隐私政策, 找出缺失/模糊声明及无效链接</p>
            </div>
            <div class="login_container">
                <h3 class="login_title">登录</h3>
                <el-form ref="form" :model="login" status-icon :rules="rules" label-width="0px">
                    <el-form-item prop="username">
                        <el-input v-model="login.username" placeholder="请输入您的账号" prefix-icon="el-icon-user"></el-input>
                    </el-form-item>
                    <el-form-item prop="password">
                        <el-input type="password" v-model="login.password" placeholder="请输入您的密码"
                            prefix-icon="el-icon-lock"></el-input>
                    </el-form-item>
                    <el-form-item>
                        <el-button @click="submit" type="primary" class="login_button">登录</el-button>
                    </el-form-item>
                </el-form>
                <div class="register_link">
                    <a href="#">注册</a>
                    <a href="#">忘记密码?</a>
                </div>
            </div>
            <div class="footer">
                © 2024 Zhong Zhu Shi Gong Dui. All rights reserved.
            </div>
        </div>
    </div>
</template>

<script>
import Cookie from 'js-cookie'
import { getMenu } from '../api/index'
export default {
    data() {
        return {
            // 登陆数据
            login: {
                account: '',
                password: ''
            },
            // 校验规则
            rules: {
                account: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
                password: [{ required: true, message: '请输入密码', trigger: 'blur' }]
            }
        }
    },
    methods: {
        submit() {
            // 表单的校验
            this.$refs.form.validate((valid) => {
                if (valid) {
                    // 传入表单数据
                    getMenu(this.login).then((data) => {
                        // console.log(data);
                        if (data.data.code === 20000) {
                            // 记录cookie
                            Cookie.set('token', data.data.data.token)
                            // 设置菜单
                            this.$store.commit('setMenu', data.data.data.menu)
                            // 动态添加路由
                            this.$store.commit('addMenu', this.$router)
                            // 跳转到首页
                            this.$router.push('/home')
                        } else {
                            // 验证失败的弹窗
                            this.$message.error(data.data.data.message);
                        }
                    })
                }
            })
        }
    }
}
</script>

<style lang="less" scoped>
.login_page {
    display: flex;
    justify-content: flex-end;
    align-items: center;
    height: 100vh;
    background: url('images/signinbackground.jpg') no-repeat center center;
    background-size: cover;
    position: relative;
}

.content {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    align-items: flex-end;
    position: relative;
    z-index: 1;
    width: 100%;
    height: 100%;
    padding: 50px;
    box-sizing: border-box;
}

.text_section {
    text-align: left;
    color: #333;

    h1 {
        font-size: 24px;
        margin-bottom: 10px;
    }

    p {
        font-size: 14px;
        margin-bottom: 20px;
    }
}

.login_container {
    width: 350px;
    padding: 30px;
    background: #fff;
    border-radius: 8px;
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
    margin-bottom: 20px;

    .login_title {
        font-size: 24px;
        font-weight: 500;
        text-align: center;
        margin-bottom: 30px;
        color: #333;
    }

    .el-form-item {
        margin-bottom: 20px;
    }

    .login_button {
        width: 100%;
        height: 40px;
    }

    .register_link {
        display: flex;
        justify-content: space-between;
        margin-top: 10px;

        a {
            color: #409EFF;
            text-decoration: none;
        }
    }
}

.footer {
    text-align: left;
    color: #333;
    font-size: 12px;
}
</style>