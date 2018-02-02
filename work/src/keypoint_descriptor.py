import cv2
import numpy as np

image = cv2.imread("imgs/close_lobster.JPG")
h, w = image.shape[:2]
image = np.float32(image) / 255.0
#image = cv2.resize(image, (int(1.5*w), int(1.5*h)), interpolation=cv2.INTER_CUBIC)

gx = cv2.Sobel(image, cv2.CV_32F, 1, 0, ksize=1)
gy = cv2.Sobel(image, cv2.CV_32F, 0, 1, ksize=1)

magnitude, angle = cv2.cartToPolar(gx, gy, angleInDegrees=True)

print(type(magnitude))
print(type(angle))

cv2.imshow("mag", magnitude)
cv2.imshow("angle", angle)
cv2.imshow("gx", gx)
cv2.imshow("gy", gy)
cv2.waitKey(0)
cv2.destroyAllWindows()

print(magnitude.shape)
