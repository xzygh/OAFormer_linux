# coding=utf-8
import os
import cv2
import torch
import numpy as np
from torch.utils.data import Dataset

########################### Data Augmentation ###########################
class Normalize(object):
    def __init__(self, mean, std):
        self.mean = mean 
        self.std = std
    
    def __call__(self, image, mask, edge=None):
        image = (image - self.mean)/self.std
        mask /= 255
        if edge is None:
            return image, mask
        else:
            edge /= 255
            return image, mask, edge


class RandomCrop(object):
    def __call__(self, image, mask, edge=None):
        H, W, _ = image.shape
        randw = np.random.randint(W/8)
        randh = np.random.randint(H/8)
        offseth = 0 if randh == 0 else np.random.randint(randh)
        offsetw = 0 if randw == 0 else np.random.randint(randw)
        p0, p1, p2, p3 = offseth, H+offseth-randh, offsetw, W+offsetw-randw
        if edge is None:
            return image[p0:p1, p2:p3, :], mask[p0:p1, p2:p3]

        else:
            return image[p0:p1, p2:p3, :], mask[p0:p1, p2:p3], edge[p0:p1, p2:p3]


class RandomFlip(object):
    def __call__(self, image, mask, edge=None):
        if edge is None:
            if np.random.randint(2) == 0:
                return image[:, ::-1, :], mask[:, ::-1]
            else:
                return image, mask
        else:
            if np.random.randint(2) == 0:
                return image[:, ::-1, :], mask[:, ::-1], edge[:, ::-1]
            else:
                return image, mask, edge


class Resize(object):
    def __init__(self, H, W):
        self.H = H
        self.W = W

    def __call__(self, image, mask):
        image = cv2.resize(image, dsize=(self.W, self.H), interpolation=cv2.INTER_LINEAR)
        mask = cv2.resize(mask, dsize=(self.W, self.H), interpolation=cv2.INTER_LINEAR)
        return image, mask

class ToTensor(object):
    def __call__(self, image, mask):
        image = torch.from_numpy(image)
        image = image.permute(2, 0, 1)
        mask = torch.from_numpy(mask)
        return image, mask


########################### Config File ###########################
class Config(object):
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.mean = np.array([[[124.55, 118.90, 102.94]]])
        self.std = np.array([[[56.77,  55.97,  57.50]]])
        print('\nParameters...')
        for k, v in self.kwargs.items():
            print('%-10s: %s' % (k, v))

    def __getattr__(self, name):
        if name in self.kwargs:
            return self.kwargs[name]
        else:
            return None


########################### Dataset Class ###########################
class Data(Dataset):
    def __init__(self, cfg):
        self.cfg = cfg
        self.normalize = Normalize(mean=cfg.mean, std=cfg.std)
        self.randomcrop = RandomCrop()
        self.randomflip = RandomFlip()
        self.resize = Resize(cfg.resize, cfg.resize)
        self.totensor = ToTensor()
        self.samples = []

        # 解析 train.txt 或 test.txt 文件
        with open(cfg.datapath + '/' + cfg.mode + '.txt', 'r') as lines:
            for line in lines:
                # 假设每行格式为 "image_path mask_path"
                parts = line.strip().split()
                if len(parts) == 2:
                    self.samples.append((parts[0], parts[1]))
                else:
                    raise ValueError(f"Invalid line format in {cfg.datapath}/{cfg.mode}.txt: {line.strip()}")

    def __getitem__(self, idx):
        # 从 samples 中获取图像路径和标签路径
        image_path, mask_path = self.samples[idx]

        print(f"Trying to read image: {image_path}")
        print(f"Trying to read mask: {mask_path}")

        # 读取图像和掩码
        image = cv2.imread(image_path)
        if image is None:
            raise FileNotFoundError(f"Image not found or cannot be read: {image_path}")
        image = image[:, :, ::-1].astype(np.float32)

        mask = cv2.imread(mask_path, 0)
        if mask is None:
            raise FileNotFoundError(f"Mask not found or cannot be read: {mask_path}")
        mask = mask.astype(np.float32)

        shape = mask.shape

        if self.cfg.mode == 'train':
            image, mask = self.normalize(image, mask)
            image, mask = self.randomcrop(image, mask)
            image, mask = self.randomflip(image, mask)
            return image, mask
        else:
            image, mask = self.normalize(image, mask)
            image, mask = self.resize(image, mask)
            image, mask = self.totensor(image, mask)
            return image, mask, shape, image_path

    def collate(self, batch):
        size = self.cfg.trainsize[np.random.randint(0, len(self.cfg.trainsize))]
        image, mask = [list(item) for item in zip(*batch)]
        for i in range(len(batch)):
            image[i] = cv2.resize(image[i], dsize=(size, size), interpolation=cv2.INTER_LINEAR)
            mask[i] = cv2.resize(mask[i],  dsize=(size, size), interpolation=cv2.INTER_LINEAR)
        image = torch.from_numpy(np.stack(image, axis=0)).permute(0, 3, 1, 2)
        mask = torch.from_numpy(np.stack(mask, axis=0)).unsqueeze(1)
        return image, mask

    def __len__(self):
        return len(self.samples)
