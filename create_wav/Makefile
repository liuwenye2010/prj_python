.PHONY: all clean 


target-output	= create_wav.exe


target_all      = $(target-output) 

MSBUILDPATH:=$(subst $\\,/,$(subst $\",,$(shell cmd /c "build.cmd")))
$(info $(MSBUILDPATH))
MSBUILD:= $(MSBUILDPATH)/MSBuild.exe
$(info $(MSBUILD))


all:$(target_all)


$(target-output):create_wav.py 
	pyinstaller -F $<
	cp ./dist/create_wav.exe ./create_wav.exe


   
clean:
	rm -rf $(target_all)