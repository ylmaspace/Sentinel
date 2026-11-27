"""SQLite and UI repair regressions."""
from pathlib import Path


def test_theme_contains_real_qss_not_python_shell():
    theme = Path("src/sentinel/ui/styles/theme.qss")
    text = theme.read_text(encoding="utf-8")
    assert "QWidget" in text
    assert "Main application shell" not in text


def test_missing_ui_modules_exist():
    for path in ("src/sentinel/ui/main_window.py", "src/sentinel/ui/trust_view.py"):
        assert Path(path).is_file()
