# -*- coding: utf-8 -*-
# @Function: 项目创建脚手架工具

import io
import os
import shutil
import subprocess
import sys
from pathlib import Path

# 强制 UTF-8 输出
os.environ["PYTHONIOENCODING"] = "utf-8"
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")

TEMPLATE_DIR = Path(__file__).resolve().parent.parent

# 排除的文件和目录
EXCLUDE = {
    ".git",
    "__pycache__",
    ".venv",
    "venv",
    "node_modules",
    "reports",
    ".env",
    "*.pyc",
    ".DS_Store",
    "Thumbs.db",
    "private",
}


def validate_name(name: str) -> bool:
    """验证项目名称"""
    if not name:
        return False
    if not name.replace("-", "").replace("_", "").isalnum():
        return False
    return True


def get_project_info() -> tuple:
    """获取项目信息"""
    print("AI 项目创建向导")
    print("=" * 20)

    # 获取项目名称
    while True:
        name = input("\n请输入项目名称: ").strip()
        if validate_name(name):
            break
        print("项目名称无效，只能包含字母、数字、下划线和连字符")

    # 获取项目描述
    description = input("请输入项目描述（直接回车跳过）: ").strip()

    return name, description


def confirm_creation(name: str, description: str) -> bool:
    """确认创建"""
    print(f"\n项目名称: {name}")
    print(f"项目描述: {description or '未设置'}")

    confirm = input("\n确认创建项目？[Y/n]: ").strip().lower()
    return confirm in ("", "y", "yes")


def copy_template(project_dir: Path) -> None:
    """复制模板文件"""
    ignore = shutil.ignore_patterns(*EXCLUDE)
    shutil.copytree(TEMPLATE_DIR, project_dir, ignore=ignore)


def replace_project_name(project_dir: Path, name: str, description: str) -> None:
    """替换项目名称"""
    replacements = {
        "AI-XiangMuMoBan": name,
        "AI 项目模板 — 通用的 AI 辅助开发项目起点。": description or "AI 辅助开发项目",
    }

    for file_path in project_dir.rglob("*.md"):
        try:
            content = file_path.read_text(encoding="utf-8")
            for old, new in replacements.items():
                content = content.replace(old, new)
            file_path.write_text(content, encoding="utf-8")
        except Exception:
            pass


def init_git(project_dir: Path) -> bool:
    """初始化 Git 仓库"""
    try:
        subprocess.run(["git", "init"], cwd=project_dir, check=True, capture_output=True)
        subprocess.run(["git", "add", "."], cwd=project_dir, check=True, capture_output=True)
        subprocess.run(
            ["git", "commit", "-m", "feat: 初始化项目"],
            cwd=project_dir,
            check=True,
            capture_output=True,
        )
        return True
    except Exception as e:
        print(f"Git 初始化失败: {e}")
        return False


def print_report(name: str, project_dir: Path, git_ok: bool) -> None:
    """打印创建报告"""
    file_count = sum(1 for _ in project_dir.rglob("*") if _.is_file())

    print("\n" + "=" * 20)
    print("项目创建成功！")
    print("=" * 20)
    print(f"项目名称: {name}")
    print(f"项目路径: {project_dir}")
    print(f"文件数量: {file_count} 个")
    print(f"Git 状态: {'已初始化' if git_ok else '初始化失败'}")
    print("\n下一步:")
    print(f"  1. cd {name}")
    print("  2. make setup          # 安装依赖")
    print("  3. 开始开发！")


def main() -> int:
    """主函数"""
    # 检查命令行参数
    if len(sys.argv) > 1:
        name = sys.argv[1]
        description = ""
        if not validate_name(name):
            print(f"项目名称无效: {name}")
            return 1
        # 命令行模式自动确认
        print(f"项目名称: {name}")
        print(f"项目描述: {description or '未设置'}")
    else:
        name, description = get_project_info()
        if not confirm_creation(name, description):
            print("已取消创建")
            return 0

    project_dir = Path.cwd() / name

    if project_dir.exists():
        print(f"项目目录已存在: {project_dir}")
        return 1

    print("\n正在创建项目...")

    # 复制模板
    copy_template(project_dir)
    print("复制模板文件")

    # 替换项目名称
    replace_project_name(project_dir, name, description)
    print("替换项目名称")

    # 初始化 Git
    git_ok = init_git(project_dir)
    if git_ok:
        print("初始化 Git 仓库")

    # 打印报告
    print_report(name, project_dir, git_ok)

    return 0


if __name__ == "__main__":
    sys.exit(main())
