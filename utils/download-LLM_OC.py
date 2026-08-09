#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
download-LLM_OC.py

从 Release 下载 LLM_OpenCourse 课程的数据包并解压到对应目录。

Release:
    https://github.com/SylverQG/resource/releases/tag/data-06-LLM_OpenCourse

下载内容:
    Series-1.zip -> LLM_OpenCourse/Series 1/  （解压）
    Series-2.zip -> LLM_OpenCourse/Series 2/  （解压）

用法:
    python utils/download-LLM_OC.py
"""

import os
import sys
import zipfile
import urllib.request

# 仓库根目录（本脚本在 utils/ 下，向上两级）
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

BASE_URL = "https://github.com/SylverQG/resource/releases/download/data-06-LLM_OpenCourse/"

FILES = [
    {
        "url": BASE_URL + "Series-1.zip",
        "file_name": "Series-1.zip",
        "target_dir": os.path.join(REPO_ROOT, "LLM_OpenCourse", "Series 1"),
        "extract": True,
    },
    {
        "url": BASE_URL + "Series-2.zip",
        "file_name": "Series-2.zip",
        "target_dir": os.path.join(REPO_ROOT, "LLM_OpenCourse", "Series 2"),
        "extract": True,
    },
]


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
    for item in FILES:
        dest = os.path.join(item["target_dir"], item["file_name"])
        os.makedirs(item["target_dir"], exist_ok=True)

        print(f"[{item['file_name']}] -> {item['target_dir']}")
        print(f"开始下载 {item['url']}")
        try:
            download_file(item["url"], dest)
        except Exception as e:
            print(f"\n下载失败: {e}", file=sys.stderr)
            sys.exit(1)

        if not (os.path.exists(dest) and os.path.getsize(dest) > 0):
            print(f"错误: 下载结果为空文件。", file=sys.stderr)
            sys.exit(1)

        if item["extract"]:
            print("开始解压...")
            try:
                with zipfile.ZipFile(dest, "r") as zf:
                    zf.extractall(item["target_dir"])
                print(f"解压完成 -> {item['target_dir']}")
            except zipfile.BadZipFile:
                print(f"错误: 不是有效的 zip 包", file=sys.stderr)
                sys.exit(1)
        print()

    print("全部完成！")


if __name__ == "__main__":
    main()