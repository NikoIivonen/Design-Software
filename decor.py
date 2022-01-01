import pygame
import sys
from tkinter import *
from tkinter.ttk import Combobox
from tkinter import messagebox
from tkinter import filedialog

shape = None
text = None
base_w = None
base_h = None
base_wp = None
base_hp = None

base_url = ""
obj_list = []


def menu():

    choice = False
    # Create the root window
    window = Tk()

    window.title('Main menu')

    window.geometry("500x500")

    window.config(background="white")

    def new():
        nonlocal choice
        choice = False
        window.destroy()

    def old():
        nonlocal choice
        choice = True
        window.destroy()

    button_new = Button(window, text="New template", command=new)
    button_old = Button(window, text="Load a template", command=old)

    button_new.place(x=100, y=200)
    button_old.place(x=300, y=200)

    window.mainloop()

    return choice


load_old = menu()


def save():

    with open("decor_saves.txt", "w") as file:
        file.write(base_url+";"+str(base_w)+";"+str(base_h)+"\n")
        for obj in obj_list:
            if type(obj) == Shape:
                line = obj.name+";"+str(obj.w)+";"+str(obj.h)+";"+str(obj.angle)+";"+str(obj.scale)+";"+str(obj.x)+";"+str(obj.y)
                file.write(line+"\n")
            elif type(obj) == Object:
                line = "image;"+str(obj.x)+";"+str(obj.y)+";"+str(obj.w)+";"+str(obj.h)+";"+str(obj.img_url)+";"+str(obj.angle)+";"+str(obj.scale)
                file.write(line+"\n")


def load():

    global base_url, base_w, base_h, base_wp, base_hp

    with open("decor_saves.txt", "r") as file:

        for line in file.readlines():

            if line[0] == "r" or line[0] == "c":
                line = line.strip("\n")
                parts = line.split(";")

                name = parts[0]
                width = float(parts[1])
                height = float(parts[2])
                angle = float(parts[3])
                scale = float(parts[4])
                x = float(parts[5])
                y = float(parts[6])

                obj_list.append(Shape(name, width, height, angle, scale, x, y))

            elif line[0] == "i":
                line = line.strip("\n")
                parts = line.split(";")[1:]
                x = float(parts[0])
                y = float(parts[1])
                width = float(parts[2])
                height = float(parts[3])
                url = parts[4]
                angle = float(parts[5])
                scale = float(parts[6])
                img = pygame.image.load(url)

                obj_list.append(Object(img, x, y, width, height, url, angle, scale))

            else:
                parts = line.split(";")
                base_url = parts[0]
                base_w = float(parts[1])
                base_h = float(parts[2])

                img = pygame.image.load(base_url)
                bigger = max(img.get_width(), img.get_height())
                ratio = 800 / bigger

                base_wp = img.get_width() * ratio
                base_hp = img.get_height() * ratio


def base_info():
    tk = Tk()
    tk.geometry("500x400")
    tk.title("Enter info")
    url = ""

    def browseFiles():
        nonlocal url
        url = filedialog.askopenfilename(initialdir="/", title="Select a File")

    def select():
        global text, base_w, base_h
        text = ent1.get() + ";" + ent2.get()

        try:
            parts = text.split(";")
            base_w = float(parts[0])
            base_h = float(parts[1])
            img = pygame.image.load(url)
            if base_w <= 0 or base_h <= 0 or len(url) == 0:
                raise ValueError
            tk.destroy()
        except:
            messagebox.showerror(title="Error", message="Check your inputs")

    b1 = Button(tk, text="Check", command=select).place(x=180, y=300, width=100, height=50)

    lb1 = Label(tk, text="Base width (m)")
    lb1.place(x=110, y=150)
    ent1 = Entry(tk)
    ent1.place(x=200, y=150)

    lb2 = Label(tk, text="Base height (m)")
    lb2.place(x=110, y=200)
    ent2 = Entry(tk)
    ent2.place(x=200, y=200)

    button_explore = Button(tk, text="Browse Files", command=browseFiles)
    button_explore.place(x=220, y=90)

    tk.mainloop()

    return url


def shape_info():
    tk = Tk()
    tk.geometry("500x400")
    tk.title("Enter info")

    def select():
        global shape, text
        shape = cb.get().lower()
        text = ent1.get() + ";" + ent2.get()

        try:
            if shape == "":
                raise ValueError
            parts = text.split(";")
            w = float(parts[0])
            h = float(parts[1])
            text = shape+";"+text
            tk.destroy()
        except:
            messagebox.showerror(title="Error", message="Check your inputs")

    data = ("Rectangle", "Circle")
    cb = Combobox(tk, values=data)
    cb.place(x=60, y=150)
    b1 = Button(tk, text="Check", command=select).place(x=180, y=300, width=100, height=50)

    lb1 = Label(tk, text="Width (cm)")
    lb1.place(x=204, y=150)
    ent1 = Entry(tk)
    ent1.place(x=270, y=150)

    lb2 = Label(tk, text="Height (cm)")
    lb2.place(x=200, y=200)
    ent2 = Entry(tk)
    ent2.place(x=270, y=200)

    tk.mainloop()


def scale_info():
    tk = Tk()
    tk.geometry("500x400")
    tk.title("Enter info")

    def select():
        global text
        e1 = ent1.get()
        e2 = ent2.get()

        if e1 == "":
            e1 = "100"
        if e2 == "":
            e2 = "0"

        text = e1 + ";" + e2

        try:
            parts = text.split(";")
            s = float(parts[0])
            r = float(parts[1])
            if s < 0:
                raise ValueError

            tk.destroy()
        except:
            messagebox.showerror(title="Error", message="Check your inputs")

    b1 = Button(tk, text="Check", command=select).place(x=180, y=300, width=100, height=50)

    lb1 = Label(tk, text="Scale-%")
    lb1.place(x=145, y=150)
    ent1 = Entry(tk)
    ent1.place(x=200, y=150)

    lb2 = Label(tk, text="Rotation angle")
    lb2.place(x=110, y=200)
    ent2 = Entry(tk)
    ent2.place(x=200, y=200)

    tk.mainloop()


def image_info():
    url = ""
    w = 0
    h = 0

    tk = Tk()
    tk.geometry("500x400")
    tk.title("Enter info")

    def browseFiles():
        nonlocal url
        url = filedialog.askopenfilename(initialdir="/", title="Select a File")

    def select():
        nonlocal url, w, h
        try:
            w = float(ent2.get())
            h = float(ent3.get())
            img = pygame.image.load(url)
            if len(url) == 0 or w <= 0 or h <= 0:
                raise ValueError
            tk.destroy()
        except:
            messagebox.showerror(title="Error", message="Check your inputs")

    b1 = Button(tk, text="Check", command=select).place(x=180, y=300, width=100, height=50)

    # lb1 = Label(tk, text="Image URL")
    # lb1.place(x=135, y=150)
    # ent1 = Entry(tk)
    # ent1.place(x=200, y=150)
    # ent1.clipboard_get()

    button_explore = Button(tk, text="Browse Files", command=browseFiles)
    button_explore.place(x=220, y=150)

    lb2 = Label(tk, text="Object width (cm)")
    lb2.place(x=95, y=200)
    ent2 = Entry(tk)
    ent2.place(x=200, y=200)

    lb3 = Label(tk, text="Object height (cm)")
    lb3.place(x=92, y=250)
    ent3 = Entry(tk)
    ent3.place(x=200, y=250)

    tk.mainloop()

    return url, w, h


pygame.init()
clock = pygame.time.Clock()

font_button = pygame.font.SysFont("arial", 18, True)
screen = pygame.display.set_mode((800, 800))


class Shape:
    def __init__(self, shape: str, width: float, height: float, angle, scale, x, y):
        self.x = x
        self.y = y
        self.w = width
        self.h = height
        self.scale = scale
        self.width, self.height = width*(self.scale/100) / (base_w * 100) * base_wp, height*(self.scale/100) / (base_h * 100) * base_hp
        self.shape = pygame.Rect(self.x, self.y, self.width, self.height)
        self.name = shape
        self.drag = False
        self.surf = pygame.Surface((self.width, self.height))
        self.angle = angle
        self.surf.set_colorkey((2, 3, 4))
        self.surf.fill((10, 10, 10))

    def draw(self):
        self.shape = pygame.Rect(self.x, self.y, self.width, self.height)

        if self.name == "rectangle":
            pygame.draw.rect(self.surf, (0, 0, 0), self.shape)
            rotated = pygame.transform.rotate(self.surf, self.angle)
            screen.blit(rotated, (self.x, self.y))
        elif self.name == "circle":
            pygame.draw.ellipse(screen, (0, 0, 0), self.shape)

    def move_with_mouse(self):

        if not dragging:
            self.drag = False

        if self.shape.collidepoint(mx, my):
            self.drag = True

        if dragging and self.drag and drag_obj == self:
            self.x = mx
            self.y = my

    def right_click(self):

        if self.shape.collidepoint(mx, my):
            scale_info()
            if type(text) == str:
                parts = text.split(";")
                num = float(parts[0])
                self.scale *= num/100
                rot = float(parts[1])

                self.width, self.height = self.width*num/100, self.height*num/100
                self.surf = pygame.transform.scale(self.surf, (self.surf.get_width()*num/100, self.surf.get_height()*num/100))
                self.angle += rot

    def wheel(self):
        if self.shape.collidepoint(mx, my):
            self.angle += 5

    def delete(self):
        if self.shape.collidepoint(mx, my):
            obj_list.remove(self)


class Object:
    def __init__(self, img, x, y, width, height, img_url, angle, scale):
        self.x = x
        self.y = y
        self.scale = scale
        self.angle = angle
        self.w = width
        self.h = height
        self.width, self.height = width*(self.scale/100) / (base_w * 100) * base_wp, height*(self.scale/100) / (base_h * 100) * base_hp
        self.img = pygame.transform.rotate(pygame.transform.scale(img, (self.width, self.height)), self.angle)
        self.object = pygame.Rect(self.x, self.y, self.img.get_width(), self.img.get_height())
        self.drag = False
        self.img_url = img_url

    def draw(self):
        self.object = pygame.Rect(self.x, self.y, self.img.get_width(), self.img.get_height())
        screen.blit(self.img, self.object)

    def move_with_mouse(self):

        if self.object.collidepoint(mx, my):
            self.drag = True

        if not dragging:
            self.drag = False

        if dragging and self.drag and drag_obj == self:
            self.x = mx
            self.y = my

    def right_click(self):
        if self.object.collidepoint(mx, my):
            scale_info()
            if type(text) == str:
                parts = text.split(";")
                num = float(parts[0])
                rot = float(parts[1])
                self.angle += rot
                self.scale *= num/100

                self.width, self.height = self.img.get_width()*num/100, self.img.get_height()*num/100
                self.img = pygame.transform.scale(self.img, (self.img.get_width()*num/100, self.img.get_height()*num/100))
                self.img = pygame.transform.rotate(self.img, rot)

    def delete(self):
        if self.object.collidepoint(mx, my):
            obj_list.remove(self)


"""SCALING THE BASE RIGHT"""

if not load_old:

    base_url = base_info()

else:
    load()

img_base = pygame.image.load(base_url).convert_alpha()
bigger = max(img_base.get_width(), img_base.get_height())
ratio = 800/bigger
base_wp = img_base.get_width() * ratio
base_hp = img_base.get_height() * ratio
img_base = pygame.transform.scale(img_base, (base_wp, base_hp))


dragging = False
some_on_drag = False
drag_obj = None

mx, my = -1, -1
start_x, start_y = -1, -1


"""BUTTONS"""

button_rect = pygame.Rect(630, 750, 100, 50)
button_img = pygame.Rect(400, 750, 100, 50)


"""APP LOOP"""

while True:

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
            dragging = True

            if button_rect.collidepoint(mx, my):
                shape_info()
                if type(text) == str:
                    parts = text.split(";")
                    name = parts[0]
                    width = float(parts[1])
                    height = float(parts[2])

                    obj_list.append(Shape(name, width, height, 0, 100, 0, 100))

            if button_img.collidepoint(mx, my):
                url, w, h = image_info()
                if type(url) == str and len(url) > 0:
                    img = pygame.image.load(url).convert_alpha()
                    obj_list.append(Object(img, 700, 100, w, h, url, 0, 100))

        if e.type == pygame.MOUSEBUTTONUP and e.button == 1:
            dragging = False
            some_on_drag = False
            drag_obj = None

        if e.type == pygame.MOUSEBUTTONDOWN and e.button == 3:
            for obj in obj_list:
                obj.right_click()

        if e.type == pygame.MOUSEBUTTONUP and e.button == 3:
            for obj in obj_list:
                obj.right = False

        if e.type == pygame.KEYDOWN and e.key == pygame.K_DELETE:
            for obj in obj_list:
                obj.delete()

        if e.type == pygame.MOUSEWHEEL:
            for obj in obj_list:
                if type(obj) == Shape:
                    obj.wheel()

    """DRAGGING"""

    mx, my = pygame.mouse.get_pos()

    screen.fill((0, 0, 0))

    screen.blit(img_base, (0, 0))

    """OBJECTS"""

    for obj in obj_list:
        obj.draw()
        obj.move_with_mouse()
        if obj.drag and not some_on_drag and dragging:
            some_on_drag = True
            drag_obj = obj

    """SHAPE BUTTON"""

    pygame.draw.rect(screen, (0, 230, 0), button_rect)
    pygame.draw.rect(screen, (0, 230, 0), button_img)

    text = font_button.render("Add a shape", True, (0, 0, 0))
    screen.blit(text, (button_rect.x+5, button_rect.y+17))

    text = font_button.render("Add an image", True, (0, 0, 0))
    screen.blit(text, (button_img.x+5, button_img.y+17))

    pygame.display.flip()
    clock.tick(60)
    save()

