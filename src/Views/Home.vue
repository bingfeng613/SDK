<template>
    <div class="upload-policy-container">
        <div class="upload-box">
            <input type="file" id="file-upload" accept=".html" multiple @change="uploadFiles" style="display: none;" />
            <label for="file-upload" class="upload-button">上传隐私政策</label>
            <p>请选择一个/多个APP隐私政策html文件上传</p>
        </div>
    </div>
</template>

<script>
export default {
    methods: {
        uploadFiles(event) {
            const files = event.target.files;
            const formData = new FormData();
            for (let i = 0; i < files.length; i++) {
                formData.append('files[]', files[i]);
            }

            fetch('/upload', {
                method: 'POST',
                body: formData,
            })
                .then(response => response.json())
                .then(data => {
                    console.log('上传成功:', data);
                    // Handle success logic here
                })
                .catch(error => {
                    console.error('上传失败:', error);
                    // Handle failure logic here
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
    /* Increased padding for larger box */
    border-radius: 10px;
}

.upload-button {
    background-color: #3f51b5;
    color: white;
    padding: 20px 40px;
    /* Increased padding for larger button */
    border-radius: 5px;
    cursor: pointer;
    font-size: 18px;
    /* Increased font size */
}

p {
    margin-top: 20px;
    /* Increased margin for spacing */
    font-size: 16px;
    /* Increased font size */
    color: #666;
}
</style>
