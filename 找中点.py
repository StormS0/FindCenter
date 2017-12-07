import cv2
import numpy as np
from matplotlib import pyplot as plt

def distance(a,b):
    d = (b[1]-a[1])*(b[1]-a[1])+(b[0]-a[0])*(b[0]-a[0])
    print (a,b,d)
    return d
img = cv2.imread("1.jpg")

b,g,r = cv2.split(img)
ret2,th2 = cv2.threshold(b,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(3, 3))
th2 = cv2.erode(th2, kernel, iterations=1)
th2 = cv2.dilate(th2, kernel, iterations=2)
cv2.imshow("th2",th2)

cv2.waitKey(0)
gray = np.float32(th2)

corners = cv2.goodFeaturesToTrack(gray, maxCorners=10, qualityLevel=0.5, minDistance=10)

# 返回的结果是 [[ 311., 250.]] 两层括号的数组。
corners = np.int0(corners)
box = []
for i in corners:
    x, y = i.ravel()
    cv2.circle(img, (x, y), 3, 255, -1)
    box.append((x, y))
box.sort()

dis1 = 0
break_n = 0
box_n = 0
k = -1
for  i in range(len(box)):
    dist = distance(box[k],box[i])
    if dist - dis1 < 5000:
        dis1 = dist
        break_n = break_n + 1
    else:
        dis1 = dist
        break_n =0
    if break_n == 2:
        box_n = i
        print("中值",i)
        break
    k = k+1
print(box[box_n -1 :box_n+3])
(x1,y2),radius = cv2.minEnclosingCircle(np.array([box[box_n-1 :box_n+3]]))
cv2.circle(img, (int(x1), int(y2)), 3, (0,0,255), -1)
plt.imshow(img), plt.show()
