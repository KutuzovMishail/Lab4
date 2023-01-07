# Import module
import tkinter as tk
from PIL import ImageTk, Image
import random
import string
from playsound import playsound
import threading
from itertools import count


class ImageLabel(tk.Label):
    """a label that displays images, and plays them if they are gifs"""

    def load(self, im):
        if isinstance(im, str):
            im = Image.open(im)
        self.loc = 0
        self.frames = []

        try:
            for i in count(1):
                self.frames.append(ImageTk.PhotoImage(im.copy().resize((600, 600))))
                im.seek(i)
        except EOFError:
            pass

        try:
            self.delay = im.info['duration']
        except:
            self.delay = 100

        if len(self.frames) == 1:
            self.config(image=self.frames[0])
        else:
            self.next_frame()

    def unload(self):
        self.config(image="")
        self.frames = None

    def next_frame(self):
        if self.frames:
            self.loc += 1
            self.loc %= len(self.frames)
            self.config(image=self.frames[self.loc])
            self.after(self.delay, self.next_frame)


def update_code(lbl):
    th_1 = random.randint(0, 25)
    th_2 = random.randint(0, 25)
    while th_1 == th_2:
        th_1 = random.randint(0, 25)
        th_2 = random.randint(0, 25)

    min_th = min(th_1, th_2)
    max_th = max(th_1, th_2)

    first_block = str(min_th + 1) if min_th >= 9 else '0' + str(min_th + 1)
    third_block = str(max_th + 1) if max_th >= 9 else '0' + str(max_th + 1)

    second_block = [string.ascii_uppercase[random.randint(min_th, max_th)] for _ in range(7)]

    generated_key = first_block + ' ' + ''.join(second_block) + ' ' + third_block
    lbl.configure(text=generated_key)


if __name__ == "__main__":
    root = tk.Tk()
    root.title('Code generator')
    # Adjust size
    root.geometry("600x600")

    # Add image file
    deathwing = Image.open('img_terraria_4.gif')
    image2 = deathwing.resize((600, 600), Image.Resampling.LANCZOS)
    bg = ImageTk.PhotoImage(image2)

    threading.Thread(target=playsound, args=('melody_2.mp3',), daemon=True).start()

    label1 = ImageLabel(root)
    label1.pack()
    label1.load('img_terraria_4.gif')
    label1.place(x=0, y=0)

    label2 = tk.Label(root, text="Code/Key will be here")
    label2.pack(pady=50)

    frame1 = tk.Frame(root)
    frame1.pack(pady=10)

    button1 = tk.Button(frame1, text="Generate code", command=lambda: update_code(label2))
    button1.pack(pady=0)

    root.mainloop()