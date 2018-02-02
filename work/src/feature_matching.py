import cv2
import numpy as np

def preprocess(image, scale, gray=True):
    height, width = image.shape[:2]
    
    # Resize
    processed_image = cv2.resize(image, (int(scale*width), int(scale*height)), interpolation=cv2.INTER_CUBIC)
    
    # Grayscale
    if gray:
        processed_image = cv2.cvtColor(processed_image, cv2.COLOR_BGR2GRAY)

    return processed_image 


def flann_matcher():
    index_params = dict(algorithm = 0, trees = 5)
    search_params = dict(checks = 50)

    return cv2.FlannBasedMatcher(index_params, search_params)

query_image = cv2.imread("imgs/claw.JPG")
train_image = preprocess(cv2.imread("imgs/IMG_1380.JPG"), 1, gray=False)

#orb = cv2.ORB_create()
orb = cv2.xfeatures2d.SIFT_create()
#orb = cv2.SIFT()

kp1, des1 = orb.detectAndCompute(query_image, None)
kp2, des2 = orb.detectAndCompute(train_image, None)



#bf_matcher = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

flann = flann_matcher()
matches = flann.knnMatch(des1, des2, k=2)

#matches = bf_matcher.match(des1, des2)
#matches = sorted(matches, key=lambda x:x.distance)

#image = train_image.copy()
#image = cv2.drawMatches(query_image, kp1, train_image, kp2, matches[:20], image, flags=2)

print("Matches found " + str(len(matches)))

good_matches = []
for m,n in matches:
    if m.distance < 0.95*n.distance:
        good_matches.append(m)


print("Good matches found: " + str(len(good_matches)))

if len(good_matches) > 1:
    src_pts = np.float32([kp1[m.queryIdx].pt for m in good_matches]).reshape(-1,1,2)
    dst_pts = np.float32([kp2[m.trainIdx].pt for m in good_matches]).reshape(-1,1,2)

    M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
    matchesMask = mask.ravel().tolist()

    h,w = query_image.shape[:2]
    pts = np.float32([[0,0], [0,h-1], [w-1,h-1], [w-1,0]]).reshape(-1,1,2)
    dst = cv2.perspectiveTransform(pts, M)

    train_image = cv2.polylines(train_image, [np.int32(dst)], True, 255, 3, cv2.LINE_AA)

draw_params = dict(matchColor = (0, 255, 0),
                   singlePointColor = None,
                   matchesMask = matchesMask,
                   flags = 2)

img3 = cv2.drawMatches(query_image, kp1, train_image, kp2, good_matches, None, **draw_params)

cv2.namedWindow("Matches", cv2.WINDOW_NORMAL)
cv2.imshow("Matches", img3)
cv2.waitKey(0)
cv2.destroyAllWindows()
    


'''
cv2.imshow("Matches", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
'''
