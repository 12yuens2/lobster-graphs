python3 translate.py graphs/
mv *.querygfu queries
./ggsxe -b -gfu output.gfu
./ggsxe -f -gfu output.gfu --dir queries/
