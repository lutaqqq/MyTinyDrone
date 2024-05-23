import tkinter as tk
from tkinter import messagebox, Toplevel, Label, Button, Frame
import cv2
from PIL import Image, ImageTk
from datetime import datetime
import os
import threading
from djitellopy import tello
from flight_commands import start_flying, stop_flying


class VideoRecorder:
    def __init__(self, drone_frame):
        self.is_recording = False
        self.out = None
        self.frame = drone_frame

    def start_recording(self):
        if not self.is_recording:
            try:
                fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                H, W, _ = self.frame.frame.shape

                now = datetime.now()
                current_time = now.strftime("%Y-%m-%d_%H-%M-%S")
                filename = f"tello_video_{current_time}.mp4"
                folder_name = 'Video'

                if not os.path.exists(folder_name):
                    os.makedirs(folder_name)

                full_path = os.path.join(folder_name, filename)

                self.out = cv2.VideoWriter(full_path, fourcc, 30, (W, H))
                self.is_recording = True
                return True
            except Exception as e:
                messagebox.showerror('Ошибка', f'Ошибка при начале записи видео: {e}')
                return False
        else:
            self.stop_recording()
            return False

    def stop_recording(self):
        if self.is_recording:
            self.out.release()
            self.is_recording = False
            return True
        else:
            return False

    def record_frame(self):
        if self.is_recording and self.out is not None:
            frame = self.frame.frame
            self.out.write(frame)


class DroneController:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Контроллер TELLO")

        self.input_frame = Frame(self.root)

        self.drone = tello.Tello()
        self.drone.connect()
        self.drone.streamon()

        self.frame = self.drone.get_frame_read()

        self.recorder = VideoRecorder(self.frame)

        self.is_recording = False

        self.drone.speed = 75

        self.cap_lbl = Label(self.root)

        self.takeoff_land_button = Button(self.root, text='Взлететь / Приземлиться', command=self.takeoff_land)
        self.takeoff_land_button.grid(column=1, row=3)

        self.flip_button = Button(self.root, text='Меню флипов', command=self.open_flip_window)
        self.flip_button.grid(column=1, row=4)

        self.camera_record_button = Button(self.root, text='Начать запись', command=self.toggle_camera_recording)
        self.camera_record_button.grid(column=1, row=5)

        self.setup_keyboard_controls()

    def toggle_camera_recording(self):
        if self.is_recording:
            self.stop_camera_recording()
        else:
            self.start_camera_recording()

    def start_camera_recording(self):
        if self.recorder.start_recording():
            self.is_recording = True
            self.camera_record_button.config(text='Остановить запись')
        else:
            self.camera_record_button.config(text='Начать запись')

    def stop_camera_recording(self):
        if self.recorder.stop_recording():
            self.is_recording = False
            self.camera_record_button.config(text='Начать запись')

    def open_flip_window(self):
        panel = Toplevel(self.root)
        panel.title('Меню флипов')

        flip_frame = Frame(panel)

        flip_left_button = Button(flip_frame, text='Переворот влево', command=lambda: self.execute_flip('left'))
        flip_right_button = Button(flip_frame, text='Переворот вправо', command=lambda: self.execute_flip('right'))
        flip_forward_button = Button(flip_frame, text='Переворот вперёд', command=lambda: self.execute_flip('forward'))
        flip_back_button = Button(flip_frame, text='Переворот назад', command=lambda: self.execute_flip('back'))

        flip_left_button.grid(column=0, row=0)
        flip_right_button.grid(column=1, row=0)
        flip_forward_button.grid(column=0, row=1)
        flip_back_button.grid(column=1, row=1)

        flip_frame.pack()

    def execute_flip(self, direction):
        try:
            if self.drone.is_flying:
                if direction == 'left':
                    threading.Thread(target=self.drone.flip_left).start()
                elif direction == 'right':
                    threading.Thread(target=self.drone.flip_right).start()
                elif direction == 'forward':
                    threading.Thread(target=self.drone.flip_forward).start()
                elif direction == 'back':
                    threading.Thread(target=self.drone.flip_back).start()
        except Exception as e:
            messagebox.showerror('Ошибка', f'Ошибка переворота: {e}')

    def takeoff_land(self):
        if self.drone.is_flying:
            threading.Thread(target=lambda: self.drone.land()).start()
        else:
            threading.Thread(target=lambda: self.drone.takeoff()).start()

    def setup_keyboard_controls(self):
        self.input_frame.bind('<KeyPress-w>', lambda event: start_flying(event, 'upward', self.drone,
                                                                         self.drone.speed))
        self.input_frame.bind('<KeyRelease-w>', lambda event: stop_flying(event, self.drone))

        self.input_frame.bind('<KeyPress-a>', lambda event: start_flying(event, 'yaw_left', self.drone,
                                                                         self.drone.speed))
        self.input_frame.bind('<KeyRelease-a>', lambda event: stop_flying(event, self.drone))

        self.input_frame.bind('<KeyPress-s>', lambda event: start_flying(event, 'downward', self.drone,
                                                                         self.drone.speed))
        self.input_frame.bind('<KeyRelease-s>', lambda event: stop_flying(event, self.drone))

        self.input_frame.bind('<KeyPress-d>', lambda event: start_flying(event, 'yaw_right', self.drone,
                                                                          self.drone.speed))
        self.input_frame.bind('<KeyRelease-d>', lambda event: stop_flying(event, self.drone))

        self.input_frame.bind('<KeyPress-Up>', lambda event: start_flying(event, 'forward', self.drone,
                                                                          self.drone.speed))
        self.input_frame.bind('<KeyRelease-Up>', lambda event: stop_flying(event, self.drone))

        self.input_frame.bind('<KeyPress-Down>', lambda event: start_flying(event, 'backward',
                                                                            self.drone, self.drone.speed))
        self.input_frame.bind('<KeyRelease-Down>', lambda event: stop_flying(event, self.drone))

        self.input_frame.bind('<KeyPress-Left>', lambda event: start_flying(event, 'left', self.drone,
                                                                            self.drone.speed))
        self.input_frame.bind('<KeyRelease-Left>', lambda event: stop_flying(event, self.drone))

        self.input_frame.bind('<KeyPress-Right>', lambda event: start_flying(event, 'right', self.drone,
                                                                             self.drone.speed))
        self.input_frame.bind('<KeyRelease-Right>', lambda event: stop_flying(event, self.drone))

        self.input_frame.grid(column=2, row=2)
        self.input_frame.focus_set()

    def video_stream(self):
        try:
            frame = self.frame.frame
            frame = cv2.resize(frame, (720, 480))

            cv2image = cv2.cvtColor(frame, cv2.COLOR_RGB2RGBA)

            img = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=img)

            self.cap_lbl.imgtk = imgtk
            self.cap_lbl.configure(image=imgtk)

            self.recorder.record_frame()

            self.root.after(10, self.video_stream)
        except Exception as e:
            messagebox.showerror('Ошибка', f'Ошибка в потоке видео: {e}')

    def run_app(self):
        try:
            self.cap_lbl.grid(column=1, row=2)

            self.video_stream()

            video_thread = threading.Thread(target=self.video_stream)
            video_thread.daemon = True
            video_thread.start()

            self.root.mainloop()

        except Exception as e:
            messagebox.showerror('Ошибка', f'Ошибка при запуске приложения: {e}')
        finally:
            self.cleanup()

    def cleanup(self):
        try:
            print('Освобождение ресурсов...')
            self.drone.end()
        except Exception as e:
            messagebox.showerror('Ошибка', f'Ошибка освобождения ресурсов: {e}')


if __name__ == '__main__':
    gui = DroneController()
    gui.run_app()