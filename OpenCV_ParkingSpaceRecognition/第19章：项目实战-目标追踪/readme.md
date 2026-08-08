# 目标追踪

将相关模型与视频放在了 [release](https://gitee.com/SylverQG/resource/releases/tag/data-03-tracking) 中

zip 内仅含模型、视频等二进制文件，代码（*.py）由本仓库直接提供：
- multi-object-tracking/
  - videos/（los_angeles.mp4、nascar.mp4、soccer_01.mp4、soccer_02.mp4）
- multiobject-tracking-dlib/
  - mobilenet_ssd/（MobileNetSSD_deploy.caffemodel、MobileNetSSD_deploy.prototxt）
  - dlib-19.7.0-cp36-cp36m-win_amd64.whl
  - race.mp4

# 使用脚本下载并解压到对应子文件夹
```bash
python download_data.py
```

下载后内容会分别放入 multi-object-tracking/ 与 multiobject-tracking-dlib/ 两个文件夹。

