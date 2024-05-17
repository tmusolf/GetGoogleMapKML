@echo off
echo.
echo Converts google my maps into OSMAnd GPX files.
echo.
echo Reads in a supplied file containing a google map name and it's corresponding ID value (mid=xxxx)
echo The google map name doesn't have to be the actual name it's the string you want used for the folder.
echo.
setlocal EnableDelayedExpansion
set KMLtoGPX_PROGRAM="U:\Projects\Computer Projects\PC Software\KMLtoOSMAndGPXTracks\KMLtoOSMAndGPXTracks.py"
set MAPtoKML_PROGRAM="U:\Projects\Computer Projects\PC Software\BAT\GoogleMapsToOSMAnd\GetMapKML.py"
:getinput
set /p infile= "Enter filename containing one comma separated pair of values for each line (<name>,<mapID>): "

if exist %infile% goto execute 
echo.
echo ***Missing input file: %infile% ***
echo.
goto end
:execute

:: Get the current date in YYYY-MM-DD format
for /f "tokens=2 delims==" %%a in ('wmic OS Get localdatetime /value') do set "dt=%%a"

set "CurrentDate=%dt:~0,4%-%dt:~4,2%-%dt:~6,2%"
echo Current date: %CurrentDate%
set /a count=0
set /a errorCount=0

:: Read the file containing infile and outfile names
:: Tokens split on comma, first token put in %%A and second in %%B
for /f "eol=# tokens=1,2 delims=," %%A in (%infile%) do (
	:: Execute the batch file with infile, outfile, and current date as arguments
	set /a count+=1
	set "outputfolder=%%A-%CurrentDate%"
	set "kmlfile=!outputfolder!.kml"
	echo =========================================================================================
	echo Processing map #!count! %%A
	::echo count: !count! A: %%A outputfolder: !outputfolder!  mapid: %%B  kmlfile: !kmlfile!
	py %MAPtoKML_PROGRAM% %%B "!kmlfile!"
	if !ERRORLEVEL! EQU 0 (
		py %KMLtoGPX_PROGRAM% "!kmlfile!" -w 12
		if !ERRORLEVEL! EQU 0 (
			echo Delete file !kmlfile!
			del "!kmlfile!"
		) else (set /a errorCount+=1)
	) else (set /a errorCount+=1)
	echo.
)
echo Processed %count% maps. Error count: %errorCount%
:end
endlocal
pause

