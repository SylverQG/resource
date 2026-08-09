# Scan

注意安装`tesseract-ocr`,将其放在了 [release](https://github.com/SylverQG/resource/releases/tag/exe-01-tesseract-ocr-v4)

# 使用脚本下载到当前目录
```bash
python utils/download-opencv.py 第10章
```

下载后得到 tesseract-ocr-setup-4.00.00dev.exe，双击安装。

安装完成后，需要在代码中配置 tesseract 路径（根据实际安装位置修改）：
```python
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
```