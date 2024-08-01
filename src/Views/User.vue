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
          <doughnut-chart :data="linkData"></doughnut-chart>
          <div class="details">
            <div class="detail-item">
              <span class="detail-label">链接无法访问：</span>
              <span class="detail-value">15 / 5%</span>
              <div class="bar-bg">
                <div class="bar" :style="{ width: '5%', backgroundColor: '#621da9' }"></div>
              </div>
            </div>
            <div class="detail-item">
              <span class="detail-label">链接非隐私政策：</span>
              <span class="detail-value">110 / 35%</span>
              <div class="bar-bg">
                <div class="bar" :style="{ width: '35%', backgroundColor: '#a84bde' }"></div>
              </div>
            </div>
            <div class="detail-item">
              <span class="detail-label">链接为APP隐私政策：</span>
              <span class="detail-value">47 / 15%</span>
              <div class="bar-bg">
                <div class="bar" :style="{ width: '15%', backgroundColor: '#e25788' }"></div>
              </div>
            </div>
            <div class="detail-item">
              <span class="detail-label">链接为无数据声明的SDK隐私政策：</span>
              <span class="detail-value">48 / 15%</span>
              <div class="bar-bg">
                <div class="bar" :style="{ width: '15%', backgroundColor: '#ffb039' }"></div>
              </div>
            </div>
          </div>
        </div>
        <div class="chart">
          <h3>数据合规性</h3>
          <doughnut-chart :data="complianceData"></doughnut-chart>
          <div class="details">
            <p>278 总声明数</p>
            <p>of 618 总声明数</p>
            <div class="detail-item">
              <span class="detail-label">合规：</span>
              <span class="detail-value">45%</span>
              <div class="bar-bg">
                <div class="bar" :style="{ width: '45%', backgroundColor: '#FF6384' }"></div>
              </div>
            </div>
            <div class="detail-item">
              <span class="detail-label">缺失声明：</span>
              <span class="detail-value">185 / 30%</span>
              <div class="bar-bg">
                <div class="bar" :style="{ width: '30%', backgroundColor: '#36A2EB' }"></div>
              </div>
            </div>
            <div class="detail-item">
              <span class="detail-label">模糊声明：</span>
              <span class="detail-value">155 / 25%</span>
              <div class="bar-bg">
                <div class="bar" :style="{ width: '25%', backgroundColor: '#FFCE56' }"></div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import DoughnutChart from '@/components/DoughnutChart.vue'
import html2canvas from 'html2canvas';
import jsPDF from 'jspdf';
import * as XLSX from 'xlsx';


export default {
  components: {
    DoughnutChart
  },
  computed: {
    ...mapState(['linkData', 'complianceData']),
  },
  // data() {
  //   return {
  //     linkData: {
  //       labels: ['有效', '无法访问', '非隐私政策', 'APP隐私政策', 'SDK隐私政策'],
  //       datasets: [{
  //         data: [95, 15, 110, 47, 48],
  //         backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF']
  //       }]
  //     },
  //     complianceData: {
  //       labels: ['合规', '缺失声明', '模糊声明'],
  //       datasets: [{
  //         data: [278, 185, 155],
  //         backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56']
  //       }]
  //     }
  //   }
  // },
  methods: {
    viewSources() {
      // Implement the function to view sources
    },
    exportData() {
      const data = [
        ['类型', '数量', '比例'],
        ['缺失声明数', 185, '30%'],
        ['模糊声明数', 155, '25%'],
        ['合规声明数', 278, '45%']
      ];
      const ws = XLSX.utils.aoa_to_sheet(data);
      const wb = XLSX.utils.book_new();
      XLSX.utils.book_append_sheet(wb, ws, '统计数据');
      XLSX.writeFile(wb, '统计数据.xlsx');
    },
    async exportImage() {
      const charts = document.querySelector('.charts');
      const canvas = await html2canvas(charts);
      const imgData = canvas.toDataURL('image/jpeg');
      const link = document.createElement('a');
      link.href = imgData;
      link.download = '统计图像.jpg';
      link.click();
    },
    async exportReport() {
      const charts = document.querySelector('.charts');
      const canvas = await html2canvas(charts);
      const imgData = canvas.toDataURL('image/jpeg');
      const pdf = new jsPDF();
      pdf.addImage(imgData, 'JPEG', 10, 10, 200, 200);
      pdf.save('统计报告.pdf');
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
  margin: 10px 0;
}

.detail-label {
  color: #666;
}

.detail-value {
  color: #333;
  margin-left: 10px;
}

.bar-container {
  display: flex;
  align-items: center;
  width: 100%;
}

.bar-bg {
  height: 8px;
  background-color: #e0e0e0;
  margin: 5px 0;
  border-radius: 4px;
  position: relative;
}

.bar {
  height: 100%;
  border-radius: 4px;
  position: absolute;
  top: 0;
  left: 0;
}
</style>
