.PHONY: all clean 

src             = csv2wave.py 
target-output	= csv2wave.exe
target_all      = $(target-output) 
all:$(target_all)

$(target-output):$(src)
	pyinstaller -F $<
	cp ./dist/$@ ./$@
clean:
	rm -rf $(target_all)
	rm -rf ./dist 
	rm -rf ./build
	rm -rf ./__pycache__