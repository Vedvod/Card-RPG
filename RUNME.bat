ECHO OFF
cd "C:\Users\vedvo\Documents\GitHub\Keyless-Karlsson\"
py -m pip install -U pip
cd  "%CD%\Contents\" & rem #change dir to Contents
cls & echo Keyless Karlsson & PING localhost -n 2 >NUL & echo A wizard's quest in finding direction. & PING localhost -n 5 >NUL & rem #intro message
cls & py -m pip install -U "%CD%/modules/pygame-2.1.3.dev4-cp310-cp310-win_amd64.whl" "%CD%/modules/numpy-1.22.4-cp310-cp310-win_amd64.whl" & rem #This is for 64 bit
cls & py -m pip install -U "%CD%/modules/pygame-2.1.3.dev4-cp310-cp310-win32.whl" "%CD%/modules/numpy-1.22.4-cp310-cp310-win32.whl" & rem #This is for 32 bit
cd  "%CD%\Scripts\" & rem #This changes the working directory to the Scripts folder, where the python script is located. This means that the script runs as though run normally.
:pythonrun
	cls & python "%CD%\main.py" & pause & rem #This uses the 'python' command to run the script, replicating manually running the script, then pauses after the program ends
	set/p again="Run the script again? (y, yes or n, no) " 
	if /i "%again%" == "yes" goto pythonrun
	if /i "%again%" == "y" goto pythonrun
	echo Thanks for playing! & PING localhost -n 4 >NUL & rem #Thanks message and pause

REM #yes, this is indeed the same system used in the Great Bank ATM project!