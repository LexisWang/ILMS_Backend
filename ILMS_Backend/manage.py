#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ILMS_Backend.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


def crontab_task():
    """
        分  时  日   月  周
        *   *   *   *   *
        1   *   *   *   * (表示的是每个小时的第一分钟)
        */1 *   *   *   * (每分钟执行一次)
        0   2   *   *   * (表示每天的 02：00：00 执行一次)
    """

    # 项目开启时添加定时任务
    # 1.获取要执行的 任务文件 路径
    run_task_file_path = './crontab/invalid_file_clear.py'
    # 2.获取当前 python 解释器的路径
    python_path = sys.executable
    # 3.创建 crontab 任务的 命令文件 并写入
    task_file_path = './crontab/my_task.conf'
    with open(task_file_path, mode='w', encoding='utf-8') as f:
        f.write(f'0 2 * * * {python_path} {os.path.abspath(run_task_file_path)}\n')

    os.popen(f'crontab {os.path.abspath(task_file_path)}')


if __name__ == '__main__':
    # crontab_task()
    main()
