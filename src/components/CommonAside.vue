<template>
    <el-menu default-active="1-4-1" class="el-menu-vertical-demo" @open="handleOpen" @close="handleClose"
        :collapse="isCollapse" background-color="#ffffff" text-color="#333333" active-text-color="#409EFF">
        <div class="user">
            <img src="../Views/images/avatar.png" alt="">
            <div class="userInfo">
                <p class="name">审计员A</p>
                <p class="access">auditorA</p>
                <a href="#" class="change-password">修改密码</a>
            </div>
        </div>
        <el-menu-item @click="clickItem(item)" v-for="item in  noChildren " :key="item.name" :index="item.name">
            <i :class="`el-icon-${item.icon}`"></i>
            <span slot="title">{{ item.label }}</span>
        </el-menu-item>
        <el-submenu v-for=" item  in  hasChildren " :key=" item.label " :index=" item.label ">
            <template slot="title">
                <i :class="`el-icon-${item.icon}`"></i>
                <span slot="title">{{ item.label }}</span>
            </template>
            <el-menu-item-group v-for=" subItem  in  item.children " :key=" subItem.name ">
                <el-menu-item @click="clickItem(subItem)" :index=" subItem.name ">{{ subItem.label }}</el-menu-item>
            </el-menu-item-group>
        </el-submenu>
    </el-menu>
</template>

<style lang="less" scoped>
.el-menu-vertical-demo {
    width: 200px;
    min-height: 100vh;
    border-right: none;
}

.user {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 20px 0;
    border-bottom: 1px solid #ccc;
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
            margin-bottom: 5px;
        }

        .access {
            color: #999;
            margin-bottom: 10px;
        }

        .change-password {
            color: #409EFF;
            font-size: 14px;
            text-decoration: none;
        }
    }
}
</style>

<script>
import cookie from 'js-cookie'
export default {
    data() {
        return {};
    },
    methods: {
        handleOpen(key, keyPath) {
            console.log(key, keyPath);
        },
        handleClose(key, keyPath) {
            console.log(key, keyPath);
        },
        clickItem(item) {
            // 判断是否是"统计数据"菜单项
            // console.log(item.name)
            // 注意需要设置为组件的名字
            if (item.name === 'user') {
                // 检查 Vuex 中的数据是否存在
                if (!this.$store.state.stats.statistics || Object.keys(this.$store.state.stats.statistics).length === 0) {
                    this.$message.warning('未通过已解析库生成统计数据');
                    return; // 阻止跳转
                }
            }

            if (this.$route.path !== item.path && !(this.$route.path === '/home' && (item.path === '/'))) {
                this.$router.push(item.path);
            }
            this.$store.commit('SelectMenu', item);
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
        }
    }
}
</script>
