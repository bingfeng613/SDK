<template>
  <div>
    <main-header></main-header>
    <div class="mall-container">
      <div class="actions">
        <el-checkbox v-model="checkAll" @change="handleCheckAllChange">全选</el-checkbox>
        <el-input v-model="search" placeholder="搜索" prefix-icon="el-icon-search" class="search-input"
          @input="handleSearch"></el-input>
        <el-button type="primary" @click="confirmDelete">删除</el-button>
        <el-button type="primary" @click="downloadOriginal">下载原文</el-button>
        <el-button type="primary" @click="exportData">导出数据</el-button>
        <el-button type="primary" @click="generateStats">生成统计</el-button>
      </div>
      <el-table v-loading="loading" :data="tableData" style="width: 100%" @selection-change="handleSelectionChange"
        ref="table">
        <el-table-column type="selection" width="55" align="center"></el-table-column>
        <el-table-column prop="appName" label="APP名称" align="center"></el-table-column>
        <el-table-column prop="lackDataNum" label="缺失声明数" align="center"></el-table-column>
        <el-table-column prop="lackData" label="缺失声明项" align="center"></el-table-column>
        <el-table-column prop="fuzzyDataNum" label="模糊声明项" align="center"></el-table-column>
        <el-table-column prop="fuzzyData" label="模糊声明项数" align="center"></el-table-column>
        <el-table-column prop="brokenLinkNum" label="无效链接数" align="center"></el-table-column>
        <el-table-column prop="brokenLink" label="无效链接项" align="center"></el-table-column>
      </el-table>
      <div class="pagination">
        <el-pagination @current-change="handlePageChange" :current-page="currentPage" :page-size="pageSize"
          layout="prev, pager, next" :total="total"></el-pagination>
      </div>
    </div>
  </div>
</template>

<script>
import { export_json_to_excel } from './Export2Excel';
import { mapActions } from 'vuex';
import axios from 'axios';
import { MessageBox } from 'element-ui';
import MainHeader from '@/components/MainHeader.vue';

export default {
  components: { MainHeader },
  data() {
    return {
      checkAll: false,
      search: '',
      loading: false,
      currentPage: 1,
      pageSize: 5,
      total: 0,
      selectedItems: [],
      tableData: []
    };
  },
  methods: {
    ...mapActions(['updateStats']),
    handleCheckAllChange(val) {
      this.$refs.table.toggleAllSelection();
    },
    handleSelectionChange(val) {
      this.selectedItems = val;
    },
    // 获取数据
    async fetchData() {
      this.loading = true;
      try {
        const response = await axios.get('http://127.0.0.1:8000/apps/list', {
          params: {
            page_size: this.pageSize,
            page: this.currentPage
          }
        });
        this.tableData = response.data.results;
        this.total = response.data.count;
      } catch (error) {
        console.error('Error fetching data:', error);
      } finally {
        this.loading = false;
      }
    },
    // 字段查询 获取数据
    async searchApps() {
      this.loading = true;
      try {
        const response = await axios.get('http://127.0.0.1:8000/apps/search', {
          params: {
            keyword: this.search,
            page_size: this.pageSize,
            page: this.currentPage
          }
        });
        this.tableData = response.data.results;
        this.total = response.data.count;
      } catch (error) {
        console.error('Error searching apps:', error);
      } finally {
        this.loading = false;
      }
    },
    handleSearch() {
      this.currentPage = 1; // Reset to the first page when searching
      this.searchApps();
    },
    // 删除数据
    confirmDelete() {
      if (this.selectedItems.length === 0) {
        this.$message.warning('请先选择要删除的数据');
        return;
      }
      MessageBox.confirm('确认是否删除?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.deleteSelected();
      }).catch(() => {
        this.$message.info('已取消删除');
      });
    },
    deleteSelected() {
      const idsToDelete = this.selectedItems.map(item => item.id);

      axios.delete('http://127.0.0.1:8000/apps/delete/', { data: { ids: idsToDelete } })
        .then(response => {
          if (response.status === 200) {
            this.$message.success('删除成功');
            this.fetchData();
          } else {
            this.$message.error('删除失败，请重试');
          }
        })
        .catch(error => {
          this.$message.error('删除过程中出现错误，请重试');
          console.error('Error deleting items:', error);
        });
    },

    downloadOriginal() {
      if (this.selectedItems.length === 0) {
        this.$message.warning('请先选择要下载的内容');
        return;
      }

      const idsToDownload = this.selectedItems.map(item => item.id);

      // Fetch the content of the selected items
      const downloadPromises = this.selectedItems.map(item =>
        axios.get(item.htmlUrl, { responseType: 'blob' })
      );

      // Wait for all the requests to complete
      Promise.all(downloadPromises)
        .then(responses => {
          responses.forEach((response, index) => {
            const url = window.URL.createObjectURL(new Blob([response.data]));
            const link = document.createElement('a');
            link.href = url;
            link.setAttribute('download', `${this.selectedItems[index].appName}_privacy_policy.html`);
            document.body.appendChild(link);
            link.click();
            link.remove();
          });
          this.$message.success('下载成功');
        })
        .catch(error => {
          this.$message.error('下载过程中出现错误，请重试');
          console.error('Error downloading items:', error);
        });
    },
    // 导出数据
    exportData() {
      if (this.selectedItems.length === 0) {
        this.$message.warning('请先选择要导出的数据');
        return;
      }
      const data = this.selectedItems.map(item => ({
        'APP名称': item.appName,
        '缺失声明数': item.lackDataNum,
        '缺失声明项': item.lackData,
        '模糊声明项': item.fuzzyDataNum,
        '模糊声明项数': item.fuzzyData,
        '无效链接数': item.brokenLinkNum,
        '无效链接项': item.brokenLink,
        '隐私政策原文链接': item.htmlUrl
      }));
      export_json_to_excel(['APP名称', '缺失声明数', '缺失声明项', '模糊声明项', '模糊声明项数', '无效链接数', '无效链接项', '隐私政策原文链接'], data, '导出数据');
    },
    // 生成统计数据
    async generateStats() {
      if (this.selectedItems.length === 0) {
        this.$message.warning('请先选择要生成统计的数据');
        return;
      }
      // 调用成功 再进行跳转
      const selectedIds = this.selectedItems.map(item => item.id);
      const selectedAppNames = this.selectedItems.map(item => item.appName);
      // console.log(selectedIds)
      try {
        const response = await fetch(`http://127.0.0.1:8000/statistics/?ids=${JSON.stringify(selectedIds)}`);
        // console.log(response)
        if (!response.ok) {
          this.$message.warning('出现问题 请重试');
          return;
        }
        const data = await response.json();
        this.$store.commit('setStatistics', data);
        this.$store.commit('setSelectedApps', { ids: selectedIds, names: selectedAppNames });
        // console.log(data)
        // 调用成功 再进行跳转
        this.$router.push({ name: 'user' });
      } catch (error) {
        console.error('Failed to fetch statistics:', error);
      }
    },

    // 换页
    handlePageChange(page) {
      this.currentPage = page;
      if (this.search) {
        this.searchApps();
      } else {
        this.fetchData();
      }
    },
  },
  mounted() {
    this.fetchData();
  }
};
</script>

<style scoped>
.mall-container {
  padding: 20px;
  border: 2px solid #ccc;
  border-radius: 20px;
  display: flex;
  flex-direction: column;
  height: 70vh;
  margin: 0 20px;
  background-color: #f5f5f5;
}

.actions {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
}

.search-input {
  margin-left: 20px;
  margin-right: 20px;
}

.actions .el-button {
  margin-left: 10px;
  background-color: #336FFF;
  border-color:#336FFF;
}

.pagination {
  text-align: right;
  margin-top: 20px;
}
</style>
