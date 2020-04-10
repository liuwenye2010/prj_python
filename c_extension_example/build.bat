rm -rf build *.pyd
python setup.py build_ext --inplace
python setup.py install
python test.py
pause