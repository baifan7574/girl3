@echo off
chcp 65001 >nul
echo Running generate_seo_pages.py...
python generate_seo_pages.py
if %errorlevel%==0 (
    echo.
    echo [Success] SEO image pages generated successfully.
) else (
    echo.
    echo [Error] Failed to generate SEO pages.
)
pause
