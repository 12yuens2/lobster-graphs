import csv
import os


# identification
ident_csv = open("identification.csv", "w")
ident_csv.write("Method,Model,Category,Precision,Recall,LabelThreshold,HistThreshold\n")
ident_csv.flush()

for ident_data in os.listdir("data/identification/"):
    label_threshold = ident_data[15:19]
    hist_threshold = ident_data[20:23]

    ident_file = open("data/identification/" + ident_data, "r")
    lines = ident_file.read().splitlines()[1:]

    for line in lines:
        ident_csv.write(line + "," + label_threshold + "," + hist_threshold + "\n")
    
ident_csv.flush()
ident_csv.close()
    
# labelling
labelling_csv = open("labelling.csv", "w")
labelling_csv.write("Method,Label,Model,Category,Precision,Recall,LabelThreshold,HistThreshold\n")
labelling_csv.flush()

for label_data in os.listdir("data/labelling/"):
    label_threshold = label_data[10:14]
    hist_threshold = label_data[15:18]

    label_file = open("data/labelling/" + label_data, "r")
    lines = label_file.read().splitlines()[1:]

    for line in lines:
        labelling_csv.write(line + "," + label_threshold + "," + hist_threshold + "\n")

labelling_csv.flush()
labelling_csv.close()
