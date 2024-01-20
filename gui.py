import tkinter
from tkinter import ttk
from mosaic import *



def change_range(self, range_scale, range_label):
    value = "현재 범위 값 : " + str(range_scale.get());
    range_label.config(text=value);
    set_range(range_scale.get());
    
    
def change_strength(self, strength_scale, strength_label):
    value = "현재 강도 값 : " + str(strength_scale.get());
    strength_label.config(text=value);    
    set_strength(strength_scale.get());

# def buttonClicked():
#     label.configure(foreground='blue')
#     label.configure(text='CLICKED')
#     button.configure(text='GOOD!')
def run():
    window=tkinter.Tk()

    window.title("Real - Time Mosaic")
    window.geometry("210x130")
    window.resizable(False, False)

    range_scale = tkinter.Scale(window, strength_scale, strength_label, command=change_range, to=2, resolution=0.1, length=200, orient="horizontal");
    range_scale.set(1);
    range_scale.grid(row=0, column=0);

    range_label = ttk.Label(window, text="현재 범위 값 : 0")
    range_label.grid(row=2, column=0);

    strength_scale = tkinter.Scale(window, range_scale, range_label, command=change_strength, from_=0.1, to=0, resolution=0.01, length=200, orient="horizontal");
    strength_scale.set(0.05);
    strength_scale.grid(row=3, column=0);

    strength_label = ttk.Label(window, text="현재 강도 값 : 0")
    strength_label.grid(row=4, column=0);
    window.mainloop()


# # Button
# button = ttk.Button(window, text="CLICK", command=buttonClicked)




