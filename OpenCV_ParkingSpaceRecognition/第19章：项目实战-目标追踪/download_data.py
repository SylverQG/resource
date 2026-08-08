#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
download_data.py

从 Release 下载第19章目标追踪的数据包 tracking.zip（分卷），合并后分别解压到对应子文件夹：

    multi-object-tracking/        (OpenCV 版本，内含 videos/ 等)
    multiobject-tracking-dlib/    (dlib 版本，内含 mobilenet_ssd/、race.mp4 等)

Release 地址（见 readme.md）:
    https://gitee.com/SylverQG/resource/releases/tag/data-03-tracking

说明：
    - zip 内只应包含模型、视频等二进制文件（*.py 代码由 git 仓库管理）
    - 脚本会跳过 zip 中的 .py 文件，避免覆盖仓库中的代码
    - tracking.zip 以分卷形式（tracking.zip.001 / .002 / ...）发布，脚本自动下载并合并

用法:
    python download_data.py
"""

import os
import sys
import zipfile
import urllib.request

# Release 附件下载直链前缀（分卷）
BASE_URL = (
    "https://gitee.com/SylverQG/resource/releases/download/"
    "data-03-tracking/"
)

# 脚本所在目录（第19章根目录）
TARGET_DIR = os.path.dirname(os.path.abspath(__file__))

ZIP_NAME = "tracking.zip"

# zip 内需要按子目录解压的顶层文件夹 -> 解压目标文件夹
SUBDIR_MAP = {
    "multi-object-tracking": os.path.join(TARGET_DIR, "multi-object-tracking"),
    "multiobject-tracking-dlib": os.path.join(TARGET_DIR, "multiobject-tracking-dlib"),
}


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


def discover_parts(zip_name: str, target_dir: str) -> list:
    """发现目标目录下所有 <zip_name>.<序号> 分卷，按序号排序返回。"""
    parts = []
    index = 1
    while True:
        part = f"{zip_name}.{index:03d}"
        part_path = os.path.join(target_dir, part)
        if os.path.exists(part_path):
            parts.append(part)
            index += 1
        else:
            break
    return parts


def merge_parts(part_names: list, dest_zip: str) -> None:
    """按顺序将分卷合并为完整 zip。"""
    with open(dest_zip, "wb") as out:
        for part in part_names:
            part_path = os.path.join(TARGET_DIR, part)
            with open(part_path, "rb") as src:
                while True:
                    chunk = src.read(1024 * 1024)
                    if not chunk:
                        break
                    out.write(chunk)
    print(f"已合并 {len(part_names)} 个分卷 -> {dest_zip}")


def extract_to_subdirs(zip_path: str) -> None:
    """
    将 zip 中两个顶层子目录的内容分别解压到对应文件夹。
    例如 zip 内的 multi-object-tracking/videos/x.mp4
        -> 解压到 TARGET_DIR/multi-object-tracking/videos/x.mp4

    跳过 .py 文件：代码由 git 仓库管理，不参与解压。
    """
    with zipfile.ZipFile(zip_path, "r") as zf:
        names = zf.namelist()
        # 校验 zip 内是否包含需要分发的一级目录
        missing = [k for k in SUBDIR_MAP if not any(
            n.startswith(k + "/") for n in names)]
        if missing:
            print(
                f"错误: zip 内缺少以下子目录: {missing}\n"
                f"请确认 tracking.zip 内含 multi-object-tracking/ 与 multiobject-tracking-dlib/ 两个文件夹。",
                file=sys.stderr,
            )
            sys.exit(1)

        for name in names:
            top = name.split("/", 1)[0]
            target = SUBDIR_MAP.get(top)
            if target is None:
                continue  # zip 根目录下的无关文件，忽略

            if name.endswith(".py"):
                print(f"跳过代码文件: {name}")
                continue  # 代码由 git 管理，不覆盖仓库中的 py

            # 目标文件路径：去掉顶层目录名，合并到对应子文件夹
            rel = name.split("/", 1)[1] if "/" in name else ""
            dest_path = os.path.join(target, rel)
            if name.endswith("/"):
                os.makedirs(dest_path, exist_ok=True)
                continue
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            with zf.open(name) as src, open(dest_path, "wb") as dst:
                while True:
                    chunk = src.read(1024 * 1024)
                    if not chunk:
                        break
                    dst.write(chunk)

    for k, v in SUBDIR_MAP.items():
        print(f"已解压 {k}/ -> {v}")


def main() -> None:
    zip_path = os.path.join(TARGET_DIR, ZIP_NAME)

    # 1. 自动发现并下载所有分卷
    parts = discover_parts(ZIP_NAME, TARGET_DIR)
    if not parts:
        # 本地还没有任何分卷，从 .001 开始逐卷下载，直到某个序号 404
        index = 1
        while True:
            part = f"{ZIP_NAME}.{index:03d}"
            url = BASE_URL + part
            part_path = os.path.join(TARGET_DIR, part)
            print(f"开始下载 {url}")
            try:
                download_file(url, part_path)
            except urllib.error.HTTPError as e:
                if e.code == 404:
                    if index == 1:
                        print(f"错误: Release 中未找到 {part}，请确认附件名与 tag。", file=sys.stderr)
                        sys.exit(1)
                    print(f"分卷 {part} 不存在，视为下载完成。")
                    break
                print(f"\n下载失败: {e}", file=sys.stderr)
                sys.exit(1)
            except Exception as e:
                print(f"\n下载失败: {e}", file=sys.stderr)
                sys.exit(1)
            index += 1
    else:
        # 已有部分分卷，补齐缺失的（断点续传）
        index = len(parts) + 1
        while True:
            part = f"{ZIP_NAME}.{index:03d}"
            url = BASE_URL + part
            part_path = os.path.join(TARGET_DIR, part)
            print(f"开始下载 {url}")
            try:
                download_file(url, part_path)
            except urllib.error.HTTPError as e:
                if e.code == 404:
                    print(f"分卷 {part} 不存在，视为下载完成。")
                    break
                print(f"\n下载失败: {e}", file=sys.stderr)
                sys.exit(1)
            except Exception as e:
                print(f"\n下载失败: {e}", file=sys.stderr)
                sys.exit(1)
            index += 1

    # 2. 合并分卷
    parts = discover_parts(ZIP_NAME, TARGET_DIR)
    merge_parts(parts, zip_path)

    # 3. 解压
    print("开始解压...")
    try:
        extract_to_subdirs(zip_path)
    except zipfile.BadZipFile:
        print("错误: 合并后的文件不是有效的 zip 包，可能分卷不完整。", file=sys.stderr)
        print("请删除 tracking.zip.001/.002 等分卷后重新运行本脚本。", file=sys.stderr)
        sys.exit(1)

    print("完成！数据已就绪。")


if __name__ == "__main__":
    main()