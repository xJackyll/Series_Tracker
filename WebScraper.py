# WebScraper.py
#
# Data Creazione: 26/03/2021
# Ultima Modifica: 27/09/2023
# Versione: 3.0
# Autore: xJackyll
#
# Lo script non e' per niente scritto bene e a volte si bugga. Detto questo svolge bene il suo lavoro ed e' molto utile
# 
# N.B.  Non modificare lo script se non si ha chiaro cosa si sta facendo 


from tkinter import *
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time

# Change this variables if not running
Ico1 = "Arduino.ico"
Ico2 = "Nome_Anime.txt"
Last_Ep_Dir = "LAST_EPISODE.txt"
Nome_Anime_Dir = "Libro_Con_Amaterasu.ico"
ChromeUser_Dir = "C:\\Users\\user\\AppData\\Local\\Google\\Chrome\\User Data\\Default" # This is an exmple, put your own Chrome User Profile

Open_Text = open(Ico2, "r")
Nome_Animes = Open_Text.read()
Open_Text.close()

NUM_EP = ""
ics = 0

def animesaturn():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get("https://www.animesaturn.tv")



def Options():
    top = Toplevel()
    top.title("Menù opzioni")
    top.iconbitmap(Ico1)
    Bottone1_pt2 = Button(top, text="Immetti Ep Manualmente", padx=50, pady=50, command=bottone_anime_manuali, fg="black", bg="gold", activebackground="yellow", bd="5", cursor="pirate", font="italic, 15")
    Bottone1_pt2.pack()
    Bottone1_pt3 = Button(top, text="Cambia Anime", padx=96, pady=50, command=cambia_anime, fg="black", bg="gold", activebackground="yellow", bd="5", cursor="pirate", font="italic, 15")
    Bottone1_pt3.pack()

def bottone_anime_manuali():
    top2 = Toplevel()
    top2.title("Immetti il N° dell'episodio")
    top2.iconbitmap(Ico1)
    Spazio_Dove_Immettere_Ep = Entry(top2, width=35, borderwidth=5, textvariable=var)
    Bottone1_pt3 = Button(top2, text="Immetti ep", padx=30, pady=20, command=Get_Num_Ep, fg="black", bg="gold", activebackground="yellow", bd="5", cursor="pirate", font="italic, 15")
    Spazio_Dove_Immettere_Ep.pack()
    Bottone1_pt3.pack()

def Get_Num_Ep():
    global ics
    azzero_num_ep = open(Last_Ep_Dir, "w")
    azzero_num_ep.write(str(var.get()))
    azzero_num_ep.close()


def cambia_anime():
    top3 = Toplevel()
    top3.title("Jackyll")
    top3.iconbitmap(Ico1)
    Spazio_Dove_Immettere_Anime = Entry(top3, width=35, borderwidth=5, textvariable=var2)
    Bottone1_pt2 = Button(top3, text="Cambia Anime", padx=30, pady=20, command=Get_New_Anime, fg="black", bg="gold", activebackground="yellow", bd="5", cursor="pirate", font="italic, 15")
    Spazio_Dove_Immettere_Anime.pack()
    Bottone1_pt2.pack()


def Get_New_Anime():
    sostituisco_anime = open(Ico2, "w")
    sostituisco_anime.write(str(var2.get()))
    sostituisco_anime.close()
    azzero_num_ep2 = open(Last_Ep_Dir, "w")
    azzero_num_ep2.write("1")
    azzero_num_ep2.close()


def myclick(NOME):
    global NUM_EP
    a = open(Last_Ep_Dir, "r")
    N_EP = a.read()
    a.close()

    capa = DesiredCapabilities.CHROME
    capa["pageLoadStrategy"] = "none"

    options = webdriver.ChromeOptions()
    options.add_argument("user-data-dir=" + ChromeUser_Dir)
    options.add_experimental_option("excludeSwitches", ["enable-automation"])

    driver = webdriver.Chrome(options=options)

    # PAGE SCRAPING
    driver.maximize_window()
    driver.get("https://www.animesaturn.tv")

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'query'))).send_keys(NOME, Keys.ENTER)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[4]/ul[1]/li/div/div/h3/a'))).send_keys(Keys.ENTER)

    # NUM_EP
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[3]/div/div[2]/div[5]/div/div/div[1]/div[' + N_EP + ']/a'))).send_keys(Keys.ENTER)

    # SWITCH TAB & START THE EP
    driver.close()
    driver.switch_to.window(driver.window_handles[-1])

    # Click on the right ep  number
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[4]/div[1]/div/a[1]'))).send_keys(Keys.ENTER)

    # Try to autoplay the episode with two different possible element patterns (perche' alcune serie hanno diversi layout)
    try:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/center/div[2]/div/div/div/div/div/div/div/div[2]/div[4]/video'))).send_keys(Keys.ENTER)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/center/div[2]/div/div/div/div/div/div/div/div[2]/div[4]/video'))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/center/div[2]/div/div/div/div/div/div/div/div[2]/div[4]/video'))).click()

    except:
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, '/html/body/center/div[2]/div/div/div/div/div/button'))).send_keys(Keys.ENTER)
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, '/html/body/center/div[2]/div/div/div/div/div/div[8]/button'))).click()



    while 1 > 0:
        time.sleep(3)
        ep_corrente = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/center/div[2]/div/div/h4")))
        Num_ep_finale = ep_corrente.text[-2:]
        OPEN = open(Last_Ep_Dir, "w")
        NUM = OPEN.write(str(int(Num_ep_finale) + 1))
        OPEN.close()

        print("Current Episode: " + Num_ep_finale)


root = Tk()
root.title("Per Aspera Ad Astra")
root.iconbitmap(Nome_Anime_Dir)

var = IntVar()
var2 = StringVar()

frame = LabelFrame(root, text="ANIMES", bg="light grey")
frame.grid(row=0, column=0)
frame2 = LabelFrame(root, text=":)", bg="light grey")
frame2.grid(row=0, column=1)

Bottone = Button(frame, text=Nome_Animes, padx=50, pady=50, command=lambda: myclick(Nome_Animes), fg="black", bg="gold", activebackground="yellow", bd="5", cursor="heart", font="italic, 15")
Bottone3 = Button(frame2, text="EXIT PROGRAM", padx=50, pady=50, command=root.quit, fg="black", bg="gold", activebackground="yellow", bd="5", cursor="pirate", font="italic, 15")
Bottone5 = Button(frame, text="IMPOSTAZIONI", padx=55, pady=50, fg="black", bg="gold", activebackground="yellow", bd="5", cursor="pirate", font="italic, 15", command=Options)
Bottone4 = Button(frame2, text="ANIMESATURN", padx=55, pady=50, command=animesaturn, fg="black", bg="gold", activebackground="yellow", bd="5", cursor="pirate", font="italic, 15")
Bottone.grid()
Bottone5.grid()
Bottone4.grid()
Bottone3.grid()
root.mainloop()
