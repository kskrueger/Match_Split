import cv2
import threading

filename = 'Media/2020Arkansas.mp4'

vid = cv2.VideoCapture(filename)
height, width = int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT)), int(vid.get(cv2.CAP_PROP_FRAME_WIDTH))
total = int(vid.get(cv2.CAP_PROP_FRAME_COUNT))
fps = int(vid.get(cv2.CAP_PROP_FPS))

# 2018
x_start_2018 = int(560 / 1280 * width)
x_end_2018 = int(738 / 1280 * width)
y_start_2018 = int(615 / 720 * height)
y_end_2018 = int(700 / 720 * height)

# 2019
x_start_2019 = int(246 / 640 * width)
x_end_2019 = int(395 / 640 * width)
y_start_2019 = int(296 / 360 * height)
y_end_2019 = int(312 / 360 * height)

# 2020
x_start_2020 = int(245 / 640 * width)
x_end_2020 = int(395 / 640 * width)
y_start_2020 = int(300 / 360 * height)
y_end_2020 = int(317 / 360 * height)

year = 2020

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


def check_frames(start_num, num):
    print("Start: " + str(start_num))
    input = cv2.VideoCapture(filename)

    i = start_num
    while i < start_num + num * fps:
        input.set(cv2.CAP_PROP_POS_FRAMES, i)
        _, frame = input.read()
        if frame is None:
            break

        if year == 2018:
            clock = frame[y_start_2018:y_end_2018, x_start_2018:x_end_2018]
        elif year == 2019:
            clock = frame[y_start_2019:y_end_2019, x_start_2019:x_end_2019]
        elif year == 2020:
            clock = frame[y_start_2020:y_end_2020, x_start_2020:x_end_2020]
        else:
            continue

        gray = cv2.cvtColor(clock, cv2.COLOR_BGR2GRAY)
        binary = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)[1]
        # cv2.imshow("Clock", clock)
        # cv2.imshow("Gray", gray)
        cv2.imshow("Binary", binary)

        # print(i)
        i = i + fps * 20  # 20 second chunks
        # cv2.waitKey(0)
    print("Done: " + str(i - fps * 20))


def new_check(start_num, num):
    print("Start: " + str(start_num))
    input = cv2.VideoCapture(filename)

    i = start_num
    last_area = None
    while i < start_num + num * fps:
        input.set(cv2.CAP_PROP_POS_FRAMES, i)
        _, frame = input.read()
        if frame is None:
            break

        if year == 2018:
            clock = frame[y_start_2018:y_end_2018, x_start_2018:x_end_2018]
        elif year == 2019:
            clock = frame[y_start_2019:y_end_2019, x_start_2019:x_end_2019]
        elif year == 2020:
            clock = frame[y_start_2020:y_end_2020, x_start_2020:x_end_2020]
        else:
            continue

        gray = cv2.cvtColor(clock, cv2.COLOR_BGR2GRAY)
        h, w = gray.shape
        sec5 = gray[0:h, w * 140 // 149:w]
        binary = cv2.inRange(sec5, 140, 210)
        area = cv2.countNonZero(binary)
        if last_area is None:
            last_area = area
        if area < last_area:
            print("Found: " + str(i))
            return
        last_area = area
        i = i + fps
    print("Done: " + str(i - fps))


# check_frames(123000, total)
increment = 30 + 8 + 120
start = 123000
end = 123000 + (increment * fps * 5)
threads = []
for a in range(start, end, increment * fps):
    t = threading.Thread(target=new_check, args=(a, increment))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print("Done!")
