# README

<a target="_blank" href="https://colab.research.google.com/github/darwintree/whisperx-karaoke/blob/main/main.ipynb">
  <img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/>
</a>

## 介绍

借助whisperx生成卡拉ok歌词所需的k轴ass文件。注意，生成的准确性与输入质量相关，请确保lrc文件的时间戳准确。此外，使用UVR5处理后的人声文件作为输入会得到更准确的时间戳。

## 使用

可以在windows本地使用或者在 Colab 中运行

需要准备输入：

1. 音频
2. lrc文件（需要以行为单位的时间戳）

之后在任意位置新建文件夹，放入这两个文件即可。

### 在 Colab 中运行

<a target="_blank" href="https://colab.research.google.com/github/darwintree/whisperx-karaoke/blob/main/main.ipynb">
  <img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/>
</a>

选择运行时为 GPU，在默认工作文件夹内新建`raw`文件夹，之后将音频文件与lrc文件放入其中。依次执行单元格即可。

### 在本地运行

#### 安装依赖

```shell
conda install pytorch==2.0.0 torchaudio==2.0.0 pytorch-cuda=11.8 -c pytorch -c nvidia
pip install git+https://github.com/m-bain/whisperx.git
pip install whisperx-karaoke
```

#### 运行

例如文件被放置在了 `./raw/song1` 文件夹内

```shell
python -m whisperx_karaoke ./raw/song1
# usage: __main__.py [-h] [--device DEVICE] [--language LANGUAGE] [--offset OFFSET] dir [dir ...]
# __main__.py: error: the following arguments are required: dir
```

等待后ass文件会被输出到同一目录内。

其他参数

- --device DEVICE

  选择设备，默认为 `cuda`

- --language LANGUAGE

  选择语言，默认为 `ja`

- --offset OFFSET

  lrc 歌词的偏移量，默认为 `0`

## Q&A

Q: 为什么命令行会长时间卡住？
A：whisperx 会尝试连接 huggingface，如果网络连接状况不好，请尝试为命令行设置代理。如windows powershell `$Env:http_proxy="http://127.0.0.1:7890";$Env:https_proxy="http://127.0.0.1:7890"`
