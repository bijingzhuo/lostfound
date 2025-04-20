@echo off
echo Starting user_service...
start cmd /k "cd /d %~dp0user_service && uvicorn app:app --reload --port 8001"

echo Starting item_service...
start cmd /k "cd /d %~dp0item_service && uvicorn app:app --reload --port 8002"

echo Opening login page...
start "" "%~dp0frontend\login.html"

exit
