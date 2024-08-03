<template>
  <div class="mall-container">
    <h1>P-Sticker:SDK隐私声明合规检测平台</h1>
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
      <el-table-column type="selection" width="55"></el-table-column>
      <el-table-column prop="appName" label="APP名称" width="150"></el-table-column>
      <el-table-column prop="lackDataNum" label="缺失声明数" width="150"></el-table-column>
      <el-table-column prop="lackData" label="缺失声明项" width="150"></el-table-column>
      <el-table-column prop="fuzzyDataNum" label="模糊声明项" width="150"></el-table-column>
      <el-table-column prop="fuzzyData" label="模糊声明项数" width="150"></el-table-column>
      <el-table-column prop="brokenLinkNum" label="无效链接数" width="150"></el-table-column>
      <el-table-column prop="brokenLink" label="无效链接项" width="300"></el-table-column>
    </el-table>
    <div class="pagination">
      <el-pagination @current-change="handlePageChange" :current-page="currentPage" :page-size="pageSize"
        layout="prev, pager, next" :total="total"></el-pagination>
    </div>
  </div>
</template>

<script>
import { export_json_to_excel } from './Export2Excel';
import { mapActions } from 'vuex';
import axios from 'axios';
import { MessageBox } from 'element-ui';

export default {
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
    generateStats() {
      if (this.selectedItems.length === 0) {
        this.$message.warning('请先选择要生成统计的数据');
        return;
      }

      const linkCounts = { 有效: 0, 无法访问: 0, 非隐私政策: 0, APP隐私政策: 0, SDK隐私政策: 0 };
      const complianceCounts = { 合规: 0, 缺失声明: 0, 模糊声明: 0 };

      this.selectedItems.forEach(item => {
        linkCounts['有效'] += item.brokenLinkNum === 0 ? 1 : 0;
        linkCounts['无法访问'] += item.brokenLinkNum > 0 ? 1 : 0;
        linkCounts['非隐私政策'] += item.brokenLink.includes('非隐私政策') ? 1 : 0;
        linkCounts['APP隐私政策'] += item.brokenLink.includes('APP隐私政策') ? 1 : 0;
        linkCounts['SDK隐私政策'] += item.brokenLink.includes('SDK隐私政策') ? 1 : 0;

        complianceCounts['合规'] += item.lackDataNum === 0 ? 1 : 0;
        complianceCounts['缺失声明'] += item.lackDataNum > 0 ? 1 : 0;
        complianceCounts['模糊声明'] += item.fuzzyDataNum > 0 ? 1 : 0;
      });

      const linkData = {
        labels: ['有效', '无法访问', '非隐私政策', 'APP隐私政策', 'SDK隐私政策'],
        datasets: [{
          data: Object.values(linkCounts),
          backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF']
        }]
      };

      const complianceData = {
        labels: ['合规', '缺失声明', '模糊声明'],
        datasets: [{
          data: Object.values(complianceCounts),
          backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56']
        }]
      };

      this.updateStats({ linkData, complianceData });
      this.$router.push({ name: 'user' });
    },
    handlePageChange(page) {
      this.currentPage = page;
      if (this.search) {
        this.searchApps();
      } else {
        this.fetchData();
      }
    }
  },
  mounted() {
    this.fetchData();
  }
};
</script>

<style scoped>
.mall-container {
  padding: 20px;
}

h1 {
  font-size: 24px;
  font-weight: bold;
  text-align: center;
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
}

.pagination {
  text-align: right;
  margin-top: 20px;
}
</style>
