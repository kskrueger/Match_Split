import cv2

filename = 'Media/2019Test.mp4'

inp = cv2.VideoCapture(filename)
total = int(inp.get(cv2.CAP_PROP_FRAME_COUNT))
fps = int(inp.get(cv2.CAP_PROP_FPS))


def check_frame(start_num, num):
    input = cv2.VideoCapture(filename)
    height, width = int(input.get(cv2.CAP_PROP_FRAME_HEIGHT)), int(input.get(cv2.CAP_PROP_FRAME_WIDTH))
    fps = int(input.get(cv2.CAP_PROP_FPS))

    i = start_num
    while i < start_num + num * fps:
        input.set(cv2.CAP_PROP_POS_FRAMES, i)
        _, frame = input.read()
        if frame is None:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        binary = cv2.threshold(gray, 220, 255, cv2.THRESH_BINARY)[1]
        binary2 = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)[1]
        cv2.bitwise_and(binary, binary2, binary)
        cv2.imshow("Gray", gray)
        cv2.imshow("Binary", binary)
        cv2.imshow("Binary2", binary2)
        cv2.waitKey(0)

        se_h = cv2.getStructuringElement(cv2.MORPH_RECT, (width, 1))
        e1 = cv2.erode(binary, se_h)
        horz = cv2.dilate(e1, se_h)

        contours, _ = cv2.findContours(horz, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[-2:]
        top_line_y = height
        low_line_y = 0
        for cont in contours:
            _, y, _, _ = cv2.boundingRect(cont)
            if y < top_line_y:
                top_line_y = y
            if y > low_line_y:
                low_line_y = y
        if top_line_y > low_line_y:
            continue
        scorebox = frame[top_line_y:low_line_y, 0:width - 1]
        binary3 = cv2.threshold(gray, 60, 255, cv2.THRESH_BINARY_INV)[1]
        timebox_area = binary3[low_line_y:low_line_y + (low_line_y - top_line_y), width * 1 // 3:width * 2 // 3]

        se_h2 = cv2.getStructuringElement(cv2.MORPH_RECT, (width // 6, 1))
        e2 = cv2.erode(timebox_area, se_h2)
        horz2 = cv2.dilate(e2, se_h2)

        contours2, _ = cv2.findContours(horz2, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[-2:]
        top_time_y = height
        low_time_y = 0
        for cont in contours2:
            _, y, _, _ = cv2.boundingRect(cont)
            if y < top_time_y:
                top_time_y = y
            if y > low_time_y:
                low_time_y = y
        if top_time_y > low_time_y:
            continue
        se_v = cv2.getStructuringElement(cv2.MORPH_RECT, (1, (low_time_y - top_time_y)))
        e3 = cv2.erode(timebox_area, se_v)
        vert = cv2.dilate(e3, se_v)

        contours3, _ = cv2.findContours(vert, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[-2:]
        left_time_x = width - 1
        right_time_x = 0
        for cont in contours3:
            x, _, _, _ = cv2.boundingRect(cont)
            if x < left_time_x:
                left_time_x = x
            if x > right_time_x:
                right_time_x = x
        if left_time_x > right_time_x:
            continue
        timebox = frame[low_line_y + top_time_y:low_line_y + low_time_y,
                  width * 1 // 3 + left_time_x:width * 1 // 3 + right_time_x]
        cv2.imshow("Timebox", timebox)

        print(i)
        i = i + fps
        cv2.waitKey(0)


check_frame(0,1)


import threading

increment = 5
threads = []
for a in range(0, total, increment*fps):
    t = threading.Thread(target=check_frame, args=(a, increment))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print("Done!")
