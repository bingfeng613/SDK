import os
import math
import shutil

# 定义函数将文件按照规定数量划分到不同批次
def batch_files(input_folder, batch_size, batch_name):
    files = os.listdir(input_folder)
    num_batches = math.ceil(len(files) / batch_size)

    for i in range(num_batches):
        batch_files = files[i * batch_size : (i + 1) * batch_size]

        batch_folder = f"{batch_name}_{i+1}"
        batch_folder = os.path.join(input_folder, batch_folder)

        if not os.path.exists(batch_folder):
            os.makedirs(batch_folder)

        for file in batch_files:
            file_path = os.path.join(input_folder, file)
            shutil.move(file_path, os.path.join(batch_folder, file))

# 指定每批次的文件数量
batch_size = 10
input_folder = "../../data/Third_Party_Text/sdk_html_temp"
# input_folder = "../../data/Third_Party_Text/sdk_html"
batch_name = "third_html"

# 划分文件到不同批次
batch_files(input_folder, batch_size, batch_name)

# 删除原始输入文件夹中的文件
# for file in os.listdir(input_folder):
#     file_path = os.path.join(input_folder, file)
#     if os.path.isfile(file_path):
#         os.remove(file_path)

# 将批次文件夹中的文件移回原始输入文件夹
# for folder in os.listdir():
#     if folder.startswith("cleaned_batch_") and os.path.isdir(folder):
#         files = os.listdir(folder)
#         for file in files:
#             file_path = os.path.join(folder, file)
#             shutil.move(file_path, os.path.join(input_folder, file))
#         os.rmdir(folder)
