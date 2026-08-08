#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
download_data.py

从 Release 下载第21章人脸关键点定位的模型文件 shape_predictor_68_face_landmarks.dat
到当前目录（landmark/ 目录）。

Release 地址（见 readme.md）:
    https://gitee.com/SylverQG/resource/releases/tag/data-04-face-landmark-detection

说明:
    - 该文件为单个模型文件（约 99MB），不需要打包成 zip
    - 直接作为附件上传到 Release，脚本下载后放置到当前目录

用法:
    python download_data.py
"""

import os
import sys
import urllib.request

# Release 附件下载直链
DOWNLOAD_URL = (
    "https://gitee.com/SylverQG/resource/releases/download/"
    "data-04-face-landmark-detection/shape_predictor_68_face_landmarks.dat"
)

# 下载目标文件名（与代码中引用保持一致）
FILE_NAME = "shape_predictor_68_face_landmarks.dat"

# 当前脚本所在目录（landmark/ 目录）
TARGET_DIR = os.path.dirname(os.path.abspath(__file__))


def download_file(url: str, dest: str) -> None:
    """带进度显示的下载，支持断点续传。"""
    if os.path.exists(dest):
        local_size = os.path.getsize(dest)
        headers = {"Range": f"bytes={local_size}-"}
        req = urllib.request.Request(url, headers=headers)
        mode = "ab"
    else:
        local_size = 0
        req = urllib.request.Request(url)
        mode = "wb"

    with urllib.request.urlopen(req) as resp:
        total = int(resp.headers.get("Content-Length", 0)) + local_size
        downloaded = local_size
        with open(dest, mode) as f:
            while True:
                chunk = resp.read(1024 * 1024)
                if not chunk:
                    break
                f.write(chunk)
                downloaded += len(chunk)
                if total:
                    pct = downloaded * 100 // total
                    print(f"\r下载进度: {pct:3d}%  ({downloaded}/{total} bytes)", end="")
                else:
                    print(f"\r已下载: {downloaded} bytes", end="")
    print()


def main() -> None:
    dest = os.path.join(TARGET_DIR, FILE_NAME)

    print(f"开始下载 {DOWNLOAD_URL}")
    try:
        download_file(DOWNLOAD_URL, dest)
    except Exception as e:
        print(f"\n下载失败: {e}", file=sys.stderr)
        print("请检查网络或 Release 附件地址是否有效。", file=sys.stderr)
        sys.exit(1)

    # 简单校验：文件应存在且非空
    if os.path.exists(dest) and os.path.getsize(dest) > 0:
        size_mb = os.path.getsize(dest) / 1024 / 1024
        print(f"完成！{FILE_NAME} 已就绪（{size_mb:.1f}MB）。")
    else:
        print("错误: 下载结果为空文件。", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()