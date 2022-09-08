import cv2 as cv
import numpy as np
from motor import Controller

controller = Controller()
camera = 0

value1 = 80
value2 = 60
saturation = 250
font = cv.FONT_HERSHEY_SIMPLEX
start_calibration = 0
contours_count = []
calibration_variable =[]
saturation_min = 500
calibration_reset = 0
last_rot_status = None
death_zone = 100
ball_dist_threshold = 100

def on_change1(input_1):
    global value1
    value1 = input_1
    print(value1)


def on_change2(input_2):
    global value2
    value2 = input_2
    print(value2)

video = cv.VideoCapture(camera)
has_target = False

while True:
    hass_ball = False
    calibration_reset += 1
    ret, frame = video.read()
    if ret == True:

        frame = cv.medianBlur(frame, 5)
        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
                #yellow ([15,104, 80])
            #Grün^^^ = np.array([50, saturation, 80])
            #grün = np.array([100, 255, 255])
        lower_yellow = np.array([40, 100, 80]) # TODO: Saturation
        upper_yellow = np.array([95, 255, 255])

        mask = cv.inRange(hsv, lower_yellow, upper_yellow)

        res = cv.bitwise_and(frame, frame, mask=mask)

        k = cv.waitKey(5) & 0xFF

        mask = cv.inRange(hsv, lower_yellow, upper_yellow)
        mask = cv.erode(mask, None, iterations=2)
        mask = cv.dilate(mask, None, iterations=2)

        contours, hierarchy = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        contours_list = []

        #Erkent den umriss mit der größten fläche und markiert diesen

        if len(contours) > 0:
            i = 0
            calibration_reset = 0

            for i in range(len(contours)):
                area =cv.contourArea(contours[i])
                contours_list.append(area)

            contours_list_backup = contours_list
            contours_list.sort()
            contours_found = False
            cnt = -1
            if len(contours_list) > 0:
                last_rot_status = None
                #print("length: " + str(len(contours_list)))
                while contours_found == False:
                    cnt += 1
                    if contours_list[len(contours_list)-1] == cv.contourArea(contours[cnt]):
                        contours_found = True


                cnt = contours[cnt]

                cv.drawContours(frame , [cnt], 0, (0,255,0), 3)
                
                cv.drawContours(res , [cnt], 0, (0,255,0), 3)
                (x, y), radius = cv.minEnclosingCircle(cnt)
                center = (int(x), int(y))
                cv.circle(frame, (int(x), int(y)), 5, (42, 46, 139), 3)
                frame_height, frame_width, _ = frame.shape
                frame_height_half = frame_height / 2
                frame_width_half = frame_width / 2


                if frame_height- ball_dist_threshold < int(y):
                    hass_ball = True

                if frame_width_half - death_zone > center[0] and hass_ball == False:
                    controller.slow_spin_l()
                    print("L")
                elif frame_width_half + death_zone < center[0] and hass_ball == False:
                    controller.slow_spin_r()
                    print("R")
                elif hass_ball == False:
                    controller.forward()
                    print("Forward")
        else:
            # find ball again
            if last_rot_status == None:
                last_rot_status = controller.get_status()

            if last_rot_status in ["spin_l", "turn_l", "slow_turn_l"]:
                controller.spin_l()
                print("L Balll")
            elif last_rot_status in ["spin_r", "turn_r", "slow_turn_r"]:
                controller.spin_r()
                print("R Ball")
            else:
                print("???")

                last_rot_status = None

        if hass_ball == True and ret == True:
            x = 0
            y = 0

            hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
            # yellow ([15,104, 80])
            # Grün^^^ = np.array([50, saturation, 80])
            # grün = np.array([100, 255, 255])
            lower_tor = np.array([130, 100, 80])  # TODO: Saturation
            upper_tor = np.array([140, 255, 255])

            mask2 = cv.inRange(hsv, lower_tor, upper_tor)

            res2 = cv.bitwise_and(frame, frame, mask=mask2)

            k = cv.waitKey(5) & 0xFF

            mask2 = cv.inRange(hsv, lower_tor, upper_tor)
            mask2 = cv.erode(mask2, None, iterations=2)
            mask2 = cv.dilate(mask2, None, iterations=2)
            contours = []
            contours, hierarchy = cv.findContours(mask2, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
            contours_list = []

            # Erkent den umriss mit der größten fläche und markiert diesen

            if len(contours) > 0:
                center_tor = []
                i = 0
                calibration_reset = 0

                for i in range(len(contours)):
                    area = cv.contourArea(contours[i])
                    contours_list.append(area)

                contours_list_backup = contours_list
                contours_list.sort()
                contours_found = False
                cnt = -1
                if len(contours_list) > 0:
                    last_rot_status = None
                    # print("length: " + str(len(contours_list)))
                    while contours_found == False:
                        cnt += 1
                        if contours_list[len(contours_list) - 1] == cv.contourArea(contours[cnt]):
                            contours_found = True

                    cnt = contours[cnt]

                    cv.drawContours(frame, [cnt], 0, (0, 255, 0), 3)

                    cv.drawContours(res2, [cnt], 0, (0, 255, 0), 3)
                    (ax, ay), radius = cv.minEnclosingCircle(cnt)
                    center_tor = (int(ax), int(ay))
                    cv.circle(frame, (int(ax), int(ay)), 5, (42, 46, 139), 3)
                    frame_height, frame_width, _ = frame.shape
                    frame_height_half = frame_height / 2
                    frame_width_half = frame_width / 2
                    center_to_center_distance = center_tor[0] - center[0]
                    if center_to_center_distance < 0:
                        center_to_center_distance = center_to_center_distance * -1
                    if frame_width_half - death_zone > center_tor[0]:
                        print("L")
                    elif frame_width_half + death_zone < center_tor[0]:

                        print("R")
                    else:
                        print("Forward")
                    if center_to_center_distance < 60:
                        print("kik")

                else:

                    if last_rot_status in ["spin_l", "turn_l", "slow_turn_l"]:

                        print("L Balll")
                    elif last_rot_status in ["spin_r", "turn_r", "slow_turn_r"]:
                        print("R Ball")
                    else:
                        print("???")
            cv.imshow('resuhaeg', res2)
            cv.waitKey(1)

        if start_calibration == 25:
            if len(contours) < 4 and saturation > 50:
                saturation -= 10
            if len(contours) > 4:
                saturation += 2
            if saturation < 50:
                saturation = 50

        if start_calibration < 24:
            calibration_variable.append(saturation)
            contours_count.append(len(contours))
            saturation -= 10
            start_calibration += 1
        if start_calibration == 24:
            start_calibration = 25
            for i in range(len(contours_count)):
                if contours_count[i] > 0 and contours_count[i] < 5 and calibration_variable[i]< saturation_min:
                    saturation_min = calibration_variable[i]
            saturation= saturation_min
        if calibration_reset > 70:
            start_calibration = 0
            calibration_reset = 0




        cv.line(frame, (0,frame_height-ball_dist_threshold), (frame_width,frame_height-ball_dist_threshold) , (140, 140, 199), 3)
        image = cv.putText(frame, str(saturation), (50, 50), font,
                            2, (255, 0, 0), 2, cv.LINE_AA)

        cv.imshow('frame', frame)
        cv.imshow('result', res)
        cv.waitKey(1)


    if k == 27:

        cv.destroyAllWindows()
        break
