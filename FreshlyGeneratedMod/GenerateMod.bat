@echo off
for %%* in (.) do set CurrDirName=%%~nx*
..\..\WARNO.exe -headless -generatemod "Mods/%CurrDirName%/" CommonData:Clusters/Bootstrap/ClusterBootstrapGeneration.ndf
if %ERRORLEVEL% EQU 0 ..\..\Tools\AssetCooker.exe -e CoreCatalog.cat -g ./Gen/ --common-data ./CommonData/ --game-data ./GameData/
if %ERRORLEVEL% EQU 0 ..\Utils\Python\python.exe ..\Utils\Scripts\CopyModGenData.py WARNO %CurrDirName%
PAUSE
