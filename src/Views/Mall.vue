<template>
  <div class="mall-container">
    <h1>P-Sticker:SDK隐私声明合规检测平台</h1>
    <div class="actions">
      <el-checkbox v-model="checkAll" @change="handleCheckAllChange">全选</el-checkbox>
      <el-input v-model="search" placeholder="搜索" prefix-icon="el-icon-search" class="search-input"></el-input>
      <el-button type="primary" @click="deleteSelected">删除</el-button>
      <el-button type="primary" @click="downloadOriginal">下载原文</el-button>
      <el-button type="primary" @click="exportData">导出数据</el-button>
      <el-button type="primary" @click="generateStats">生成统计</el-button>
    </div>
    <el-table v-loading="loading" :data="filteredData" style="width: 100%" @selection-change="handleSelectionChange"
      ref="table">
      <el-table-column type="selection" width="55"></el-table-column>
      <el-table-column prop="appName" label="APP名称" width="150"></el-table-column>
      <el-table-column prop="missingStatements" label="缺失声明数" width="150"></el-table-column>
      <el-table-column prop="missingItems" label="缺失声明项" width="150"></el-table-column>
      <el-table-column prop="redundantStatements" label="模糊声明项" width="150"></el-table-column>
      <el-table-column prop="redundantItems" label="模糊声明项数" width="150"></el-table-column>
      <el-table-column prop="invalidLinks" label="无效链接数" width="150"></el-table-column>
      <el-table-column prop="invalidLinkItems" label="无效链接项" width="300"></el-table-column>
    </el-table>
    <div class="pagination">
      <el-pagination @current-change="handlePageChange" :current-page="currentPage" :page-size="pageSize"
        layout="prev, pager, next" :total="filteredData.length"></el-pagination>
    </div>
  </div>
</template>

<script>
import { export_json_to_excel } from './Export2Excel';
import { mapActions } from 'vuex';

export default {
  data() {
    return {
      checkAll: false,
      search: '',
      loading: false,
      currentPage: 1,
      pageSize: 10,
      selectedItems: [],
      tableData: [
        {
          appName: '微信',
          missingStatements: 7,
          missingItems: 'IP地址信息',
          redundantStatements: 2,
          redundantItems: '网络信息',
          invalidLinks: 5,
          invalidLinkItems: 'https://www.umeng.com'
        },
        {
          appName: 'QQ',
          missingStatements: 5,
          missingItems: '机型信息',
          redundantStatements: 6,
          redundantItems: '网页浏览记录',
          invalidLinks: 7,
          invalidLinkItems: 'https://www.talkingdata.com'
        },
        {
          appName: '陌陌',
          missingStatements: 9,
          missingItems: '系统版本信息',
          redundantStatements: 3,
          redundantItems: '传感器信息',
          invalidLinks: 4,
          invalidLinkItems: 'https://support.im'
        },
        // Add more sample data as needed
      ],
    };
  },
  computed: {
    filteredData() {
      return this.tableData.filter(item =>
        item.appName.includes(this.search)
      );
    }
  },
  methods: {
    ...mapActions(['updateStats']),
    handleCheckAllChange(val) {
      this.$refs.table.toggleAllSelection();
    },
    handleSelectionChange(val) {
      this.selectedItems = val;
    },
    deleteSelected() {
      // 删除功能的实现
    },
    downloadOriginal() {
      // 下载功能的实现
    },
    exportData() {
      if (this.selectedItems.length === 0) {
        this.$message.warning('请先选择要导出的数据');
        return;
      }
      const data = this.selectedItems.map(item => ({
        'APP名称': item.appName,
        '缺失声明数': item.missingStatements,
        '缺失声明项': item.missingItems,
        '模糊声明项': item.redundantStatements,
        '模糊声明项数': item.redundantItems,
        '无效链接数': item.invalidLinks,
        '无效链接项': item.invalidLinkItems
      }));
      export_json_to_excel(['APP名称', '缺失声明数', '缺失声明项', '模糊声明项', '模糊声明项数', '无效链接数', '无效链接项'], data, '导出数据');
    },
    generateStats() {
      if (this.selectedItems.length === 0) {
        this.$message.warning('请先选择要生成统计的数据');
        return;
      }

      // 统计选中数据的各种信息
      const linkCounts = { 有效: 0, 无法访问: 0, 非隐私政策: 0, APP隐私政策: 0, SDK隐私政策: 0 };
      const complianceCounts = { 合规: 0, 缺失声明: 0, 模糊声明: 0 };

      this.selectedItems.forEach(item => {
        // 示例统计逻辑，根据实际数据需要调整
        linkCounts['有效'] += item.invalidLinks === 0 ? 1 : 0;
        linkCounts['无法访问'] += item.invalidLinks > 0 ? 1 : 0;
        linkCounts['非隐私政策'] += item.invalidLinkItems.includes('非隐私政策') ? 1 : 0;
        linkCounts['APP隐私政策'] += item.invalidLinkItems.includes('APP隐私政策') ? 1 : 0;
        linkCounts['SDK隐私政策'] += item.invalidLinkItems.includes('SDK隐私政策') ? 1 : 0;

        complianceCounts['合规'] += item.missingStatements === 0 ? 1 : 0;
        complianceCounts['缺失声明'] += item.missingStatements > 0 ? 1 : 0;
        complianceCounts['模糊声明'] += item.redundantStatements > 0 ? 1 : 0;
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

      // 更新统计信息
      this.updateStats({ linkData, complianceData });

      // 跳转到 User 页面
      this.$router.push({ name: 'user' });
    },
    handlePageChange(page) {
      this.currentPage = page;
    },
  },
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
