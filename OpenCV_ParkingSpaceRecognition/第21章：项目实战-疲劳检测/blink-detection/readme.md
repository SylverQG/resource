# 疲劳检测

将相关模型与视频放在了 [release](https://github.com/SylverQG/resource/releases/tag/data-05-blink-detection) 中

Release 内包含以下文件（单个文件直接下载，无需打包）：
- shape_predictor_68_face_landmarks.dat（dlib 人脸关键点模型，约 99MB）
- test.mp4（测试视频）

代码（detect_blinks.py）由本仓库直接提供。

# 使用脚本下载到当前目录
```bash
python utils/download.py 第21章：项目实战-疲劳检测
```

下载后两个文件会放在 blink-detection/ 目录下，与 detect_blinks.py 同级。

# 运行
```bash
python detect_blinks.py --shape-predictor shape_predictor_68_face_landmarks.dat --video test.mp4
```
- `--shape-predictor`：dlib 人脸关键点模型路径
- `--video`：测试视频路径