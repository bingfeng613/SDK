<template>
    <div class="tabs">
        <el-tag v-for="(item, index) in tags" :key="item.path" :closable="item.name !== 'home'"
            :effect="item.name === $route.name ? 'dark' : 'plain'" @click="changeMenu(item)"
            @close="handleClose(item, index)">
            {{ item.label }}
        </el-tag>
    </div>
</template>

<script>
import { mapState } from 'vuex'

export default {
    methods: {
        changeMenu(item) {
            this.$router.push({ name: item.name });
        },
        handleClose(item, index) {
            this.$store.commit('closeTag', item);
            if (item.name === this.$route.name) {
                const length = this.tags.length;
                if (length === index) {
                    this.$router.push({ name: this.tags[index - 1].name });
                } else {
                    this.$router.push({ name: this.tags[index].name });
                }
            }
        }
    },
    computed: {
        ...mapState({
            tags: state => state.tab.tabList
        })
    }
}
</script>

<style lang="less" scoped>
.tabs {
    padding: 20px 20px 0 20px;

    .el-tag {
        margin-right: 15px;
        cursor: pointer;
    }
}
</style>
