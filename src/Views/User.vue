<template>
  <div>
    <main-header></main-header>
    <div class="container">
    <div class="header">
      <div class="buttons">
        <button @click="viewSources">查看解析来源</button>
        <button @click="exportData">导出统计数据</button>
        <button @click="exportImage">导出统计图像</button>
        <button @click="exportReport">导出统计报告</button>
      </div>
    </div>
    <div class="content">
      <div class="left-part">
        <div class="card-summary">
          <h3>共导入：</h3>
          <p>{{ statistics.appNum }} 篇APP隐私政策</p>
          <h3>共解析：</h3>
          <p>{{ statistics.declareGroupNum }} 个声明组</p>
          <p>{{ statistics.declareUrlNum }} 个声明链接</p>
        </div>
        <div class="chart-data">
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

      <div class="chart-url">
        <h3>链接有效性</h3>
        <doughnut-chart :data="linkData" center-label="有效"></doughnut-chart>

        <div class="details">
          <p>{{ statistics.complianceUrlNum }} 有效链接数</p>
          <p>of {{ statistics.declareUrlNum }} 总链接数</p>
          <div class="detail-item" v-for="(value, label) in linkDetails" :key="label">
            <div class="label-container">
              <span class="detail-label">{{ label }}：</span>
              <span class="detail-value">{{ value.count }} / {{ value.proportion }}</span>
            </div>
            <div class="bar-bg">
              <div class="bar" :style="{ width: value.proportion, backgroundColor: value.color }"></div>
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
  </div>

</template>

<script>
import { mapState } from 'vuex';
import DoughnutChart from '@/components/DoughnutChart.vue';
import html2canvas from 'html2canvas';
import jsPDF from 'jspdf';
import axios from "axios";
import MainHeader from '@/components/MainHeader.vue';
import { List } from 'element-ui';

export default {
  components: {
    DoughnutChart,
    MainHeader
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
      try {
        // 获取图表元素
        const chartDataElement = this.$el.querySelector('.chart-data');
        const chartUrlElement = this.$el.querySelector('.chart-url');

        // 使用 html2canvas 将第一个图表转换为图片
        const chartDataCanvas = await html2canvas(chartDataElement);
        const chartDataImage = chartDataCanvas.toDataURL('image/jpeg');

        // 使用 html2canvas 将第二个图表转换为图片
        const chartUrlCanvas = await html2canvas(chartUrlElement);
        const chartUrlImage = chartUrlCanvas.toDataURL('image/jpeg');

        // 创建一个 <a> 元素并触发下载第一个图表
        const link1 = document.createElement('a');
        link1.href = chartDataImage;
        link1.download = 'data-compliance-chart.jpg';
        document.body.appendChild(link1);
        link1.click();
        document.body.removeChild(link1);

        // 创建一个 <a> 元素并触发下载第二个图表
        const link2 = document.createElement('a');
        link2.href = chartUrlImage;
        link2.download = 'link-compliance-chart.jpg';
        document.body.appendChild(link2);
        link2.click();
        document.body.removeChild(link2);

      } catch (error) {
        console.error('Error exporting images:', error);
      }
    },
    async exportReport() {

      try {
        // 获取内容元素
        const contentElement = this.$el.querySelector('.content');

        // 保存当前的缩放比例
        const originalZoom = document.body.style.zoom;

        // 设置缩放比例为100%
        document.body.style.zoom = '100%';

        // 使用 html2canvas 将内容转换为图片
        const contentCanvas = await html2canvas(contentElement);
        const contentImage = contentCanvas.toDataURL('image/jpeg');

        // 恢复原有的缩放比例
        document.body.style.zoom = originalZoom;

        // 创建 jsPDF 实例，设置为横向 A4 页面
        const pdf = new jsPDF('landscape', 'mm', 'a4');

        const pageWidth = pdf.internal.pageSize.getWidth();
        const pageHeight = pdf.internal.pageSize.getHeight();

        // 设置标题
        const title = "P-Sticker: SDK Privacy Statement Compliance Detection Platform";
        const titleFontSize = 16;
        pdf.setFontSize(titleFontSize);
        pdf.text(title, pageWidth / 2, 10, { align: 'center' });

        // 计算图片显示区域
        const titleHeight = titleFontSize + 10; // 标题高度 + 上下边距
        const contentHeight = pageHeight - titleHeight - 10; // 剩余高度 - 底部边距

        // 将内容图片缩放以适应页面
        const imgProps = pdf.getImageProperties(contentImage);
        const imgWidth = imgProps.width;
        const imgHeight = imgProps.height;
        const ratio = Math.min(pageWidth / imgWidth, contentHeight / imgHeight);

        const pdfWidth = imgWidth * ratio;
        const pdfHeight = imgHeight * ratio;

        // 计算图片的位置，使其居中
        const xOffset = (pageWidth - pdfWidth) / 2;
        const yOffset = titleHeight;

        // 添加图片到 PDF
        pdf.addImage(contentImage, 'JPEG', xOffset, yOffset, pdfWidth, pdfHeight);

        // 生成并下载 PDF
        pdf.save('report.pdf');
      } catch (error) {
        console.error('Error exporting report:', error);
      }

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
  display: flex;
  flex-direction: column;
  height: 90vh;
  margin: 0 20px;
  border: 2px solid #ccc;
  border-radius: 20px;
  background-color: #f5f5f5;
}

.header {
  text-align: center;
}

.buttons {
  display: flex;
  justify-content: left;
  margin-left: 250px
}

.buttons button {
  margin-top: 0;
  margin-right: 80px;
  margin-bottom: 10px;
  margin-left: 20px;
  padding: 15px 40px;
  border: none;
  border-radius: 5px;
  background-color: #336FFF;
  border-color:#336FFF;
  color: white;
  cursor: pointer;
  transition: background-color 0.3s;
}

.content {
  display: flex;
  justify-content: space-around;
  margin-top: 20px;
  flex-wrap: wrap;
}

.card-summary {
  padding: 20px;
  border: 1px solid #ccc;
  margin-bottom:30px;
  border-radius: 10px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  background-color: #ffffff;
}

.chart-data {
  border: 1px solid #ccc;
  padding: 30px;
  border-radius: 10px;
  box-shadow: 0 10px 10px rgba(0, 0, 0, 0.1);
  background-color: #ffffff;
}

.chart-url {
  border: 1px solid #ccc;
  padding: 30px;
  border-radius: 10px;
  box-shadow: 0 10px 10px rgba(0, 0, 0, 0.1);
  width: 30%;
  background-color: #ffffff;
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



.label-container {
  display: flex; 
  justify-content: space-between; 
  align-items: center; 
}

.detail-label {
  color: #333;
}

.detail-value {
  color: #666;
  margin-left: 10px;
  margin-left: auto; 
  text-align: right; 
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
