<template>
    <div>
        <main-header></main-header>
        <div class="upload-policy-container">
            <div class="upload-box">
                <input type="file" id="file-upload" accept=".html" multiple @change="handleFileSelect"
                    style="display: none;" />
                <label for="file-upload" class="upload-button">上传隐私政策</label>
                <p>请选择一个/多个APP隐私政策html文件上传</p>
                <ul>
                    <li v-for="(file, index) in selectedFiles" :key="index">
                        {{ file.name }}
                        <button class="delete-button" @click="removeFile(index)">删除</button>
                    </li>
                </ul>
                <button class="confirm-button" @click="uploadFiles" :disabled="selectedFiles.length === 0">确定上传</button>
                <div v-if="loading" class="loading-overlay">
                    <div class="loading-spinner"></div>
                    <p>上传解析中，请稍等...</p>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { MessageBox } from 'element-ui';
import MainHeader from '@/components/MainHeader.vue';
import cookie from 'js-cookie'

export default {
    components: { MainHeader},
    data() {
        return {
            selectedFiles: [],
            user_account: this.$store.state.user.account,
            loading: false,
        };
    },
    methods: {
        handleFileSelect(event) {
            const files = Array.from(event.target.files);
            const invalidFiles = files.filter(file => file.type !== 'text/html');
            if (invalidFiles.length > 0) {
                this.$message.warning('只能上传html格式的文件');
                return;
            }
            this.selectedFiles = files;
        },
        removeFile(index) {
            this.selectedFiles.splice(index, 1);
        },
        uploadFiles() {
            this.loading = true; 

            const formData = new FormData();
            for (let i = 0; i < this.selectedFiles.length; i++) {
                formData.append('file', this.selectedFiles[i]); // 修改参数名为 'file'
            }

            console.log('Files to upload:', this.selectedFiles); // 调试信息

            formData.append('account', this.user_account); // 添加user_account参数

            fetch('http://127.0.0.1:8000/upload-app/', {
                method: 'POST',
                body: formData,
            })
                .then(response => response.json())
                .then(data => {
                    console.log('上传成功:', data);
                    this.$message.success('上传成功');
                    this.selectedFiles = []; // 清空已上传文件列表
                    console.log('note',this.loading) 
                    // this.loading = false;
                    setTimeout(() => {
                        this.loading = false; // 关闭加载动画
                        this.$router.push({ name: 'mall' }); // 跳转到指定页面
                    }, 10000);
                    // this.$router.push({ name: 'mall' });
                })
                .catch(error => {
                    console.error('上传失败:', error);
                    this.$message.error('上传失败', error);
                    // this.loading = false;
                });
        },
    },
};
</script>

<style scoped>
.upload-policy-container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 70vh;
    margin: 0 20px;
    border: 2px solid #ccc;
    border-radius: 20px;
    background-color: #f5f5f5;
}

.upload-box {
    text-align: center;
    border: 2px solid #ccc;
    padding: 60px;
    border-radius: 20px;
    background-color: white;
}

.upload-button {
    background-color: #336FFF;
    color: white;
    padding: 20px 40px;
    border-radius: 5px;
    cursor: pointer;
    font-size: 18px;
}

p {
    margin-top: 60px;
    margin-bottom: 40px;
    font-size: 20px;
    font-weight: bold;
    color: #666;
}

ul {
    list-style-type: none;
    padding: 0;
}

li {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 15px;
}

.delete-button {
    background-color: #f44336;
    color: white;
    border: none;
    padding: 5px 10px;
    cursor: pointer;
    border-radius: 3px;
}

.confirm-button {
    background-color: #336FFF;
    color: white;
    border: none;
    padding: 10px 20px;
    cursor: pointer;
    border-radius: 3px;
    transition: background-color 0.3s;
    margin-top: 10px;
}

.confirm-button:disabled {
    background-color: #ccc;
    cursor: not-allowed;
}

.loading-overlay {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(255, 255, 255, 0.8);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 10;
}

.loading-spinner {
    border: 4px solid rgba(0, 0, 0, 0.1);
    border-radius: 50%;
    border-top: 4px solid #3498db;
    width: 50px;
    height: 50px;
    animation: spin 2s linear infinite;
    margin-right: 10px;
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}
</style>
