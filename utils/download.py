#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
download.py

根据清单文件 download_release.txt 批量下载所有章节的资源文件，
zip 附件自动解压到对应目录。

清单位置（相对仓库根目录）:
    OpenCV_ParkingSpaceRecognition/download_release.txt

清单格式（每行，竖线 | 分隔）:
    目标目录(相对课程根目录) | 附件文件名 | Release tag/附件名 | 是否解压(y/n)

用法:
    python utils/download.py                  # 下载全部
    python utils/download.py 第14章            # 只下载匹配"第14章"的条目
"""

import os
import sys
import zipfile
import urllib.request

# 仓库根目录（本脚本在 utils/ 下，向上两级）
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 清单文件路径
LIST_FILE = os.path.join(
    REPO_ROOT, "OpenCV_ParkingSpaceRecognition", "download_release.txt"
)

# GitHub Release 下载直链前缀
BASE_URL = "https://github.com/SylverQG/resource/releases/download/"


def load_manifest(path: str) -> list:
    """读取清单文件，返回条目列表 [(目录, 文件名, tag/附件, 是否解压)]。"""
    entries = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = [p.strip() for p in line.split("|")]
            if len(parts) != 4:
                print(f"警告: 跳过无法解析的行: {line}", file=sys.stderr)
                continue
            entries.append(tuple(parts))
    return entries


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
    """将 zip 解压到指定目录（保留 zip 内部目录结构）。"""
    with zipfile.ZipFile(zip_path, "r") as zf:
        zf.extractall(target)
    print(f"解压完成 -> {target}")


def main() -> None:
    # 过滤关键字（可选参数）
    keyword = sys.argv[1] if len(sys.argv) > 1 else ""

    if not os.path.exists(LIST_FILE):
        print(f"错误: 未找到清单文件 {LIST_FILE}", file=sys.stderr)
        sys.exit(1)

    entries = load_manifest(LIST_FILE)

    # 统计匹配条目
    matched = [e for e in entries if keyword in e[0]] if keyword else entries
    if not matched:
        print(f"没有匹配 '{keyword}' 的下载条目。", file=sys.stderr)
        sys.exit(1)

    print(f"共 {len(matched)} 个下载项{'（过滤: ' + keyword + '）' if keyword else ''}\n")

    for target_rel, file_name, tag_asset, need_extract in matched:
        # 目标绝对目录：课程根目录 + 相对路径
        target_dir = os.path.join(
            REPO_ROOT, "OpenCV_ParkingSpaceRecognition", target_rel
        )
        dest = os.path.join(target_dir, file_name)
        url = BASE_URL + tag_asset

        os.makedirs(target_dir, exist_ok=True)

        print(f"[{file_name}] -> {target_dir}")
        print(f"开始下载 {url}")
        try:
            download_file(url, dest)
        except Exception as e:
            print(f"\n下载失败: {e}", file=sys.stderr)
            print("请检查网络或 Release 附件地址是否有效。", file=sys.stderr)
            sys.exit(1)

        # 校验非空
        if not (os.path.exists(dest) and os.path.getsize(dest) > 0):
            print(f"错误: {file_name} 下载结果为空文件。", file=sys.stderr)
            sys.exit(1)

        # 是否解压
        if need_extract.lower() == "y":
            print("开始解压...")
            try:
                extract_zip(dest, target_dir)
            except zipfile.BadZipFile:
                print(f"错误: {file_name} 不是有效的 zip 包，可能下载不完整。", file=sys.stderr)
                sys.exit(1)
        print()

    print("全部完成！")


if __name__ == "__main__":
    main()