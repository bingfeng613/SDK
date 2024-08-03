<template>
    <div class="upload-policy-container">
        <div class="upload-box">
            <input type="file" id="file-upload" accept=".html,.docx,.pdf,.txt" multiple @change="handleFileSelect"
                style="display: none;" />
            <label for="file-upload" class="upload-button">上传隐私政策</label>
            <p>请选择一个/多个APP隐私政策html文件上传</p>
            <ul>
                <li v-for="(file, index) in selectedFiles" :key="index">
                    {{ file.name }}
                    <button @click="removeFile(index)">删除</button>
                </li>
            </ul>
            <button @click="uploadFiles" :disabled="selectedFiles.length === 0">确定上传</button>
        </div>
    </div>
</template>

<script>
import { MessageBox } from 'element-ui';
export default {
    data() {
        return {
            selectedFiles: [],
        };
    },
    methods: {
        handleFileSelect(event) {
            this.selectedFiles = Array.from(event.target.files);
        },
        removeFile(index) {
            this.selectedFiles.splice(index, 1);
        },
        uploadFiles() {
            const formData = new FormData();
            for (let i = 0; i < this.selectedFiles.length; i++) {
                formData.append('file', this.selectedFiles[i]); // 修改参数名为 'file'
            }

            console.log('Files to upload:', this.selectedFiles); // 调试信息

            fetch('http://127.0.0.1:8000/upload-app/', {
                method: 'POST',
                body: formData,
            })
                .then(response => response.json())
                .then(data => {
                    console.log('上传成功:', data);
                    this.$message.success('上传成功');
                    this.selectedFiles = []; // 清空已上传文件列表
                    this.$router.push({ name: 'mall' });
                })
                .catch(error => {
                    console.error('上传失败:', error);
                    this.$message.error('上传失败', error);
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
    height: 100vh;
}

.upload-box {
    text-align: center;
    border: 2px solid #e0e0e0;
    padding: 40px;
    border-radius: 10px;
}

.upload-button {
    background-color: #3f51b5;
    color: white;
    padding: 20px 40px;
    border-radius: 5px;
    cursor: pointer;
    font-size: 18px;
}

p {
    margin-top: 20px;
    font-size: 16px;
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
    margin-top: 10px;
}

button {
    background-color: #f44336;
    color: white;
    border: none;
    padding: 5px 10px;
    cursor: pointer;
    border-radius: 3px;
}

button:disabled {
    background-color: #e0e0e0;
    cursor: not-allowed;
}
</style>
