.PHONY: all clean 

src_icon        = gui.ico
src             = csv2wave.py 
target-output	= csv2wave.exe
target_all      = $(target-output) 
all:$(target_all)

$(target-output):$(src) $(src_icon)
	pyinstaller -i $(src_icon) -F $<
	cp ./dist/$@ ./$@
clean:
	rm -rf $(target_all)
	rm -rf ./dist 
	rm -rf ./build
	rm -rf ./__pycache__