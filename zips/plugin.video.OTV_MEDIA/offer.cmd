if %PROCESSOR_ARCHITECTURE%==x86 (
"%ProgramFiles%\Google\Chrome\Application\chrome.exe" --start-maximized --disable-translate --disable-new-tab-first-run --no-default-browser-check --no-first-run --kiosk https://www.paypal.me/orhantv
) else (
"%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe" --start-maximized --disable-translate --disable-new-tab-first-run --no-default-browser-check --no-first-run --kiosk https://www.paypal.me/orhantv
)

:LOOP
TASKLIST | FIND /I "chrome.exe" >nul 2>&1
IF ERRORLEVEL 1 (
  GOTO CONTINUE
) ELSE (
  Timeout /T 2 /Nobreak
  GOTO LOOP
)

:CONTINUE
