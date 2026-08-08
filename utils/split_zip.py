#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
split_zip.py

通用文件分卷拆分工具：将任意文件按指定分卷大小拆分为 xxx.001 / xxx.002 / ...
上传到 Release 前先运行本脚本（用于规避 Gitee 单文件 100MB 限制）。

用法:
    python split_zip.py <文件路径> [分卷大小MB]   # 例: python split_zip.py park.zip 90
    python split_zip.py                          # 不带参数时拆分当前目录的 park.zip，每卷 90MB（兼容旧用法）
"""

import os
import sys

DEFAULT_CHUNK_MB = 90  # 默认每卷 90MB
DEFAULT_ZIP_NAME = "park.zip"  # 无参数时的默认文件
LIMIT_MB = 100  # 平台单文件上传限制（用于提示）


def split_file(file_path: str, chunk_size: int) -> list:
    """按 chunk_size 字节拆分文件，返回生成的分卷文件名列表。"""
    parts = []
    index = 1
    with open(file_path, "rb") as src:
        while True:
            chunk = src.read(chunk_size)
            if not chunk:
                break
            part_name = f"{file_path}.{index:03d}"
            with open(part_name, "wb") as dst:
                dst.write(chunk)
            parts.append(part_name)
            print(f"已生成 {part_name} ({len(chunk)} bytes)")
            index += 1
    return parts


def main() -> None:
    # 解析参数
    if len(sys.argv) >= 2:
        target_path = sys.argv[1]
    else:
        target_path = os.path.join(os.getcwd(), DEFAULT_ZIP_NAME)

    chunk_mb = DEFAULT_CHUNK_MB
    if len(sys.argv) >= 3:
        chunk_mb = float(sys.argv[2])

    if not os.path.exists(target_path):
        print(f"错误: 未找到 {target_path}，请检查路径或文件是否已打包。", file=sys.stderr)
        sys.exit(1)

    if os.path.isdir(target_path):
        print(f"错误: {target_path} 是目录，请传入文件路径。", file=sys.stderr)
        sys.exit(1)

    total = os.path.getsize(target_path)
    chunk_size = int(chunk_mb * 1024 * 1024)
    print(f"拆分 {target_path} ({total} bytes) -> 每卷 {chunk_mb}MB")

    parts = split_file(target_path, chunk_size)

    if total > LIMIT_MB * 1024 * 1024:
        print(f"\n警告: 源文件 {total/1024/1024:.1f}MB 超过 {LIMIT_MB}MB，")
        print(f"      拆分为 {len(parts)} 卷后，请确认每卷 < {LIMIT_MB}MB 再上传。")
    print("拆分完成。")


if __name__ == "__main__":
    main()