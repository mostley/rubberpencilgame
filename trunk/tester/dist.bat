
REM Build Exe
python setup.py py2exe

REM Copy resources
copy /Y img\*.png dist\img\
copy /Y maps\*.map dist\maps\
copy /Y F:\WINDOWS\system32\GLU32.DLL dist\
copy /Y F:\WINDOWS\system32\OPENGL32.DLL dist\
copy /Y F:\WINDOWS\system32\msvcrt.dll dist\

REM pack Release
copy /Y zip.exe dist
cd dist
zip -R release.zip * -x zip.exe
copy /Y release.zip ..
cd ..

pause