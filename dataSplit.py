import os
import shutil

des_path = r"new_data(label)"
dir_name = ['test', 'train', 'valid']
txt_path = 'our_label'

# 根据img的名字，将对应的txt文件移动到对应的文件夹
for dir in dir_name:
    # 打开文件夹，遍历所有的jpg
    for file in os.listdir(f'{des_path}/{dir}/images'):
        if os.path.splitext(file)[1] == '.jpg':
            # 获取文件名
            basename = os.path.basename(file).split('.')[0]
            # 找到对应的txt文件
            txt_file = f'{txt_path}/{basename}.txt'
            # 复制到对应的文件夹
            shutil.copy2(txt_file, f'{des_path}/{dir}/labels')