export CPPFLAGS="-I/usr/local/opt/llvm/include -fopenmp"
echo $CPPFLAGS

export LDFLAGS="-L/usr/local/opt/llvm/lib"
echo $LDFLAGS

mkdir build
cd build
cmake .. -DCMAKE_TOOLCHAIN_FILE=../toolchain.txt
make
