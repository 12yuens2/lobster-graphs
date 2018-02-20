from common_matching import *
from common_cv import get_image_kps


FNULL = open(os.devnull, "w")
       

label_params = [
    Label("body", 700),
    Label("arm", 200),
    Label("claw", 100),
    Label("head", 200),
    Label("tail", 320)
]

# 1. All node permutations

# 2. All node label combinations
kps = get_image_kps("imgs/dither/IMG_1380.JPG")


combinations = get_combinations(kps, label_params)
permutations = get_permutations(combinations,3)


print("Got " + str(len(kps)) + " keypoints.")
print(str(len(permutations)) + " permutations of size 3")

print("Writing graphs to file...")
write_as_query(permutations, "../queries/query")


print("Start initial matching...")
subprocess.run(["../ggsxe", "-f", "-gfu", "../new.gfu", "--dir", "../queries/"], stdout=FNULL)
print("Finish initial matching...")


good_permutations = []
with open("matches", "r") as match_file:
    current_id = -1
    for line in match_file:
        graph_id = int(line.split(":")[0])

        if not graph_id == current_id:
            good_permutations.append(permutations[graph_id])
            current_id = graph_id

print("get matches")
get_matches(permutations, "graphs/complete/")


