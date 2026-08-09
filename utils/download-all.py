#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
download-all.py

自动识别并顺序运行 utils/ 下所有 download-*.py 专用下载脚本，
一次性下载所有课程的大文件。

用法:
    python utils/download-all.py
"""

import os
import sys
import glob
import subprocess

# 本脚本所在目录（utils/）
UTILS_DIR = os.path.dirname(os.path.abspath(__file__))


def find_download_scripts() -> list:
    """扫描 utils/ 下所有 download-*.py（排除自身）。"""
    pattern = os.path.join(UTILS_DIR, "download-*.py")
    scripts = []
    for path in sorted(glob.glob(pattern)):
        name = os.path.basename(path)
        if name == "download-all.py":
            continue
        scripts.append(path)
    return scripts


def main() -> None:
    scripts = find_download_scripts()

    if not scripts:
        print("未找到任何 download-*.py 脚本。")
        return

    print(f"共发现 {len(scripts)} 个下载脚本，将按顺序运行：\n")
    for s in scripts:
        print(f"  - {os.path.basename(s)}")
    print()

    total_ok = 0
    total_fail = 0

    try:
        for script in scripts:
            name = os.path.basename(script)
            print(f"{'='*60}")
            print(f"▶ 正在运行: {name}")
            print(f"{'='*60}")

            result = subprocess.run(
                [sys.executable, script],
                capture_output=False,
            )

            if result.returncode == 0:
                total_ok += 1
                print(f"\n✓ {name} 完成\n")
            else:
                total_fail += 1
                print(f"\n✗ {name} 失败（返回码 {result.returncode}）\n")
    except KeyboardInterrupt:
        print(f"\n\n⚠ 用户中断，已取消下载。")
        sys.exit(1)

    print(f"{'='*60}")
    print(f"全部完成：成功 {total_ok}，失败 {total_fail}")
    if total_fail:
        sys.exit(1)


if __name__ == "__main__":
    main()