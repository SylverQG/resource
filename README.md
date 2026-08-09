# Resource

个人资源收集与分享仓库，包含课程资料、代码、笔记等。


> 仓库内仅存放代码与轻量文件。

---

## 目录

- [OpenCV_ParkingSpaceRecognition](#opencv_parkingspacerecognition) — OpenCV 图像处理与项目实战课程
- [LLM_OpenCourse](#llm_opencourse) — 大语言模型系列课程
- [utils](#utils) — 下载工具

---

## OpenCV_ParkingSpaceRecognition

Python 打造停车场车位智能识别（2021 年），涵盖 OpenCV 图像处理基础到多个实战项目。

**章节：**

| 章节 | 内容 |
|---|---|
| 第 02-07 章 | 图像基本操作、图像处理 |
| 第 08 章 | 直方图与模板匹配 |
| 第 09 章 | 信用卡数字识别 |
| 第 10 章 | 文档扫描 OCR 识别 |
| 第 11-12 章 | 图像特征（Harris、SIFT、特征匹配） |
| 第 13 章 | 全景图像拼接 |
| 第 14 章 | 停车场车位识别 |
| 第 15 章 | 答题卡识别判卷 |
| 第 16-17 章 | 背景建模与光流估计 |
| 第 18 章 | OpenCV DNN 模块 |
| 第 19 章 | 目标追踪 |
| 第 20 章 | 卷积原理与操作 |
| 第 21 章 | 人脸关键点定位、疲劳检测 |

### 下载大文件

```bash
# 下载单个章节
python utils/download.py 第14章

# 下载全部章节
python utils/download.py
```

---

## LLM_OpenCourse

大语言模型系列课程（Word2Vec、NLP Pipeline、Transformer、Prompt Tuning、BM System）。

| Series | 内容 |
|---|---|
| Series 1 | Word2Vec 超参搜索、NLP Pipeline（PyTorch）、Transformer、Prompt/Delta Tuning、BM System |
| Series 2 | 大模型专题讲座（人类反馈强化学习、多模态、自主智能体、AI 安全与伦理等） |

### 下载大文件

```bash
python utils/download-LLM_OC.py
```

---

## utils

通用下载工具：

| 工具 | 用途 |
|---|---|
| [`download.py`](utils/download.py) | 通用下载器，根据清单批量下载 Release 附件 |
| [`download-LLM_OC.py`](utils/download-LLM_OC.py) | LLM_OpenCourse 专用下载器 |
| [`split_zip.py`](utils/split_zip.py) | 大文件分卷拆分工具（仅当附件超 100MB 时使用） |

### 下载机制

1. 清单文件 [`OpenCV_ParkingSpaceRecognition/download_release.txt`](OpenCV_ParkingSpaceRecognition/download_release.txt) 记录每个章节的资源地址
2. `utils/download.py` 读取清单，自动下载并解压到对应目录
3. 大文件上传在 GitHub Releases，不占用仓库空间

---

## License

[GLWT（Good Luck With That）公共许可证](LICENSE)