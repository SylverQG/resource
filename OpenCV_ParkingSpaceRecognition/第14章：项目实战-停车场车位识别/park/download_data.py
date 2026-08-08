#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
download_data.py

从 Release 下载第14章停车场车位识别的数据包 park.zip（分卷），
合并还原后解压到当前目录。

Release 附件: park.zip.001 / park.zip.002
Release 地址（见 readme.md）:
    https://gitee.com/SylverQG/resource/releases/tag/data-01-parking-space-recognition

用法:
    python download_data.py
"""

import os
import sys
import zipfile
import urllib.request

# Release 附件下载直链（分卷）
BASE_URL = (
    "https://gitee.com/SylverQG/resource/releases/download/"
    "data-01-parking-space-recognition/"
)

# 分卷文件名列表（按顺序合并）
PART_NAMES = ["park.zip.001", "park.zip.002"]

# 合并后的完整 zip 名
ZIP_NAME = "park.zip"

# 解压目标目录（当前脚本所在目录，即 park/ 目录）
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


def merge_parts(part_names: list, dest_zip: str) -> None:
    """按顺序将分卷合并为完整 zip。"""
    with open(dest_zip, "wb") as out:
        for part in part_names:
            part_path = os.path.join(TARGET_DIR, part)
            if not os.path.exists(part_path):
                print(f"错误: 缺少分卷 {part}，请重新下载。", file=sys.stderr)
                sys.exit(1)
            with open(part_path, "rb") as src:
                while True:
                    chunk = src.read(1024 * 1024)
                    if not chunk:
                        break
                    out.write(chunk)
    print(f"已合并 {len(part_names)} 个分卷 -> {dest_zip}")


def extract_zip(zip_path: str, target: str) -> None:
    """将 zip 解压到指定目录。"""
    with zipfile.ZipFile(zip_path, "r") as zf:
        for member in zf.infolist():
            zf.extract(member, target)
    print(f"解压完成 -> {target}")


def main() -> None:
    zip_path = os.path.join(TARGET_DIR, ZIP_NAME)

    # 1. 下载所有分卷
    for part in PART_NAMES:
        part_path = os.path.join(TARGET_DIR, part)
        url = BASE_URL + part
        print(f"开始下载 {url}")
        try:
            download_file(url, part_path)
        except Exception as e:
            print(f"\n下载失败: {e}", file=sys.stderr)
            sys.exit(1)

    # 2. 合并分卷
    merge_parts(PART_NAMES, zip_path)

    # 3. 解压
    print("开始解压...")
    try:
        extract_zip(zip_path, TARGET_DIR)
    except zipfile.BadZipFile:
        print("错误: 合并后的文件不是有效的 zip 包，可能分卷不完整。", file=sys.stderr)
        print("请删除 park.zip.001 / park.zip.002 后重新运行本脚本。", file=sys.stderr)
        sys.exit(1)

    print("完成！数据已就绪。")


if __name__ == "__main__":
    main()