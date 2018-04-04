import csv
import os

from decimal import Decimal


# identification
ident_csv = open("identification.csv", "w")
ident_csv.write("Method,Model,Category,Precision,Recall,F1,LabelThreshold,HistThreshold\n")
ident_csv.flush()

for ident_data in os.listdir("data/identification/"):
    label_threshold = ident_data[15:19]
    hist_threshold = ident_data[20:23]

    if "H0.3" in ident_data or "H0.5" in ident_data or "H0.7" in ident_data or "H0.9" in ident_data:
        ident_file = open("data/identification/" + ident_data, "r")
        lines = ident_file.read().splitlines()[1:]

        for line in lines:
            vals = line.split(",")

            precision = round(Decimal(float(vals[3])), 3)
            recall = round(Decimal(float(vals[4])), 3)
            f1 = "0"
            if precision +  recall > 0:
                f1 = str(2 * precision * recall / (precision + recall))
            
            vals[3] = str(round(Decimal(float(vals[3])), 3))
            vals[4] = str(round(Decimal(float(vals[4])), 3))
            line = ",".join(vals)

            ident_csv.write(line + "," + f1 + "," + label_threshold + "," + hist_threshold + "\n")
    
ident_csv.flush()
ident_csv.close()
    
# labelling
labelling_csv = open("labelling.csv", "w")
labelling_csv.write("Method,Label,Model,Category,Precision,Recall,F1,LabelThreshold,HistThreshold\n")
labelling_csv.flush()

for label_data in os.listdir("data/labelling/"):
    label_threshold = label_data[10:14]
    hist_threshold = label_data[15:18]

    if "H0.3" in label_data or "H0.5" in label_data or "H0.7" in label_data or "H0.9" in label_data:
        label_file = open("data/labelling/" + label_data, "r")
        lines = label_file.read().splitlines()[1:]

        for line in lines:
            vals = line.split(",")

            precision = round(Decimal(float(vals[4])), 3)
            recall = round(Decimal(float(vals[5])), 3)
            f1 = "0"
            if precision + recall > 0:
                f1 = str(2 * precision * recall / (precision + recall))
            
            vals[4] = str(round(Decimal(float(vals[4])), 3))
            vals[5] = str(round(Decimal(float(vals[5])), 3))
            line = ",".join(vals)
            labelling_csv.write(line + "," + f1 + "," + label_threshold + "," + hist_threshold + "\n")

labelling_csv.flush()
labelling_csv.close()
