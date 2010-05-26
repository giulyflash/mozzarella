cls
@echo off
path = %~dp0Python26;%~dp0\Python26\Scripts;%~dp0\Python26\Lib\site-packages\django\bin;%~dp0\Utilities;%~dp0\Utilities\Exemaker;%~dp0\Utilities\Npp;%~dp0\Utilities\Sqlite;%~dp0\Utilities\Mercurial;%~dp0\Utilities\Winmerge;%PATH%
set PYTHONPATH=%~dp0%\Python26;%~dp0%\Python26\Lib\site-packages
exemaker -i "%~dp0\Python26\python.exe" "%~dp0\Python26\Lib\site-packages\django\bin\django-admin.py" "%~dp0\Python26\Lib\site-packages\django\bin" 1>nul 2>&1
echo.
python manage.py shell
pause