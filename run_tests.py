import pytest
import datetime
import webbrowser
import os

timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
report_file = f"reports/report_{timestamp}.html"

os.makedirs("reports", exist_ok=True)

pytest.main([
    "--html", report_file,
    "--self-contained-html",
    '--ignore=tests/test_login_swaglabPOM.py',  # ✅ ข้ามไฟล์นี้
    '--ignore=tests/test_login_swaglabPOMDDT.py',  # ✅ ข้ามอีกไฟล์
])

webbrowser.open(f"file://{os.path.abspath(report_file)}")
