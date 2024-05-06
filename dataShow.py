# 查看image_name_dict矩形框的效果，即数据标注的效果
import os
import cv2

input_txt_file = r"C:\Users\Administrator\Desktop\labels"

# image_name_dict = {'image_name': [yolo_data]}
image_name_dict = {}
for txt_file in os.listdir(input_txt_file):
    with open(f'{input_txt_file}/{txt_file}', 'r') as f:
        bbox_data_list = f.readlines()
        image_name = txt_file.split('.')[0]
        image_name_dict[image_name] = bbox_data_list


if not os.path.exists('show_img'):
    os.makedirs('show_img')

for image_name, bbox_data_list in image_name_dict.items():
    image = cv2.imread(f'ori_data(label)/{image_name}.jpg')

    for bbox_data in bbox_data_list:
        bbox_data = bbox_data.split(' ')
        class_index, x, y, w, h = map(float, bbox_data)
        img_height, img_width = image.shape[:2]
        xmin = int((x - w / 2) * img_width)
        ymin = int((y - h / 2) * img_height)
        xmax = int((x + w / 2) * img_width)
        ymax = int((y + h / 2) * img_height)
        # xmin = int(x)
        # ymin = int(y)
        # xmax = int(w)
        # ymax = int(h)

        cv2.rectangle(image, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)

        label = str(int(class_index))

        cv2.putText(image, label, (xmin, ymin - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)

    # Save the image with bounding boxes
    cv2.imwrite(f'show_img/{image_name}.jpg', image)


# # 把未划分的yolo数据放入show_label文件夹，以txt文件写入
# if not os.path.exists('show_label'):
#     os.makedirs('show_label')

# for image_name, bbox_data_list in image_name_dict.items():
#     bbox_data_str = '\n'.join(bbox_data_list)
#     with open(f'show_label/{image_name}.txt', 'w') as f:
#         f.write(bbox_data_str)