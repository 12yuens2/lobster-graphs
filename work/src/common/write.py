import cv2

from common.cv import get_point_tuple

# Type imports
from cv2 import KeyPoint
from typing import List, Tuple, Any
from classes.matching import KeyLabel
from classes.graphs import Graph

# Path for lobster images to match on
PATH = "imgs/lobsters/"

# Write permutations as .querygfu
def permutations_as_query(permutations: List[Tuple[KeyLabel, ...]],
                   permutation_size: int,
                   filepath: str) -> None:

    f = open(filepath + ".querygfu", "w")
    for i in range(len(permutations)):
        permutation = permutations[i]

        # Graph header
        f.write("#graph" + str(i) + "\n")

        f.write(str(permutation_size) + "\n")

        for node in permutation:
            label = node[1].name
            f.write(str(label) + "\n")

        f.write(str(permutation_size - 1) + "\n")
        for x,y in zip(range(permutation_size - 1), range(1, permutation_size)):
            f.write(str(x) + " " + str(y) + "\n")

        f.flush()
    f.close()

# Write list of opencv keypoints as .gdf format
def kps_as_gdf(kps: List[KeyPoint],
               filename: str,
               filepath: str) -> None:

    f = open(filepath + filename, "w")

    # Node header definition
    f.write("nodedef> name VARCHAR,label VARCHAR,width DOUBLE,height DOUBLE,x DOUBLE,y DOUBLE,color VARCHAR\n")

    # Write nodes
    i = 1
    px,py = (0,0)
    for kp in kps:
        (x,y) = get_point_tuple(kp)
        #radius = kp.size/2

        # Do not write duplicate keypoints
        #if not (x,y) == (px,py):
        f.write(str(i)+",\"\"," +
                str(kp.size)+"," +
                str(kp.size)+"," +
                str(x) + "," + str(y) +
                ",'153,153,153'\n")
        i += 1

        (px,py) = (x,y)
        f.flush()
    
    f.close()


# Write opencv image to file
def write_image(image: Any, filename: str) -> None:
    cv2.imwrite(filename, image)


# Draw permutation triplets to onto image and write to file
def write_triplets(triplets: List[Tuple[KeyLabel, ...]],
                   image_file: str,
                   write_path: str) -> None:

    image = cv2.imread(PATH + image_file)
    
    for triplet in triplets:
        for n1,n2 in zip(list(triplet)[:-1], list(triplet)[1:]):
            image = cv2.drawKeypoints(image, [n1[0], n2[0]], image, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

            cv2.line(image, get_point_tuple(n1[0]), get_point_tuple(n2[0]), (255,0,0), thickness=3)
            cv2.putText(image, str(n1[1]), get_point_tuple(n1[0]), 1, 1, (0,0,255), 2, cv2.LINE_AA)
            cv2.putText(image, str(n2[1]), get_point_tuple(n2[0]), 1, 1, (0,0,255), 2, cv2.LINE_AA)

    cv2.imwrite(write_path + image_file, image)


# Draw and write keypoints to image
def write_keypoints(image_file: str, kps: List[cv2.KeyPoint]) -> None:
    image = cv2.imread(PATH + image_file)
    cv2.drawKeypoints(image, kps, image, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    cv2.imwrite("imgs/keypoints/" + image_file, image)


def write_graph(graph: Graph,
                image_name: str,
                image_path: str,
                write_path: str) -> None:

    image = cv2.imread(image_path + image_name)

    # Draw graph nodes
    image = cv2.drawKeypoints(image, [node.kp for node in graph.nodes], image, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

    # Draw graph edges
    for edge in graph.edges:
        n1_pos = tuple(map(int, edge.n1.pos))
        n2_pos = tuple(map(int, edge.n2.pos))
        cv2.line(image, n1_pos, n2_pos, (255,0,0), thickness=3)

        # Draw node labels
        cv2.putText(image, edge.n1.label, n1_pos, 1, 3, (0,0,255), 4, cv2.LINE_AA)
        cv2.putText(image, edge.n2.label, n2_pos, 1, 3, (0,0,255), 4, cv2.LINE_AA)

    cv2.imwrite(write_path + image_name, image)