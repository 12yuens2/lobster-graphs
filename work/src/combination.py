import cv2
import numpy as np

from common_matching import *
from common_cv import get_image_kps, get_point_tuple, cv2window


FNULL = open(os.devnull, "w")
       

label_params = [
    Label("body", 700),
    Label("arm", 200),
    Label("claw", 100),
    Label("head", 200),
    Label("tail", 320),
    Label("back", 200)
]

# Remove old queries
subprocess.run(["rm", "-f", "../queries/*"])

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


'''
good_permutations = []
with open("matches", "r") as match_file:
    current_id = -1
    for line in match_file:
        graph_id = int(line.split(":")[0])

        if not graph_id == current_id:
            good_permutations.append(permutations[graph_id])
            current_id = graph_id
'''

print("get matches")
good_matches = list(set(get_matches(permutations, "graphs/complete/")))

    
print(good_matches)
print(str(len(good_matches)))

print(type(good_matches[0]))

# draw lines and labels
image = cv2.imread("imgs/dither/IMG_1380.JPG")
y = 0
for match in good_matches:
    for t1,t2 in zip(list(match)[:-1], list(match)[1:]):
        image = cv2.drawKeypoints(image, [t1[0], t2[0]], image, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        cv2.line(image, get_point_tuple(t1[0]), get_point_tuple(t2[0]), (255,0,0), thickness=3)
        cv2.putText(image, str(t1[1]), tuple(map(sum, zip(get_point_tuple(t1[0]), (0,y)))), 1, 1, (0,0,255), 2, cv2.LINE_AA)
        y += 4
        cv2.putText(image, str(t2[1]), tuple(map(sum, zip(get_point_tuple(t2[0]), (0,y)))), 1, 1, (0,0,255), 2, cv2.LINE_AA)
        print(str(t1) + " " + str(t2))
        y += 4

cv2window("test", image)
cv2.waitKey(0)
cv2.destroyAllWindows()

cv2.imwrite("test.jpg", image)
