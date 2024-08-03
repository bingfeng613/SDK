## 总结

### 已解析库
"导出数据":导出对应的excel  -> done
"下载原文"：下载对应的隐私政策html
"生成统计"：跳转到统计数据那一页，根据选中的生成统计数据


### 统计数据
"查看解析来源"：查看统计数据是选中哪些进行生成的，额外设置一个弹窗显示App名字列表

"导出统计数据"：下载excel，里面有这页的缺失声明数、模糊声明数、比例啥的数据
"导出统计图像"：下载这页统计卡片的jpg 
"导出统计报告"：下载统计卡片拼起来的pdf

### 前端运行
在终端执行
npm install    -> 有warning等内容不要紧

npm run serve   

### 后端运行
cd backend

下载依赖 pip install -r requirements.txt

设置数据库 导入sql文件，修改setting.py内DATABASES信息

启动后端 python manage.py runserver 