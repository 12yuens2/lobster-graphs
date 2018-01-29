
# Translate graphs to query graphs
python3 translate.py graphs/

# Move queries
mv *.querygfu queries

# Build graph database
./ggsxe -b -gfu db.gfu

# Query graph database
./ggsxe -f -gfu db.gfu --dir queries/
