from tkinter import Tk, Label, Button, Frame, Toplevel, messagebox
from PIL import Image, ImageTk
from djitellopy import tello
from flight_commands import start_flying, stop_flying
from indicators import Indicators
from datetime import datetime
import cv2
import threading
import os

class DroneController:
    def __init__(self):

        self.root = Tk()
        self.root.title("Контроллер TELLO")
        self.root.minsize(800, 600)

        self.input_frame = Frame(self.root)

        self.drone = tello.Tello()
        self.drone.connect()
        self.drone.streamon()

        self.flying = False

        self.h = 480
        self.w = 720

        self.frame = self.drone.get_frame_read()

        self.is_recording = False
        self.out = None

        self.drone.speed = 100

        self.cap_lbl = Label(self.root)

        self.takeoff_land_button = Button(self.root, text='Взлететь / Приземлиться', command=lambda: self.takeoff_land())
        self.takeoff_land_button.grid(column=1, row=3)

        self.flipping = False

        self.flip_button = Button(self.root, text='Меню флипов', command=self.openFlipWindow)
        self.flip_button.grid(column=1, row=4)

        self.flip_left_button = None
        self.flip_right_button = None
        self.flip_forward_button = None
        self.flip_back_button = None

        self.camera_record_button = Button(self.root, text='Начать запись', command=self.start_camera_recording)
        self.camera_record_button.grid(column=1, row=5)

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

        self.indicators = Indicators(self.drone, self.w, self.h)

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

                # Combine folder name with filename for full path
                full_path = os.path.join(folder_name, filename)

                # Set up video writer for recording
                self.out = cv2.VideoWriter(full_path, fourcc, 30, (w, h))
                self.is_recording = True
                self.camera_record_button.config(text='Остановить запись')

                # Start video recording thread
                threading.Thread(target=self.record_tello_video).start()
            except Exception as e:
                messagebox.showerror('Ошибка', f'Ошибка при начале записи видео: {e}')
        else:
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
            # Close the window and release the video writer
            cv2.destroyAllWindows()
            self.out.release()

    def openFlipWindow(self):
        panel = Toplevel(self.root)
        panel.wm_title('Меню флипов')

        flip_frame = Frame(panel)  # Создаем новый фрейм в Toplevel окне
        try:
            self.flip_left_button = Button(flip_frame, text='Переворот влево', command=lambda: self.execute_flip('left'))

            self.flip_right_button = Button(flip_frame, text='Переворот вправо', command=lambda: self.execute_flip('right'))

            self.flip_forward_button = Button(flip_frame, text='Переворот вперёд', command=lambda: self.execute_flip('forward'))

            self.flip_back_button = Button(flip_frame, text='Переворот назад', command=lambda: self.execute_flip('back'))

        except Exception as e:
            messagebox.showerror('Ошибка', f'Ошибка переворота: {e}')


        # Упаковываем кнопки флипа во вновь созданный фрейм
        self.flip_left_button.grid(column=0, row=0, padx=10, pady=5)
        self.flip_right_button.grid(column=0, row=1, padx=10, pady=5)
        self.flip_forward_button.grid(column=0, row=2, padx=10, pady=5)
        self.flip_back_button.grid(column=0, row=3, padx=10, pady=5)

        flip_frame.pack()

    def execute_flip(self, direction):
        try:
            if self.drone.is_flying and self.flipping is False:
                if direction == 'left':
                    print('Переворот влево')
                    threading.Thread(target=lambda dir=direction: self.drone.flip_left()).start()
                    self.flipping = True
                elif direction == 'right':
                    print('Переворот вправо')
                    threading.Thread(target=lambda dir=direction: self.drone.flip_right()).start()
                    self.flipping = True
                elif direction == 'forward':
                    print('Переворот вперёд')
                    threading.Thread(target=lambda dir=direction: self.drone.flip_forward()).start()
                    self.flipping = True
                elif direction == 'back':
                    print('Переворот назад')
                    threading.Thread(target=lambda dir=direction: self.drone.flip_back()).start()
                    self.flipping = True
        except Exception as e:
            messagebox.showerror('Ошибка', f'Ошибка переворота: {e}')
        finally:
            self.flipping = False

    def takeoff_land(self):
        if self.drone.is_flying:
            threading.Thread(target=lambda: self.drone.land()).start()
        else:
            threading.Thread(target=lambda: self.drone.takeoff()).start()

    def run_app(self):
        try:
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

    def video_stream(self):

        try:
            frame = self.frame.frame
            frame = cv2.resize(frame, (self.w, self.h))

            self.indicators.draw_battery_indicator(frame)

            cv2image = cv2.cvtColor(frame, cv2.COLOR_RGB2RGBA)  # Convert from BGR to RGB

            img = Image.fromarray(cv2image)

            imgtk = ImageTk.PhotoImage(image=img)

            self.cap_lbl.grid(column=1, row=2)

            self.cap_lbl.imgtk = imgtk

            self.cap_lbl.configure(image=imgtk)

            if self.is_recording:
                if self.out is not None:
                    self.out.write(frame)

            self.root.update_idletasks()  # Force update of GUI

            self.cap_lbl.after(15, self.video_stream)
        except Exception as e:
            messagebox.showerror('Ошибка', f'Ошибка в потоке видео: {e}')

    def cleanup(self) -> None:
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
