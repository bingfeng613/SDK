<template>
    <el-menu default-active="1-4-1" class="el-menu-vertical-demo" @open="handleOpen" @close="handleClose"
        :collapse="isCollapse" background-color="#ffffff" text-color="#333333" active-text-color="#409EFF">
        <div class="user">
            <img src="../Views/images/avatar.png" alt="">
            <div class="userInfo">
                <p class="name">{{ userName }}</p>
                <!-- <p class="access">auditorA</p> -->
                <a href="#" class="change-password" @click="openChangePasswordDialog">修改密码</a>
                <a class="spacer"></a>
                <a href="#" class="logout" @click="logout">退出</a>
            </div>
        </div>

        <el-menu-item @click="clickItem(item)" v-for="item in noChildren" :key="item.name" :index="item.name">
            <i :class="`el-icon-${item.icon}`"></i>
            <span slot="title">{{ item.label }}</span>
        </el-menu-item>
        <!-- <el-submenu v-for="item in hasChildren" :key="item.label" :index="item.label">
            <template slot="title">
                <i :class="`el-icon-${item.icon}`"></i>
                <span slot="title">{{ item.label }}</span>
            </template>
            <el-menu-item-group v-for="subItem in item.children" :key="subItem.name">
                <el-menu-item @click="clickItem(subItem)" :index="subItem.name">{{ subItem.label }}</el-menu-item>
            </el-menu-item-group>
        </el-submenu> -->

        <!-- Change Password Dialog -->
        <el-dialog title="修改密码" :visible.sync="changePasswordDialogVisible">
            <el-form ref="changePasswordForm" :model="changePasswordForm" :rules="changePasswordRules"
                label-width="80px">
                <el-form-item label="当前密码" prop="oldPassword">
                    <el-input type="password" v-model="changePasswordForm.oldPassword"></el-input>
                </el-form-item>
                <el-form-item label="新密码" prop="newPassword">
                    <el-input type="password" v-model="changePasswordForm.newPassword"></el-input>
                </el-form-item>
                <el-form-item label="确认新密码" prop="confirmNewPassword">
                    <el-input type="password" v-model="changePasswordForm.confirmNewPassword"></el-input>
                </el-form-item>
                <el-form-item>
                    <el-button type="primary" @click="submitChangePassword">确定</el-button>
                    <el-button @click="changePasswordDialogVisible = false">取消</el-button>
                </el-form-item>
            </el-form>
        </el-dialog>
    </el-menu>
</template>

<style lang="less" scoped>
.el-menu-vertical-demo {
    width: 200px;
    min-height: 100vh;
    // border-right: 2px solid #ccc;
}

.user {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 20px 0;
    border-bottom: 2px solid #ccc;
    background-color: #f5f5f5;

    img {
        width: 80px;
        height: 80px;
        border-radius: 50%;
        margin-bottom: 10px;
    }

    .userInfo {
        text-align: center;

        .name {
            font-size: 18px;
            margin-bottom: 10px;
        }

        .access {
            color: #999;
            margin-bottom: 10px;
        }

        .change-password,
        .logout {
            color: #409EFF;
            font-size: 14px;
            text-decoration: none;
            cursor: pointer;
            margin-top: 10px;
        }

        .spacer {
            margin-left: 10px; 
            margin-right: 10px; 
        }
    }
}

.el-menu {
    border-right: 2px solid #ccc; 
    min-height: 120vh;
}

</style>

<script>
import cookie from 'js-cookie'
import axios from 'axios'

export default {
    data() {
        return {
            user: this.$store.state.user.account,
            changePasswordDialogVisible: false,
            changePasswordForm: {
                oldPassword: '',
                newPassword: '',
                confirmNewPassword: ''
            },
            changePasswordRules: {
                oldPassword: [{ required: true, message: '请输入当前密码', trigger: 'blur' }],
                newPassword: [{ required: true, message: '请输入新密码', trigger: 'blur' }],
                confirmNewPassword: [{ required: true, message: '请确认新密码', trigger: 'blur' }]
            }
        };
    },
    methods: {
        handleOpen(key, keyPath) {
            console.log(key, keyPath);
        },
        handleClose(key, keyPath) {
            console.log(key, keyPath);
        },
        clickItem(item) {
            if (item.name === 'user') {
                if (!this.$store.state.stats.statistics || Object.keys(this.$store.state.stats.statistics).length === 0) {
                    this.$message.warning('未通过已解析库生成统计数据');
                    return;
                }
            }
            
            if (item.name === 'test') {
                this.$router.push({ 
                    path: 'http://www.baidu.com', 
                    query: { redirect: item.name } 
                });
            }

            if (this.$route.path !== item.path && !(this.$route.path === '/home' && item.path === '/')) {
                this.$router.push(item.path);
            }
            this.$store.commit('SelectMenu', item);
        },
        logout() {
            this.$store.commit('setMenu', []);  // 清除菜单
            this.$store.commit('setAccount', '');  // 清除账户信息
            cookie.remove('token');
            this.$router.push('/login');
        },
        openChangePasswordDialog() {
            this.changePasswordDialogVisible = true;
        },
        // 修改密码
        submitChangePassword() {
            this.$refs.changePasswordForm.validate((valid) => {
                if (valid) {
                    if (this.changePasswordForm.newPassword !== this.changePasswordForm.confirmNewPassword) {
                        this.$message.error('两次输入的新密码不一致');
                        return;
                    }
                    axios.post('http://127.0.0.1:8000/change-password/', {
                        account: this.user,
                        old_password: this.changePasswordForm.oldPassword,
                        new_password: this.changePasswordForm.newPassword
                    }).then(response => {
                        console.log(response)
                        // console.log(response.data.message);
                        if (response.status === 200) {
                            this.$message.success('密码修改成功');
                            this.logout();
                        } else {
                            this.$message.error(response.data.message);
                        }
                    }).catch(error => {
                        this.$message.error('密码修改失败，请重试',error);
                    });
                }
            });
        }
    },
    computed: {
        noChildren() {
            return this.MenuData.filter(item => !item.children);
        },
        hasChildren() {
            return this.MenuData.filter(item => item.children);
        },
        isCollapse() {
            return this.$store.state.tab.isCollapse;
        },
        MenuData() {
            return JSON.parse(cookie.get('menu')) || this.$store.state.tab.menu;
        },
        userName() {
            console.log(this.$store.state.user.account)
            return this.$store.state.user.account;
        }
    }
}
</script>
