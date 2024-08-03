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
        <p>{{ statistics.appNum }} 篇APP隐私政策</p>
        <p>共解析：</p>
        <p>{{ statistics.declareGroupNum }} 个声明组</p>
        <p>{{ statistics.declareUrlNum }} 个声明链接</p>
      </div>
      <div class="charts">
        <div class="chart">
          <h3>链接有效性</h3>
          <doughnut-chart :data="linkData" center-label="有效"></doughnut-chart>

          <div class="details">
            <p>{{ statistics.complianceUrlNum }} 有效链接数</p>
            <p>of {{ statistics.declareUrlNum }} 总链接数</p>
            <div class="detail-item" v-for="(value, label) in linkDetails" :key="label">
              <span class="detail-label">{{ label }}：</span>
              <span class="detail-value">{{ value.count }} / {{ value.proportion }}</span>
              <div class="bar-bg">
                <div class="bar" :style="{ width: value.proportion, backgroundColor: value.color }"></div>
              </div>
            </div>
          </div>
        </div>
        <div class="chart">
          <h3>数据合规性</h3>

          <doughnut-chart :data="complianceData" center-label="合规"></doughnut-chart>
          <div class="details">
            <p>{{ statistics.complianceGroupNum }} 合规声明数</p>
            <p>of {{ statistics.declareGroupNum }} 总声明数</p>
            <div class="detail-item" v-for="(value, label) in complianceDetails" :key="label">
              <span class="detail-label">{{ label }}：</span>
              <span class="detail-value">{{ value.count }} / {{ value.proportion }}</span>
              <div class="bar-bg">
                <div class="bar" :style="{ width: value.proportion, backgroundColor: value.color }"></div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <el-dialog title="解析来源" :visible.sync="dialogVisible" width="30%" @close="handleClose">
      <el-list>
        <el-list-item v-for="name in selectedAppNames" :key="name" class="list-item">
          <span class="app-name">{{ name }}</span>
        </el-list-item>
      </el-list>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">关闭</el-button>
      </div>
    </el-dialog>

  </div>
</template>

<script>
import { mapState } from 'vuex';
import DoughnutChart from '@/components/DoughnutChart.vue';
import html2canvas from 'html2canvas';
import jsPDF from 'jspdf';
import axios from "axios";

export default {
  components: {
    DoughnutChart
  },
  data() {
    return {
      dialogVisible: false
    };
  },
  computed: {
    ...mapState({
      statistics: state => state.stats.statistics,
      selectedAppNames: state => state.stats.selectedApps.names,
      selectedAppIds: state => state.stats.selectedApps.ids
    }),
    linkDetails() {
      return {
        '链接无法访问': {
          count: this.statistics.UnableToConnectNum,
          proportion: this.statistics.UnableToConnectProportion,
          color: '#621da9'
        },
        '链接非隐私政策': {
          count: this.statistics.NotPrivacyPolicyNum,
          proportion: this.statistics.NotPrivacyPolicyProportion,
          color: '#a84bde'
        },
        '链接为APP隐私政策': {
          count: this.statistics.appPrivacyPolicyNum,
          proportion: this.statistics.appPrivacyPolicyProportion,
          color: '#e25788'
        },
        '链接为无数据声明的SDK隐私政策': {
          count: this.statistics.notDataInsidePrivacyPolicyNum,
          proportion: this.statistics.notDataInsidePrivacyPolicyProportion,
          color: '#ffb039'
        }
      };
    },
    complianceDetails() {
      return {
        // '合规': {
        //   count: this.statistics.complianceGroupNum,
        //   proportion: this.statistics.complianceGroupProportion,
        //   color: '#FF6384'
        // },
        '缺失声明': {
          count: this.statistics.lackDataNum,
          proportion: this.statistics.lackDataProportion,
          color: '#36A2EB'
        },
        '模糊声明': {
          count: this.statistics.fuzzyDataNum,
          proportion: this.statistics.fuzzyDataProportion,
          color: '#FFCE56'
        }
      };
    },
    linkData() {
      return {
        datasets: [{
          data: [this.statistics.complianceUrlNum, this.statistics.UnableToConnectNum, this.statistics.NotPrivacyPolicyNum, this.statistics.appPrivacyPolicyNum, this.statistics.notDataInsidePrivacyPolicyNum],
          backgroundColor: ['#FF6384', '#621da9', '#a84bde', '#e25788', '#ffb039']
        }],
        labels: ['有效', '链接无法访问', '链接非隐私政策', '链接为APP隐私政策', '链接为无数据声明的SDK隐私政策']
      };
    },
    complianceData() {
      return {
        datasets: [{
          data: [this.statistics.complianceGroupNum, this.statistics.lackDataNum, this.statistics.fuzzyDataNum],
          backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56']
        }],
        labels: ['合规', '缺失声明', '模糊声明']
      };
    }
  },
  methods: {
    viewSources() {
      this.dialogVisible = true;
    },
    handleClose() {
      this.dialogVisible = false;
    },
    // 导出数据
    async exportData() {
      console.log(this.selectedAppIds);
      try {
        const response = await axios.get("http://127.0.0.1:8000/statistics/excel/", {
          params: {
            ids: JSON.stringify(this.selectedAppIds)
          },
          responseType: 'blob' // 确保响应是一个 Blob 对象
        });

        // 检查响应的内容类型
        const contentType = response.headers['content-type'];
        console.log("Content Type:", contentType);

        // 创建一个URL对象指向Blob对象，并指定类型
        const blob = new Blob([response.data], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' });
        const url = window.URL.createObjectURL(blob);

        // 创建一个<a>标签元素
        const link = document.createElement('a');
        link.href = url;
        // 为文件设置下载名称
        link.setAttribute('download', 'statistics.xlsx');
        // 将<a>标签添加到页面中
        document.body.appendChild(link);
        // 触发点击事件下载文件
        link.click();
        // 移除<a>标签
        document.body.removeChild(link);
      } catch (error) {
        console.error("Error exporting data:", error);
      }
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
  },
  mounted() {
    console.log(this.statistics)
  }
}
</script>

<style scoped>
.dialog-footer {
  text-align: right;
}

.el-list-item {
  padding: 5px 0;
}

.app-name {
  display: inline-block;
  padding: 5px 10px;
  background-color: #f0f0f0;
  border: 1px solid #dcdcdc;
  border-radius: 5px;
  margin-right: 5px;
  margin-bottom: 5px;
}

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
