import os

# 定义测试图像和标签的目录
test_imgs_dir = "dataset/TestDataset/CAMO/Imgs"
test_gt_dir = "dataset/TestDataset/CAMO/GT"
output_file = "dataset/TestDataset/CAMO/test.txt"

# 打开输出文件
with open(output_file, "w") as f:
    # 遍历测试图像目录中的文件
    for img_name in sorted(os.listdir(test_imgs_dir)):
        img_path = os.path.join(test_imgs_dir, img_name)
        gt_path = os.path.join(test_gt_dir, img_name.replace('.jpg', '.png'))  # 假设标签文件扩展名为 .png
        if os.path.exists(gt_path):
            f.write(f"{img_path} {gt_path}\n")
        else:
            print(f"Warning: Ground truth not found for {img_name}, expected {gt_path}")