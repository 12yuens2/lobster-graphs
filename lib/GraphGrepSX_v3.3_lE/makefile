ggsxe: GraphGrepSXConsole.o
	cd vflib2; make
	g++ -w -o ggsxe GraphGrepSXConsole.o -L./vflib2/lib -lvf -lstdc++ -lm -O3 -pthread -std=c++0x
GraphGrepSXConsole.o: GraphGrepSXConsole.cpp 
	g++ -w -c -O3 -I./vflib2/include -I ./GGSXLib GraphGrepSXConsole.cpp

clean:
	rm ggsxe
	cd vflib2; make clean
