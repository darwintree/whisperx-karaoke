# README

## 介绍

借助whisperx生成卡拉ok歌词所需的k轴ass文件。

## 使用

需要准备输入：

1. 音频
2. lrc文件（需要以行为单位的时间戳）

之后在任意位置新建文件夹，放入这两个文件即可。

## 安装

```shell
conda install pytorch==2.0.0 torchaudio==2.0.0 pytorch-cuda=11.8 -c pytorch -c nvidia
pip install git+https://github.com/m-bain/whisperx.git
```
