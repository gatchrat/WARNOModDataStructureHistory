@echo off
for %%* in (.) do set CurrDirName=%%~nx*
..\..\WARNO.exe -headless -datapackonly -generatemod "Mods/%CurrDirName%/" CommonData:Clusters/Bootstrap/ClusterBootstrapGeneration.ndf
