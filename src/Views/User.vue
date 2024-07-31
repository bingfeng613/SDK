<template>
  <div class="container">
    <div class="header">
      <h1>P-Sticker: SDK隐私声明合规检测平台</h1>
      <div class="buttons">
        <button @click="viewSources">查看解析来源</button>
        <button @click="exportData">导出统计数据</button>
        <button @click="exportImage">导出统计图像</button>
        <button @click="exportReport">导出统计报告</button>
      </div>
    </div>
    <div class="content">
      <div class="card summary">
        <h3>共导入：</h3>
        <p>30篇APP隐私政策</p>
        <p>共解析：</p>
        <p>618个声明组</p>
        <p>315个声明链接</p>
      </div>
      <div class="charts">
        <div class="chart">
          <h3>链接有效性</h3>
          <doughnut-chart v-if="chartType === 'doughnut'" :data="linkData"></doughnut-chart>
          <bar-chart v-else :data="linkData"></bar-chart>
          <div class="details">
            <p>95 有效链接数</p>
            <p>of 315 总链接数</p>
            <div class="detail-item">
              <span class="detail-label">链接无法访问：</span><span class="detail-value">15 / 5%</span>
            </div>
            <div class="detail-item">
              <span class="detail-label">链接非隐私政策：</span><span class="detail-value">110 / 35%</span>
            </div>
            <div class="detail-item">
              <span class="detail-label">链接为APP隐私政策：</span><span class="detail-value">47 / 15%</span>
            </div>
            <div class="detail-item">
              <span class="detail-label">链接为无数据声明的SDK隐私政策：</span><span class="detail-value">48 / 15%</span>
            </div>
          </div>
        </div>
        <div class="chart">
          <h3>数据合规性</h3>
          <doughnut-chart v-if="chartType === 'doughnut'" :data="complianceData"></doughnut-chart>
          <bar-chart v-else :data="complianceData"></bar-chart>
          <div class="details">
            <p>278 总声明数</p>
            <p>of 618 总声明数</p>
            <div class="detail-item">
              <span class="detail-label">合规：</span><span class="detail-value">45%</span>
            </div>
            <div class="detail-item">
              <span class="detail-label">缺失声明：</span><span class="detail-value">185 / 30%</span>
            </div>
            <div class="detail-item">
              <span class="detail-label">模糊声明：</span><span class="detail-value">155 / 25%</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import DoughnutChart from '@/components/DoughnutChart.vue'
import BarChart from '@/components/BarChart.vue'

export default {
  components: {
    DoughnutChart,
    BarChart
  },
  data() {
    return {
      chartType: 'doughnut', // Change to 'bar' for bar charts
      linkData: {
        labels: ['有效', '无法访问', '非隐私政策', 'APP隐私政策', 'SDK隐私政策'],
        datasets: [{
          data: [95, 15, 110, 47, 48],
          backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF']
        }]
      },
      complianceData: {
        labels: ['合规', '缺失声明', '模糊声明'],
        datasets: [{
          data: [278, 185, 155],
          backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56']
        }]
      }
    }
  },
  methods: {
    viewSources() {
      // Implement the function to view sources
    },
    exportData() {
      // Implement the function to export data
    },
    exportImage() {
      // Implement the function to export image
    },
    exportReport() {
      // Implement the function to export report
    }
  }
}
</script>

<style scoped>
.container {
  font-family: 'PingFang SC', sans-serif;
  padding: 20px;
}

.header {
  text-align: center;
}

.buttons {
  display: flex;
  justify-content: center;
  margin-top: 10px;
}

.buttons button {
  margin: 0 10px;
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  background-color: #007bff;
  color: white;
  cursor: pointer;
  transition: background-color 0.3s;
}

.buttons button:hover {
  background-color: #0056b3;
}

.content {
  display: flex;
  justify-content: space-around;
  margin-top: 20px;
}

.card {
  border: 1px solid #ccc;
  padding: 20px;
  border-radius: 10px;
  width: 30%;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.charts {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  width: 65%;
}

.chart {
  border: 1px solid #ccc;
  padding: 20px;
  border-radius: 10px;
  margin-bottom: 20px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.details {
  margin-top: 10px;
}

.details p {
  margin: 5px 0;
}

.detail-item {
  display: flex;
  justify-content: space-between;
  margin: 5px 0;
}

.detail-label {
  color: #666;
}

.detail-value {
  color: #333;
}
</style>
