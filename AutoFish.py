import pyautogui
import time
import numpy as np
import cv2
import win32api, win32con
from tkinter import *
from pynput import mouse, keyboard


def on_click(x, y, button, pressed):
    global x1, y1, x2, y2
    if button == mouse.Button.right and pressed:
        if x1 == 0 and y1 == 0:
            x1 = x
            y1 = y
        #elif x1 !=0 and x2 == 0:
        #    x2 = x
        #    y2 = y
        else:
            return False
    if button == mouse.Button.right:
        print(x1,y1,x2,y2)

def on_press(key):
    global stop
    if key == keyboard.Key.esc:
        print("yes")
        stop = 1
        return False
    # Функция для получения изображения с экрана

def get_screen_image(choice):
    if choice == 0:
        pyautogui.screenshot('screens\\image.png')
        screen = cv2.imread('screens\\image.png', cv2.IMREAD_GRAYSCALE)
        cropped_screen = screen[y1:y1+50, x1:x1+64]
        array_screen = np.array(cropped_screen)
        screen_bin = cv2.threshold(array_screen, 150, 255, cv2.THRESH_BINARY)[1]
    else:
        screen = cv2.imread('screens\\base.png', cv2.IMREAD_GRAYSCALE)
        array_screen = np.array(screen)
        screen_bin = cv2.threshold(array_screen, 150, 255, cv2.THRESH_BINARY)[1]
    return screen_bin

def newbase():
    pyautogui.screenshot('screens\\image.png')
    screen = cv2.imread('screens\\image.png', cv2.IMREAD_GRAYSCALE)
    cropped_screen = screen[y1:y1+50, x1:x1+64]
    array_screen = np.array(cropped_screen)
    screen_bin = cv2.threshold(array_screen, 150, 255, cv2.THRESH_BINARY)[1]
    cv2.imwrite("screens\\base.png", screen_bin)

def select_zone():
    global x1, y1, x2, y2
    
    if x1 == 0 and x2 == 0 and y1 == 0 and y2 == 0:
        listener = mouse.Listener(on_click=on_click)
        listener.start()
    
def reset_coords():
    global x1, y1, x2, y2
    x1 = int(0)
    y1 = int(0)
    x2 = int(0)
    y2 = int(0)
    print("Coords now should be reseted, so coords now:\n x1 = ", x1,"\n y1 = ", y1,"\n x2 = ", x2,"\n y2 = ", y2)

    # Функция для сравнения двух изображений

def compare_images(image1, image2):
    diff = cv2.absdiff(image1, image2)

    total_pixels = image1.shape[0] * image1.shape[1] * 1.0
    diff_on_pixels = cv2.countNonZero(diff) * 1.0
    if np.array_equal(image1,image2):
        return 0
    else:
        difference_measure = (diff_on_pixels / total_pixels)*100
        return difference_measure

    # Функция для выбора зоны на экране

def waterchoice():
    global source_choice
    source_choice = 1
    print("You picked water, so source choice now = ", source_choice)

def lavachoice():
    global source_choice
    source_choice = 2
    print("You picked lava, so source choice now = ", source_choice)

def clicked():
    global selected_zone
    selected_zone = select_zone()

def startprog():
    global stop, source_choice
    if source_choice == 1: #If user pick a water source
        delay_after_fish = 0.5
    elif source_choice == 2: #If user pick a lava source
        delay_after_fish = 1

    kblistener = keyboard.Listener(on_press=on_press)
    kblistener.start()
    image1 = get_screen_image(1)
    cv2.imshow("image1",image1)
    cv2.waitKey(0)
    while True:
        print("Started")
        # Получаем новое изображение
        image2 = get_screen_image(0)
        cv2.imwrite("resimg.png", image2)

        # Сравниваем изображение зоны с исходным изображением
        res = compare_images(image1, image2)
        
        if res >= 1.5:
            # Нажимаем лкм
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
            time.sleep(0.2)
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
            print("clicked, res = ", res)
            time.sleep(0.1)
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
            time.sleep(0.2)
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
            time.sleep(delay_after_fish)
            image2 = get_screen_image(0)
            time.sleep(delay_after_fish)
        else:
            print("res = ", res)

        if stop == 1:
            stop = 0
            break
        time.sleep(0.2)

# Основная функция
def main():
    global x1, y1, x2, y2, stop
    x1 = int(0)
    y1 = int(0)
    x2 = int(0)
    y2 = int(0)
    stop = 0
    
    root = Tk()

    root.title("Autofishing app")
    root.geometry('400x200')

    lbl = Label(root, text = "Press button to choose area")
    lbl.grid()
    select_btn = Button(root, text="Select area",
                 fg = "red", command=clicked)
    new_base_btn = Button(root, text="Get new base",
                 fg = "red", command=newbase)
    water_btn = Button(root, text="Water",
                 fg = "blue", command=waterchoice)
    lava_btn = Button(root, text="Lava",
                 fg = "red", command=lavachoice)
    reset_btn = Button(root, text="Reset coordinates",
                 fg = "red", command=reset_coords)
    start_btn = Button(root, text="Start",
                 fg = "red", command=startprog)
    select_btn.grid(column=1,row=0)
    new_base_btn.grid(column=1,row=1)
    water_btn.grid(column=2,row=0)
    lava_btn.grid(column=2,row=1)
    reset_btn.grid(column=3,row=0)
    start_btn.grid(column=3,row=1)
    root.mainloop()
    


if __name__ == "__main__":
    main()