<template>
    <el-container>
        <el-aside width="auto">
            <common-aside />
        </el-aside>
        <el-container>
            <!-- <el-header>
                <common-header />
            </el-header> -->
            <!-- <common-tags /> -->
            <el-main>
                <router-view></router-view>
            </el-main>
        </el-container>
    </el-container>
</template>

<script>
import CommonAside from '../components/CommonAside.vue'
import CommonHeader from '../components/CommonHeader.vue'
import CommonTags from '../components/CommonTags.vue'

export default {
    components: {
        CommonAside,
        CommonHeader,
        CommonTags
    }
}
</script>

<style lang="less" scoped>
.el-header {
    padding: 0;
}
</style>
