from time import sleep

LCD_WIDTH = 16


class LCDOutputSimulator:

    def __init__(self, app):
        self.app = app
        self.canvas = app.canvas
        self.tk_lines = [app.tk_line_1, app.tk_line_2]

    def attach(self):
        sleep(0.5)
        self.canvas.itemconfig(self.tk_lines[0], text="XXXXXXXXXXXXXXXX")
        self.canvas.update_idletasks()
        sleep(0.5)
        self.canvas.itemconfig(self.tk_lines[1], text="XXXXXXXXXXXXXXXX")
        self.canvas.update_idletasks()
        sleep(0.5)

    def clear(self, lines=None):
        if lines is None:
            lines = [0, 1]
        for l in lines:
            self.print(' ' * LCD_WIDTH, pos_x=0, pos_y=l)

    def print(self, string, pos_x=None, pos_y=None):
        if pos_y is None:
            pos_y = 0
        value = self.canvas.itemcget(self.tk_lines[pos_y], 'text')
        new_value = value[:pos_x] + string + value[pos_x + len(string):]
        assert len(new_value) == LCD_WIDTH
        self.canvas.itemconfig(self.tk_lines[pos_y], text=new_value)
        self.canvas.update_idletasks()
        sleep(0.2)
