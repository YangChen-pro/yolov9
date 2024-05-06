import csv
import os
import cv2
import random
import shutil

ori_data = []

with open(f'ori_data(label)/任务一标签（新）.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    for row in reader:
        ori_data.append(row)

ori_data = ori_data[1:]  # 去掉表头
# print(ori_data)

# ori_data = ori_data[:20]  # 只取前几个数据


def split_number_and_resize_bbox(number, xmin, ymin, xmax, ymax):
    # 去掉小数点
    number_str = str(number).replace('.', '')

    # 计算划分的数量
    n = len(number_str)

    # 计算原始的目标框宽度
    w = xmax - xmin

    # 计算新的目标框宽度
    new_w = w / n

    # 划分数字并重新计算目标框
    results = []
    for i in range(n):
        new_xmin = xmin + i * new_w
        new_xmax = new_xmin + new_w
        results.append((number_str[i], new_xmin, ymin, new_xmax, ymax))

    return results


new_data = []

# 生成新的数据
for i, row in enumerate(ori_data):
    image_name = row[0].replace('.jpg', '')
    number = row[1]
    xmin = int(row[2])
    ymin = int(row[3])
    xmax = int(row[4])
    ymax = int(row[5])

    results = split_number_and_resize_bbox(number, xmin, ymin, xmax, ymax)

    for j, result in enumerate(results):
        new_number = result[0]
        new_xmin = result[1]
        new_ymin = result[2]
        new_xmax = result[3]
        new_ymax = result[4]

        new_data.append((image_name, new_number, new_xmin, new_ymin, new_xmax, new_ymax))

classes = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']


def convert_to_yolo_format(image_name, number, xmin, ymin, xmax, ymax, img_width, img_height):
    dw = 1. / img_width
    dh = 1. / img_height
    x = (xmin + xmax) / 2.0
    y = (ymin + ymax) / 2.0
    w = xmax - xmin
    h = ymax - ymin
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh

    return f'{image_name} {classes.index(number)} {x} {y} {w} {h}'


yolo_data = []

for i, row in enumerate(new_data):
    image_name = row[0]
    number = row[1]
    xmin = row[2]
    ymin = row[3]
    xmax = row[4]
    ymax = row[5]
    image = cv2.imread(f'ori_data(label)/{image_name}.jpg')
    img_height, img_width = image.shape[:2]
    yolo_data.append(convert_to_yolo_format(image_name, number, xmin, ymin, xmax, ymax, img_width, img_height))
    # yolo_data.append(f'{image_name} {number} {xmin} {ymin} {xmax} {ymax}')  # 不直接转换

# 创建一个新的文件夹'new_data(label)'，用于存放新的数据
if not os.path.exists('new_data(label)'):
    os.makedirs('new_data(label)')
    print('new_data(label)文件夹创建成功！')

# 创建三个文件夹，用于存放训练集、验证集、测试集
if not os.path.exists('new_data(label)/train'):
    os.makedirs('new_data(label)/train')
    print('new_data(label)/train文件夹创建成功！')
if not os.path.exists('new_data(label)/valid'):
    os.makedirs('new_data(label)/valid')
    print('new_data(label)/val文件夹创建成功！')
if not os.path.exists('new_data(label)/test'):
    os.makedirs('new_data(label)/test')
    print('new_data(label)/test文件夹创建成功！')

# 每个文件夹下，有一个'labels'文件夹，用于存放txt文件，一个'images'文件夹，用于存放图片
if not os.path.exists('new_data(label)/train/labels'):
    os.makedirs('new_data(label)/train/labels')
    print('new_data(label)/train/labels文件夹创建成功！')
if not os.path.exists('new_data(label)/train/images'):
    os.makedirs('new_data(label)/train/images')
    print('new_data(label)/train/images文件夹创建成功！')
if not os.path.exists('new_data(label)/valid/labels'):
    os.makedirs('new_data(label)/valid/labels')
    print('new_data(label)/val/labels文件夹创建成功！')
if not os.path.exists('new_data(label)/valid/images'):
    os.makedirs('new_data(label)/valid/images')
    print('new_data(label)/val/images文件夹创建成功！')
if not os.path.exists('new_data(label)/test/labels'):
    os.makedirs('new_data(label)/test/labels')
    print('new_data(label)/test/labels文件夹创建成功！')
if not os.path.exists('new_data(label)/test/images'):
    os.makedirs('new_data(label)/test/images')
    print('new_data(label)/test/images文件夹创建成功！')

# 定义划分比例
train_ratio = 0.7  # 训练集比例
val_ratio = 0.15  # 验证集比例
test_ratio = 0.15  # 测试集比例

# image_name一样的，放在一起，构造字典{'image_name': [yolo_data]}
image_name_dict = {}
for data in yolo_data:
    data = data.split(' ')
    image_name = data[0]
    if image_name not in image_name_dict:
        image_name_dict[image_name] = []
    image_name_dict[image_name].append(' '.join(data[1:]))

# # 按照比例，放入不同的文件夹
# # 打乱数据、随机划分
# image_names = list(image_name_dict.keys())
# random.shuffle(image_names)
# cnt = 0
# for image_name in image_names:
#     data = image_name_dict[image_name]
#     data = '\n'.join(data)
#     if cnt < train_ratio * len(image_name_dict):
#         with open(f'new_data(label)/train/labels/{image_name}.txt', 'w') as f:
#             f.write(data)
#         shutil.copy2(f'ori_data(label)/{image_name}.jpg', f'new_data(label)/train/images/{image_name}.jpg')
#     elif cnt < (train_ratio + val_ratio) * len(image_name_dict):
#         with open(f'new_data(label)/valid/labels/{image_name}.txt', 'w') as f:
#             f.write(data)
#         shutil.copy2(f'ori_data(label)/{image_name}.jpg', f'new_data(label)/valid/images/{image_name}.jpg')
#     else:
#         with open(f'new_data(label)/test/labels/{image_name}.txt', 'w') as f:
#             f.write(data)
#         shutil.copy2(f'ori_data(label)/{image_name}.jpg', f'new_data(label)/test/images/{image_name}.jpg')
#
#     cnt += 1




