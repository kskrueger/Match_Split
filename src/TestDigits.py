import cv2

# define the dictionary of digit segments so we can identify
# each digit on the thermostat
DIGITS_LOOKUP = {
    (1, 1, 1, 0, 1, 1, 1): 0,
    (0, 0, 1, 0, 0, 1, 0): 1,
    (1, 0, 1, 1, 1, 1, 0): 2,
    (1, 0, 1, 1, 0, 1, 1): 3,
    (0, 1, 1, 1, 0, 1, 0): 4,
    (1, 1, 0, 1, 0, 1, 1): 5,
    (1, 1, 0, 1, 1, 1, 1): 6,
    (1, 0, 1, 0, 0, 1, 0): 7,
    (1, 1, 1, 1, 1, 1, 1): 8,
    (1, 1, 1, 1, 0, 1, 1): 9
}

clock = cv2.imread('/Users/kskrueger/Match_Split/2019Example copy.png')

gray = cv2.cvtColor(clock, cv2.COLOR_BGR2GRAY)
binary = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)[1]
contours, _ = cv2.findContours(binary, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[-2:]
cv2.imshow("Binary", binary)
cv2.drawContours(clock, contours, -1, (255, 0, 0))
cv2.imshow("Contours", clock)

contours, _ = cv2.findContours(binary, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[-2:]
digitCnts = []
# loop over the digit area candidates
for c in contours:
    # compute the bounding box of the contour
    (x, y, w, h) = cv2.boundingRect(c)
    # if the contour is sufficiently large, it must be a digit
    if w < 2*h:
        digitCnts.append(c)

digitCnts = sorted(digitCnts, key=lambda ctr: cv2.boundingRect(ctr)[0])
digits = []
# loop over each of the digits
for c in digitCnts:
    # extract the digit ROI
    (x, y, w, h) = cv2.boundingRect(c)
    roi = binary[y:y + h, x-4:x + w]
    cv2.imshow('Roi', roi)
    cv2.waitKey(0)
    # compute the width and height of each of the 7 segments
    # we are going to examine
    # (roiH, roiW) = roi.shape
    # (dW, dH) = (int(roiW * 0.25), int(roiH * 0.15))
    # dHC = int(roiH //3)
    # define the set of 7 segments
    segments = [
        ((0, 0), (w, h//4)),  # top
        ((0, 0), (w//3, h//2)),  # top-left
        ((2*w//3, 0), (w, h//2)),  # top-right
        ((0, (h//3)), (w, (2*h//3))),  # center
        ((0, h//2), (w//3, h)),  # bottom-left
        ((2*w//3, h//2), (w, h)),  # bottom-right
        ((0, 3*h//4), (w, h))  # bottom
    ]
    on = [0] * len(segments)

    for (i, ((xA, yA), (xB, yB))) in enumerate(segments):
        # extract the segment ROI, count the total number of
        # thresholded pixels in the segment, and then compute
        # the area of the segment
        segROI = roi[yA:yB, xA:xB]
        cv2.imshow("Segroi", segROI)
        cv2.waitKey(0)
        total = cv2.countNonZero(segROI)
        area = (xB - xA) * (yB - yA)
        # if the total number of non-zero pixels is greater than
        # 50% of the area, mark the segment as "on"
        if area > 0 and total / float(area) > 0.5:
            on[i] = 1
        # lookup the digit and draw it on the image
    digit = DIGITS_LOOKUP[tuple(on)]
    digits.append(digit)
    print(digits)