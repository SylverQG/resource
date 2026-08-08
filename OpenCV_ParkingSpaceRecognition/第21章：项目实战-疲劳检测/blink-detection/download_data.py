#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
download_data.py

从 Release 下载第21章疲劳检测的模型文件与测试视频到当前目录
（blink-detection/ 目录）。

文件来源：
    - test.mp4                              -> data-05-blink-detection
    - shape_predictor_68_face_landmarks.dat -> data-04-face-landmark-detection（复用上一章）

用法:
    python download_data.py
"""

import os
import sys
import urllib.request

# 各文件的下载地址（附件名 == 本地文件名）
DOWNLOAD_MAP = [
    (
        "shape_predictor_68_face_landmarks.dat",
        "https://gitee.com/SylverQG/resource/releases/download/"
        "data-04-face-landmark-detection/shape_predictor_68_face_landmarks.dat",
    ),
    (
        "test.mp4",
        "https://gitee.com/SylverQG/resource/releases/download/"
        "data-05-blink-detection/test.mp4",
    ),
]

# 当前脚本所在目录（blink-detection/ 目录）
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
    for file_name, url in DOWNLOAD_MAP:
        dest = os.path.join(TARGET_DIR, file_name)

        print(f"开始下载 {url}")
        try:
            download_file(url, dest)
        except Exception as e:
            print(f"\n下载失败: {e}", file=sys.stderr)
            print("请检查网络或 Release 附件地址是否有效。", file=sys.stderr)
            sys.exit(1)

        # 简单校验：文件应存在且非空
        if os.path.exists(dest) and os.path.getsize(dest) > 0:
            size_mb = os.path.getsize(dest) / 1024 / 1024
            print(f"完成！{file_name} 已就绪（{size_mb:.1f}MB）。\n")
        else:
            print(f"错误: {file_name} 下载结果为空文件。", file=sys.stderr)
            sys.exit(1)

    print("全部文件下载完成！")


if __name__ == "__main__":
    main()