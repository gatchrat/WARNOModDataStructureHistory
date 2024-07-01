@echo off
for %%* in (.) do set CurrDirName=%%~nx*
..\..\WARNO.exe -headless -uploadmod "%CurrDirName%" CommonData:Clusters/Bootstrap/ClusterBootstrapUploadMod.ndf
..\Utils\Python\python.exe ..\Utils\Scripts\CreateModBackup.py -autoname
