#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
download_data.py

从 Release 下载第18章 DNN 模块的数据包 dnn_blob.zip 并解压到当前目录。

Release 地址（见 readme.md）:
    https://gitee.com/SylverQG/resource/releases/tag/model-01-dnn_blob_googlenet_caffe

用法:
    python download_data.py
"""

import os
import sys
import zipfile
import urllib.request

# Release 附件下载直链（dnn_blob.zip）
DOWNLOAD_URL = (
    "https://gitee.com/SylverQG/resource/releases/download/"
    "model-01-dnn_blob_googlenet_caffe/dnn_blob.zip"
)

# 解压目标目录（当前脚本所在目录，即 dnn_blob/ 目录）
TARGET_DIR = os.path.dirname(os.path.abspath(__file__))

ZIP_NAME = "dnn_blob.zip"


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


def extract_zip(zip_path: str, target: str) -> None:
    """将 zip 解压到指定目录。"""
    with zipfile.ZipFile(zip_path, "r") as zf:
        for member in zf.infolist():
            zf.extract(member, target)
    print(f"解压完成 -> {target}")


def main() -> None:
    zip_path = os.path.join(TARGET_DIR, ZIP_NAME)

    print(f"开始下载 {DOWNLOAD_URL}")
    try:
        download_file(DOWNLOAD_URL, zip_path)
    except Exception as e:
        print(f"\n下载失败: {e}", file=sys.stderr)
        print("请检查网络或 Release 附件地址是否有效。", file=sys.stderr)
        sys.exit(1)

    print("开始解压...")
    try:
        extract_zip(zip_path, TARGET_DIR)
    except zipfile.BadZipFile:
        print("错误: 下载的文件不是有效的 zip 包，可能下载不完整。", file=sys.stderr)
        print("请删除 dnn_blob.zip 后重新运行本脚本。", file=sys.stderr)
        sys.exit(1)

    print("完成！数据已就绪。")


if __name__ == "__main__":
    main()