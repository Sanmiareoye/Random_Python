import cv2
import numpy as np

img = cv2.imread("assets/soccer.png", 0)
template = cv2.imread("assets/shoe.png", 0)
h, w = template.shape

# slight different ways  of performing template matching and use the one that performs th best.
methods = [
    cv2.TM_CCOEFF,
    cv2.TM_CCOEFF_NORMED,
    cv2.TM_CCORR,
    cv2.TM_CCORR_NORMED,
    cv2.TM_SQDIFF,
    cv2.TM_SQDIFF_NORMED,
]

for method in methods:
    img2 = img.copy()

    result = cv2.matchTemplate(img2, template, method)
    # (W -w + 1, H - h+1)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    print(min_loc, max_loc)
    if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
        location = min_loc
    else:
        location = max_loc

    bottom_right = (location[0] + w, location[1] + h)
    cv2.rectangle(img2, location, bottom_right, 255, 5)

    cv2.imshow("Match", img2)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
