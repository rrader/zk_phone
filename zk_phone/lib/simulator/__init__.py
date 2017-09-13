from tkinter import *

from zk_phone.app import App
from zk_phone.lib.player import AudioOutput
from zk_phone.lib.simulator.fakeio.keyboard import KeyboardInputSimulator
from zk_phone.lib.simulator.fakeio.lcd_output import LCDOutputSimulator
from zk_phone.lib.simulator.fakeio.reed import ReedSwitchInputSimulator


def draw_rectangle(canvas, x1, y1, x2, y2, radius, fill="", outline="black", tags=None):
    points = [x1 + radius, y1,
              x1 + radius, y1,
              x2 - radius, y1,
              x2 - radius, y1,
              x2, y1,
              x2, y1 + radius,
              x2, y1 + radius,
              x2, y2 - radius,
              x2, y2 - radius,
              x2, y2,
              x2 - radius, y2,
              x2 - radius, y2,
              x1 + radius, y2,
              x1 + radius, y2,
              x1, y2,
              x1, y2 - radius,
              x1, y2 - radius,
              x1, y1 + radius,
              x1, y1 + radius,
              x1, y1, ]

    return canvas.create_polygon(points, fill=fill, outline=outline, smooth=True, tags=tags)


class Simulator(App):
    def __init__(self):
        master = Tk()
        w = Canvas(master, width=600, height=800)
        w.pack()
        self.canvas = w

        gap = 20
        radius = 20
        phone_x = 3 * gap
        phone_y = 3 * gap
        phone_w = 450
        phone_h = 500

        # The phone
        draw_rectangle(
            w,
            phone_x, phone_y, phone_x + phone_w, phone_y + phone_h,
            radius, 'green'
        )
        handset_x = gap + phone_x
        handset_y = phone_y
        handset_w = phone_w / 6
        handset_h = phone_h
        # Handset
        draw_rectangle(
            w, handset_x, handset_y, handset_x + handset_w, handset_y + handset_h,
            radius, 'black', tags='handset'
        )
        w.create_oval(
            handset_x - gap, handset_y - gap, handset_x + handset_w + gap, handset_y + handset_w + gap, fill='black',
            tags='handset'
        )
        w.create_oval(
            handset_x - gap, handset_y + handset_h - 5 * gap,
            handset_x + handset_w + gap, handset_y + handset_h + handset_w - 3 * gap, fill='black',
            tags='handset'
        )
        w.create_line(  # light blink
            handset_x + 15, handset_y + handset_w + 30, handset_x + 15, handset_y + handset_h - 30, fill="gray", width=3,
            tags='handset'
        )
        # LCD
        lcd_x = handset_x + handset_w + 2 * gap
        lcd_y = phone_y + gap
        line_height = 20
        lcd_h = line_height * 2 + 3 * gap
        lcd_w = phone_x + phone_w - lcd_x - gap
        draw_rectangle(w, lcd_x, lcd_y, lcd_x + lcd_w, lcd_y + lcd_h, radius, 'lightgreen')
        self.tk_line_1 = w.create_text(lcd_x + gap, lcd_y + gap, anchor='nw', font=("consolas", 15),
                                       text='0123456789ABCDEF')
        self.tk_line_2 = w.create_text(lcd_x + gap, lcd_y + line_height + 2 * gap, anchor='nw', font=("consolas", 15),
                                       text='  LINE 2 OF LCD ')
        # Keys
        kb_x = handset_x + handset_w + 2 * gap
        kb_y = phone_y + lcd_h + 2 * gap
        kb_w = phone_x + phone_w - kb_x - gap
        key_size = kb_w / 4 - (3 * gap) / 4
        KEYPAD = [
            ['1', '2', '3', 'x'],
            ['4', '5', '6', 'x'],
            ['7', '8', '9', 'x'],
            ["*", '0', "#", 'x']
        ]
        self.tk_keypad = [[], [], [], []]
        for row in range(4):
            for col in range(4):
                x = kb_x + col * (key_size + gap)
                y = kb_y + row * (key_size + gap)
                self.tk_keypad[row].append(
                    draw_rectangle(w, x, y, x + key_size, y + key_size, radius, 'gray', tags='btn' + KEYPAD[row][col])
                )
                if col != 3:
                    w.create_text(
                        x + key_size / 2, y + key_size / 2, font=("consolas", 20), text=KEYPAD[row][col],
                        tags='btn' + KEYPAD[row][col]
                    )

        super().__init__()

    def setup_io(self):
        self.lcd = LCDOutputSimulator(self)
        self.reed = ReedSwitchInputSimulator(self, self.reed_switched)
        self.kb = KeyboardInputSimulator(self, self.keypressed)
        self.audio = AudioOutput(self)

    def run(self):
        mainloop()


def main():
    s = Simulator()
    s.run()


if __name__ == "__main__":
    main()
