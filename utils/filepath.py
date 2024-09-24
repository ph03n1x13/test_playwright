from pathlib import Path

class FilePath:

    def screenshot_path(self, file_name: str):
        """Get the full path for a screenshot file, cross-platform."""
        current_dir = Path.cwd()
        parent_dir = current_dir.parent
        file_path = parent_dir / 'test_playwright' / 'screenshots' / file_name
        return file_path

    def screenshot_dir_path(self):
        """Get the directory path for screenshots and create it if it doesn't exist."""
        current_dir = Path.cwd()
        parent_dir = current_dir.parent
        screenshots_dir = parent_dir / 'test_playwright' / 'screenshots'
        screenshots_dir.mkdir(parents=True, exist_ok=True)  # Create directory if it doesn't exist
        return screenshots_dir

    def report_dir_path(self):
        """Get the directory path for reports and create it if it doesn't exist."""
        current_dir = Path.cwd()
        parent_dir = current_dir.parent
        report_dir = parent_dir / 'test_playwright' / 'reports'
        report_dir.mkdir(parents=True, exist_ok=True)  # Create directory if it doesn't exist
        return report_dir