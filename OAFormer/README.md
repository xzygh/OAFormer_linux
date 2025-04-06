# <p align=center>`OAFormer: Occlusion Aware Transformer for Camouflaged Object Detection`</p>

> **Authors:**
> [Xin Yang](https://github.com/xinyang920),
> Hengliang Zhu,
> Guojun Mao,
> [Shuli Xing](https://github.com/xingshulicc)



This official repository contains the source code, prediction results, and evaluation toolbox of paper 'OAFormer: Occlusion Aware Transformer for Camouflaged Object Detection'. The technical report could be found at [arXiv](https://arxiv.org/abs/). 


<p align="center">
    <img src="figs/net.png" width="800"  width="1500"/> <br />
    <em> 
    Figure 1: The overall architecture of the proposed occlusion aware transformer network. In part (a), we present the overall architecture of OAFormer. Part (b) displays the internal structures of the proposed neighborhood searching module (NSM).
    </em>
</p>


## 1. Code

**1.1. Requirements**

```
Python 3.7
Pytorch 1.13.0
OpenCV 4.6.0.66
Timm 0.6.11
Numpy 1.23.4
Tqdm 4.64.1
TensorboardX 2.5.1
Apex 0.1
```


**1.2. Download Datasets and Checkpoints.**

- **Datasets:** 

By default, you can put datasets into the folder 'dataset'.

- **Checkpoints:** 

By default, you can put datasets into the folder 'checkpoint'.

OAFormer: [Google Drive](https://drive.google.com/file/d/1kDuwHVZVvuyp4VzXUwb8vkklrq_SDpR3/view?usp=share_link)
Backbone: [Google Drive](https://drive.google.com/file/d/1snw4TYUCD5z4d3aaId1iBdw-yUKjRmPC/view?usp=sharing)

**1.3. Train.**
```
python train.py
```
**1.4. Test.**
```
python test.py
```

**1.5. Eval.**
```
python eval.py
```


## 2. Proposed OAFormer

### 2.1 COD Benchmark Results:

The prediction of our OAFormer can be found in [Google Drive](https://drive.google.com/file/d/15zRxBHQlcU-uLDHa2OfWnJeoLUf_6d2h/view?usp=share_link). Here are quantitative performance comparison.

<p align="center">
    <img src="figs/Performance.png" width="700"  width="1200"/> <br />
    <em> 
    </em>

</p>



## Acknowlegement
Thanks [Zhirui Zhao](https://github.com/zhaozhirui) providing a friendly [codebase](https://github.com/zhaozhirui/CTDNet) for binary segmentation tasks. And our code is built based on it. 



## Reference
You may want to cite:
```
@inproceedings{yang2023oaformer,
  title={OAFormer: Occlusion Aware Transformer for Camouflaged Object Detection},
  author={Yang, Xin and Zhu, Hengliang and Mao, Guojun and Xing, Shuli},
  booktitle={2023 IEEE International Conference on Multimedia and Expo (ICME)},
  pages={1421--1426},
  year={2023},
  organization={IEEE}
}
```

### License

Code in this repo is for non-commercial use only.






