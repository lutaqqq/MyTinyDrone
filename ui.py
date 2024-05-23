from tkinter import Tk, Label, Button, Frame, Toplevel, messagebox
from PIL import Image, ImageTk
from djitellopy import tello
from flight_commands import start_flying, stop_flying
from indicators import Indicators
from datetime import datetime
import cv2
import threading
import os
from FaceFunction.FrontalDetection import FrontalFaceDetector
from FaceFunction.MeshDetection import FaceMeshDetector

class DroneController:
    def __init__(self):
        self.root = Tk()
        self.root.title("Контроллер TELLO")
        self.root.minsize(800, 600)

        self.input_frame = Frame(self.root)
        self.input_frame.grid(column=2, row=2)
        self.input_frame.focus_set()

        self.drone = tello.Tello()
        self.connect_drone()

        self.flying = False
        self.h = 480
        self.w = 720
        self.frame = self.drone.get_frame_read()

        self.is_recording = False
        self.out = None
        self.drone.speed = 100

        self.face_tracking = False
        self.face_detector = FaceMeshDetector(effects='blur')

        self.cap_lbl = Label(self.root)
        self.cap_lbl.grid(column=1, row=2)

        self.create_buttons()
        self.create_labels()

        self.indicators = Indicators(self.drone, self.w, self.h)

    def connect_drone(self):
        try:
            self.drone.connect()
            self.drone.streamon()
        except Exception as e:
            messagebox.showerror('Ошибка', f'Не удалось подключиться к дрону: {e}')
            self.cleanup()

    def create_buttons(self):
        self.takeoff_land_button = Button(self.root, text='Взлететь / Приземлиться', command=self.takeoff_land)
        self.takeoff_land_button.grid(column=1, row=3)

        self.flip_button = Button(self.root, text='Меню флипов', command=self.openFlipWindow)
        self.flip_button.grid(column=1, row=4)

        self.camera_record_button = Button(self.root, text='Начать запись', command=self.start_camera_recording)
        self.camera_record_button.grid(column=1, row=5)

        self.switch_button = Button(self.root, text='Включить отслеживание лиц', command=self.toggle_face_tracking)
        self.switch_button.grid(column=1, row=6)

    def create_labels(self):
        self.text0 = Label(self.root,
                           text='Команды управления TELLO с помощью клавиатуры:\n',
                           font=('TimesNewRoman', 14, 'bold'))
        self.text0.grid(column=1, row=0)

        self.text1 = Label(self.root, text=
        'W - Подняться\t\t\t\tСтрелка Вверх - Движение вперед\n'
        'S - Спуститься\t\t\t\tСтрелка Вниз - Движение назад\n'
        'A - Поворот против часовой стрелки\tСтрелка Влево - Движение влево\n'
        'D - Поворот по часовой стрелке\t\tСтрелка Вправо - Движение вправо',
                           justify='left')
        self.text1.grid(column=1, row=1)

    def toggle_face_tracking(self):
        self.face_tracking = not self.face_tracking
        if self.face_tracking:
            self.switch_button.config(text='Выключить отслеживание лиц')
        else:
            self.switch_button.config(text='Включить отслеживание лиц')

    def start_camera_recording(self):
        if not self.is_recording:
            try:
                fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Use 'mp4v' codec for MP4 format
                h, w, _ = self.frame.frame.shape

                now = datetime.now()
                current_time = now.strftime("%Y-%m-%d_%H-%M-%S")
                filename = f"tello_video_{current_time}.mp4"
                folder_name = 'Video'

                if not os.path.exists(folder_name):
                    os.makedirs(folder_name)

                full_path = os.path.join(folder_name, filename)
                self.out = cv2.VideoWriter(full_path, fourcc, 30, (w, h))
                self.is_recording = True
                self.camera_record_button.config(text='Остановить запись')
                threading.Thread(target=self.record_tello_video).start()
            except Exception as e:
                messagebox.showerror('Ошибка', f'Ошибка при начале записи видео: {e}')
        else:
            self.stop_camera_recording()

    def stop_camera_recording(self):
        if self.out:
            self.out.release()
        self.is_recording = False
        self.camera_record_button.config(text='Начать запись')

    def record_tello_video(self):
        try:
            while self.is_recording:
                frame = self.frame.frame
                self.out.write(frame)
        except Exception as e:
            messagebox.showerror('Ошибка', f'Не удалось начать запись видео: {e}')
        finally:
            cv2.destroyAllWindows()
            if self.out:
                self.out.release()

    def openFlipWindow(self):
        panel = Toplevel(self.root)
        panel.wm_title('Меню флипов')

        flip_frame = Frame(panel)
        flip_frame.pack()

        self.create_flip_buttons(flip_frame)

    def create_flip_buttons(self, flip_frame):
        try:
            self.flip_left_button = Button(flip_frame, text='Переворот влево', command=lambda: self.execute_flip('left'))
            self.flip_right_button = Button(flip_frame, text='Переворот вправо', command=lambda: self.execute_flip('right'))
            self.flip_forward_button = Button(flip_frame, text='Переворот вперёд', command=lambda: self.execute_flip('forward'))
            self.flip_back_button = Button(flip_frame, text='Переворот назад', command=lambda: self.execute_flip('back'))

            self.flip_left_button.grid(column=0, row=0, padx=10, pady=5)
            self.flip_right_button.grid(column=0, row=1, padx=10, pady=5)
            self.flip_forward_button.grid(column=0, row=2, padx=10, pady=5)
            self.flip_back_button.grid(column=0, row=3, padx=10, pady=5)
        except Exception as e:
            messagebox.showerror('Ошибка', f'Ошибка при создании кнопок флипа: {e}')

    def execute_flip(self, direction):
        try:
            if self.drone.is_flying and not self.flipping:
                self.flipping = True
                flip_func = {
                    'left': self.drone.flip_left,
                    'right': self.drone.flip_right,
                    'forward': self.drone.flip_forward,
                    'back': self.drone.flip_back
                }
                if direction in flip_func:
                    threading.Thread(target=flip_func[direction]).start()
        except Exception as e:
            messagebox.showerror('Ошибка', f'Ошибка переворота: {e}')
        finally:
            self.flipping = False

    def takeoff_land(self):
        if self.drone.is_flying:
            threading.Thread(target=self.drone.land).start()
        else:
            threading.Thread(target=self.drone.takeoff).start()

    def run_app(self):
        try:
            self.bind_keys()
            self.video_stream()
            video_thread = threading.Thread(target=self.video_stream)
            video_thread.daemon = True
            video_thread.start()
            self.root.mainloop()
        except Exception as e:
            messagebox.showerror('Ошибка', f'Ошибка при запуске приложения: {e}')
        finally:
            self.cleanup()

    def bind_keys(self):
        self.input_frame.bind('<KeyPress-w>', lambda event: start_flying(event, 'upward', self.drone, self.drone.speed))
        self.input_frame.bind('<KeyRelease-w>', lambda event: stop_flying(event, self.drone))

        self.input_frame.bind('<KeyPress-a>', lambda event: start_flying(event, 'yaw_left', self.drone, self.drone.speed))
        self.input_frame.bind('<KeyRelease-a>', lambda event: stop_flying(event, self.drone))

        self.input_frame.bind('<KeyPress-s>', lambda event: start_flying(event, 'downward', self.drone, self.drone.speed))
        self.input_frame.bind('<KeyRelease-s>', lambda event: stop_flying(event, self.drone))

        self.input_frame.bind('<KeyPress-d>', lambda event: start_flying(event, 'yaw_right', self.drone, self.drone.speed))
        self.input_frame.bind('<KeyRelease-d>', lambda event: stop_flying(event, self.drone))

        self.input_frame.bind('<KeyPress-Up>', lambda event: start_flying(event, 'forward', self.drone, self.drone.speed))
        self.input_frame.bind('<KeyRelease-Up>', lambda event: stop_flying(event, self.drone))

        self.input_frame.bind('<KeyPress-Down>', lambda event: start_flying(event, 'backward', self.drone, self.drone.speed))
        self.input_frame.bind('<KeyRelease-Down>', lambda event: stop_flying(event, self.drone))

        self.input_frame.bind('<KeyPress-Left>', lambda event: start_flying(event, 'left', self.drone, self.drone.speed))
        self.input_frame.bind('<KeyRelease-Left>', lambda event: stop_flying(event, self.drone))

        self.input_frame.bind('<KeyPress-Right>', lambda event: start_flying(event, 'right', self.drone, self.drone.speed))
        self.input_frame.bind('<KeyRelease-Right>', lambda event: stop_flying(event, self.drone))

    def video_stream(self):
        try:
            frame = self.frame.frame
            frame = cv2.resize(frame, (self.w, self.h))
            if self.face_tracking:
                self.face_detector.detect_faces(frame)
            self.indicators.draw_battery_indicator(frame)
            cv2image = cv2.cvtColor(frame, cv2.COLOR_RGB2RGBA)
            img = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=img)
            self.cap_lbl.imgtk = imgtk
            self.cap_lbl.configure(image=imgtk)

            if self.is_recording and self.out:
                self.out.write(frame)

            self.root.update_idletasks()
            self.cap_lbl.after(15, self.video_stream)
        except Exception as e:
            messagebox.showerror('Ошибка', f'Ошибка в потоке видео: {e}')

    def cleanup(self):
        try:
            print('Освобождение ресурсов...')
            self.indicators.update = False
            self.drone.end()
            self.root.quit()
            exit()
        except Exception as e:
            messagebox.showerror('Ошибка', f'Ошибка освобождения ресурсов: {e}')

if __name__ == '__main__':
    gui = DroneController()
    gui.run_app()