import os
from pathlib import Path


class FilePath:

    def screenshot_path(self, file_name: str):
        current_dir = Path.cwd()
        parent_dir = current_dir.parent
        file_path = os.path.join(parent_dir, 'test_playwright/screenshots', file_name)
        return file_path

    def screenshot_dir_path(self):
        current_dir = Path.cwd()
        parent_dir = current_dir.parent
        screenshots_dir = os.path.join(parent_dir, 'test_playwright/screenshots')
        if not os.path.exists(screenshots_dir):
            os.makedirs(screenshots_dir)
        return screenshots_dir


    def report_dir_path(self):
        current_dir = Path.cwd()
        parent_dir = current_dir.parent
        report_dir = os.path.join(parent_dir, 'test_playwright/reports')
        if not os.path.exists(report_dir):
            os.makedirs(report_dir)
        return report_dir