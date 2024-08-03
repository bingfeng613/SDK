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
                    <el-form-item prop="account">
                        <el-input v-model="login.account" placeholder="请输入您的账号" prefix-icon="el-icon-user"></el-input>
                    </el-form-item>
                    <el-form-item prop="password">
                        <el-input type="password" v-model="login.password" placeholder="请输入您的密码"
                            prefix-icon="el-icon-lock"></el-input>
                    </el-form-item>
                    <el-form-item>
                        <el-button @click="submitLogin" type="primary" class="login_button">登录</el-button>
                    </el-form-item>
                </el-form>
                <div class="register_link">
                    <a @click="openRegisterDialog">注册</a>
                </div>
            </div>
            <div class="footer">
                © 2024 Zhong Zhu Shi Gong Dui. All rights reserved.
            </div>
        </div>

        <el-dialog title="注册" :visible.sync="registerDialogVisible">
            <el-form ref="registerForm" :model="register" :rules="registerRules" label-width="80px">
                <el-form-item label="账号" prop="account">
                    <el-input v-model="register.account"></el-input>
                </el-form-item>
                <el-form-item label="密码" prop="password">
                    <el-input type="password" v-model="register.password"></el-input>
                </el-form-item>
                <el-form-item label="确认密码" prop="confirmPassword">
                    <el-input type="password" v-model="register.confirmPassword"></el-input>
                </el-form-item>
                <el-form-item>
                    <el-button type="primary" @click="submitRegister">确定</el-button>
                    <el-button @click="registerDialogVisible = false">取消</el-button>
                </el-form-item>
            </el-form>
        </el-dialog>
    </div>
</template>

<script>
import Cookie from 'js-cookie'
import { login, register } from '../api/index'


export default {
    data() {
        return {
            login: {
                account: '',
                password: ''
            },
            register: {
                account: '',
                password: '',
                confirmPassword: ''
            },
            rules: {
                account: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
                password: [{ required: true, message: '请输入密码', trigger: 'blur' }]
            },
            registerRules: {
                account: [{ required: true, message: '请输入账号', trigger: 'blur' }],
                password: [{ required: true, message: '请输入密码', trigger: 'blur' }],
                confirmPassword: [{ required: true, message: '请确认密码', trigger: 'blur' }]
            },
            registerDialogVisible: false
        }
    },
    methods: {
        submitLogin() {
            this.$refs.form.validate((valid) => {
                if (valid) {
                    login(this.login).then(response => {
                        const data = response;
                        console.log(data)
                        if (data.status === 200) {
                            Cookie.set('token', data.data.account)
                            this.$message.success('登录成功');
                            this.setMenu(data.data.account)
                            this.$store.commit('setAccount', data.data.account); // 保存账号信息到 Vuex
                            this.$router.push('/home')
                        } else {
                            this.$message.error('登录失败，请重试');
                        }
                    }).catch(error => {
                        this.$message.error('登录失败，请重试',error);
                    })
                }
            })
        },
        setMenu(account) {
            let menu;
            console.log("setMenu:",account)
            if (account) {
                menu = [
                    {
                        path: '/home',
                        name: 'home',
                        label: '上传解析',
                        icon: 's-home',
                        url: 'Home.vue'
                    },
                    {
                        path: '/mall',
                        name: 'mall',
                        label: '已解析库',
                        icon: 'video-play',
                        url: 'Mall.vue'
                    },
                    {
                        path: '/user',
                        name: 'user',
                        label: '统计数据',
                        icon: 'user',
                        url: 'User.vue'
                    },
                ];
            } else {
                menu = [
                    // {
                    //     path: '/home',
                    //     name: 'home',
                    //     label: '首页',
                    //     icon: 's-home',
                    //     url: 'Home.vue'
                    // },
                    // {
                    //     path: '/video',
                    //     name: 'video',
                    //     label: '商品管理',
                    //     icon: 'video-play',
                    //     url: 'Mall.vue'
                    // }
                ];
            }
            this.$store.commit('setMenu', menu)
            this.$store.commit('addMenu', this.$router)
            console.log("menu:",menu)
            console.log("this.$router:",this.$router)
        },
        openRegisterDialog() {
            this.registerDialogVisible = true;
        },
        submitRegister() {
            this.$refs.registerForm.validate((valid) => {
                if (valid) {
                    if (this.register.password !== this.register.confirmPassword) {
                        this.$message.error('两次输入的密码不一致');
                        return;
                    }
                    register(this.register).then(response => {
                        const data = response.data;
                        if (response.status === 201) {
                            this.$message.success('注册成功，请登录');
                            this.registerDialogVisible = false;
                        } else {
                            this.$message.error(data.message);
                        }
                    }).catch(error => {
                        this.$message.error('注册失败，请重试', error);
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