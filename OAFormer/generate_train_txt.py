import os

# 定义图像和标签的目录
imgs_dir = "dataset/TrainDataset/Imgs"
gt_dir = "dataset/TrainDataset/GT"
output_file = "dataset/TrainDataset/train.txt"

# 打开输出文件
with open(output_file, "w") as f:
    # 遍历图像目录中的文件
    for img_name in sorted(os.listdir(imgs_dir)):
        img_path = os.path.join(imgs_dir, img_name)
        # 将 .jpg 替换为 .png 以匹配标签文件
        gt_path = os.path.join(gt_dir, img_name.replace('.jpg', '.png'))
        # 检查标签文件是否存在
        if os.path.exists(gt_path):
            f.write(f"{img_path} {gt_path}\n")
        else:
            print(f"Warning: Ground truth not found for {img_name}, expected {gt_path}")