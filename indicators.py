import cv2
import time
import threading

class Indicators:
    def __init__(self, drone, w, h):

        self.update = False

        self.w = w
        self.h = h
        self.drone = drone

        self.battery = self.drone.get_battery()

        threading.Thread(target=lambda: self.update_indicators()).start()

    def update_indicators(self) -> None:
        """Set update to True and continuously update the indicator values by calling the drones
        associated methods for getting that indicators respective current value reading."""
        self.update = True
        while self.update:
            print("self.drone is true, updating indicators")
            self.battery = self.drone.get_battery()
            print(f"self.battery = {self.battery}")
            time.sleep(1)

    def draw_battery_indicator(self, frame) -> None:

        cv2.rectangle(frame, (self.w // 128 + 3, self.h // 32 + 29), (self.w // 128 + 52, self.h // 32 + 51),
                      (255, 255, 255), -1)
        cv2.rectangle(frame, (self.w // 128 + 52, self.h // 32 + 35), (self.w // 128 + 55, self.h // 32 + 45),
                      (255, 255, 255),
                      -1)

        # Check if the battery level is above 70%
        if self.battery >= 70:

            color = (0, 255, 0)

            if self.battery == 100:

                cv2.line(frame, (self.w // 128 + 5, self.h // 32 + 30), (self.w // 128 + 5, self.h // 32 + 50), color,
                         2)
                cv2.line(frame, (self.w // 128 + 10, self.h // 32 + 30), (self.w // 128 + 10, self.h // 32 + 50), color,
                         2)
                cv2.line(frame, (self.w // 128 + 15, self.h // 32 + 30), (self.w // 128 + 15, self.h // 32 + 50), color,
                         2)
                cv2.line(frame, (self.w // 128 + 20, self.h // 32 + 30), (self.w // 128 + 20, self.h // 32 + 50), color,
                         2)
                cv2.line(frame, (self.w // 128 + 25, self.h // 32 + 30), (self.w // 128 + 25, self.h // 32 + 50), color,
                         2)
                cv2.line(frame, (self.w // 128 + 30, self.h // 32 + 30), (self.w // 128 + 30, self.h // 32 + 50), color,
                         2)
                cv2.line(frame, (self.w // 128 + 35, self.h // 32 + 30), (self.w // 128 + 35, self.h // 32 + 50), color,
                         2)
                cv2.line(frame, (self.w // 128 + 40, self.h // 32 + 30), (self.w // 128 + 40, self.h // 32 + 50), color,
                         2)
                cv2.line(frame, (self.w // 128 + 45, self.h // 32 + 30), (self.w // 128 + 45, self.h // 32 + 50), color,
                         2)
                cv2.line(frame, (self.w // 128 + 50, self.h // 32 + 30), (self.w // 128 + 50, self.h // 32 + 50), color,
                         2)


            elif 90 <= self.battery < 100:

                cv2.line(frame, (self.w // 128 + 5, self.h // 32 + 30), (self.w // 128 + 5, self.h // 32 + 50), color,
                         2)
                cv2.line(frame, (self.w // 128 + 10, self.h // 32 + 30), (self.w // 128 + 10, self.h // 32 + 50), color,
                         2)
                cv2.line(frame, (self.w // 128 + 15, self.h // 32 + 30), (self.w // 128 + 15, self.h // 32 + 50), color,
                         2)
                cv2.line(frame, (self.w // 128 + 20, self.h // 32 + 30), (self.w // 128 + 20, self.h // 32 + 50), color,
                         2)
                cv2.line(frame, (self.w // 128 + 25, self.h // 32 + 30), (self.w // 128 + 25, self.h // 32 + 50), color,
                         2)
                cv2.line(frame, (self.w // 128 + 30, self.h // 32 + 30), (self.w // 128 + 30, self.h // 32 + 50), color,
                         2)
                cv2.line(frame, (self.w // 128 + 35, self.h // 32 + 30), (self.w // 128 + 35, self.h // 32 + 50), color,
                         2)
                cv2.line(frame, (self.w // 128 + 40, self.h // 32 + 30), (self.w // 128 + 40, self.h // 32 + 50), color,
                         2)
                cv2.line(frame, (self.w // 128 + 45, self.h // 32 + 30), (self.w // 128 + 45, self.h // 32 + 50), color,
                         2)

            elif 80 <= self.battery < 90:

                cv2.line(frame, (self.w // 128 + 5, self.h // 32 + 30), (self.w // 128 + 5, self.h // 32 + 50), color,
                         2)
                cv2.line(frame, (self.w // 128 + 10, self.h // 32 + 30), (self.w // 128 + 10, self.h // 32 + 50), color,
                         2)
                cv2.line(frame, (self.w // 128 + 15, self.h // 32 + 30), (self.w // 128 + 15, self.h // 32 + 50), color,
                         2)
                cv2.line(frame, (self.w // 128 + 20, self.h // 32 + 30), (self.w // 128 + 20, self.h // 32 + 50), color,
                         2)
                cv2.line(frame, (self.w // 128 + 25, self.h // 32 + 30), (self.w // 128 + 25, self.h // 32 + 50), color,
                         2)
                cv2.line(frame, (self.w // 128 + 30, self.h // 32 + 30), (self.w // 128 + 30, self.h // 32 + 50), color,
                         2)
                cv2.line(frame, (self.w // 128 + 35, self.h // 32 + 30), (self.w // 128 + 35, self.h // 32 + 50), color,
                         2)
                cv2.line(frame, (self.w // 128 + 40, self.h // 32 + 30), (self.w // 128 + 40, self.h // 32 + 50), color,
                         2)

            else:

                cv2.line(frame, (self.w // 128 + 5, self.h // 32 + 30), (self.w // 128 + 5, self.h // 32 + 50), color,
                         2)
                cv2.line(frame, (self.w // 128 + 10, self.h // 32 + 30), (self.w // 128 + 10, self.h // 32 + 50), color,
                         2)
                cv2.line(frame, (self.w // 128 + 15, self.h // 32 + 30), (self.w // 128 + 15, self.h // 32 + 50), color,
                         2)
                cv2.line(frame, (self.w // 128 + 20, self.h // 32 + 30), (self.w // 128 + 20, self.h // 32 + 50), color,
                         2)
                cv2.line(frame, (self.w // 128 + 25, self.h // 32 + 30), (self.w // 128 + 25, self.h // 32 + 50), color,
                         2)
                cv2.line(frame, (self.w // 128 + 30, self.h // 32 + 30), (self.w // 128 + 30, self.h // 32 + 50), color,
                         2)
                cv2.line(frame, (self.w // 128 + 35, self.h // 32 + 30), (self.w // 128 + 35, self.h // 32 + 50), color,
                         2)


        elif 40 <= self.battery < 70:


            color = (0, 255, 255)


            if self.battery >= 60:

                cv2.line(frame, (self.w // 128 + 5, self.h // 32 + 30), (self.w // 128 + 5, self.h // 32 + 50), color,
                         2)
                cv2.line(frame, (self.w // 128 + 10, self.h // 32 + 30), (self.w // 128 + 10, self.h // 32 + 50), color,
                         2)
                cv2.line(frame, (self.w // 128 + 15, self.h // 32 + 30), (self.w // 128 + 15, self.h // 32 + 50), color,
                         2)
                cv2.line(frame, (self.w // 128 + 20, self.h // 32 + 30), (self.w // 128 + 20, self.h // 32 + 50), color,
                         2)
                cv2.line(frame, (self.w // 128 + 25, self.h // 32 + 30), (self.w // 128 + 25, self.h // 32 + 50), color,
                         2)
                cv2.line(frame, (self.w // 128 + 30, self.h // 32 + 30), (self.w // 128 + 30, self.h // 32 + 50), color,
                         2)


            elif 50 <= self.battery < 60:

                cv2.line(frame, (self.w // 128 + 5, self.h // 32 + 30), (self.w // 128 + 5, self.h // 32 + 50), color,
                         2)
                cv2.line(frame, (self.w // 128 + 10, self.h // 32 + 30), (self.w // 128 + 10, self.h // 32 + 50), color,
                         2)
                cv2.line(frame, (self.w // 128 + 15, self.h // 32 + 30), (self.w // 128 + 15, self.h // 32 + 50), color,
                         2)
                cv2.line(frame, (self.w // 128 + 20, self.h // 32 + 30), (self.w // 128 + 20, self.h // 32 + 50), color,
                         2)
                cv2.line(frame, (self.w // 128 + 25, self.h // 32 + 30), (self.w // 128 + 25, self.h // 32 + 50), color,
                         2)

            # if between 40% and 50% draw 4 yellow lines.
            else:
                cv2.line(frame, (self.w // 128 + 5, self.h // 32 + 30), (self.w // 128 + 5, self.h // 32 + 50), color,
                         2)
                cv2.line(frame, (self.w // 128 + 10, self.h // 32 + 30), (self.w // 128 + 10, self.h // 32 + 50), color,
                         2)
                cv2.line(frame, (self.w // 128 + 15, self.h // 32 + 30), (self.w // 128 + 15, self.h // 32 + 50), color,
                         2)
                cv2.line(frame, (self.w // 128 + 20, self.h // 32 + 30), (self.w // 128 + 20, self.h // 32 + 50), color,
                         2)

        # Check if the battery is less than 40% capacity.
        else:

            # If so, set the color to red.
            color = (0, 0, 255)

            # If the battery is between 30% and 40% draw 3 red lines.
            if self.battery >= 30:
                cv2.line(frame, (self.w // 128 + 5, self.h // 32 + 30), (self.w // 128 + 5, self.h // 32 + 50), color,
                         2)
                cv2.line(frame, (self.w // 128 + 10, self.h // 32 + 30), (self.w // 128 + 10, self.h // 32 + 50), color,
                         2)
                cv2.line(frame, (self.w // 128 + 15, self.h // 32 + 30), (self.w // 128 + 15, self.h // 32 + 50), color,
                         2)

            # If the battery is between 20% and 30% draw 2 red lines.
            elif 20 <= self.battery < 30:
                cv2.line(frame, (self.w // 128 + 5, self.h // 32 + 30), (self.w // 128 + 5, self.h // 32 + 50), color,
                         2)
                cv2.line(frame, (self.w // 128 + 10, self.h // 32 + 30), (self.w // 128 + 10, self.h // 32 + 50), color,
                         2)

            # If the battery is between 10% and 20% draw 3 red lines.
            else:
                cv2.line(frame, (self.w // 128 + 5, self.h // 32 + 30), (self.w // 128 + 5, self.h // 32 + 50), color,
                         2)

        # Write the current batter level as a percentage text next to the indicator.
        cv2.putText(frame, f"{self.battery} %", (self.w // 128 + 60, self.h // 32 + 45), cv2.FONT_HERSHEY_COMPLEX, .5,
                    (43, 157, 255),
                    1)