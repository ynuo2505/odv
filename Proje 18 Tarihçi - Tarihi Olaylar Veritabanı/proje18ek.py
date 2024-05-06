#-*- coding: cp1254 -*-
from tkinter import*
from tkinter import ttk
from tkinter import messagebox

def karsila():
    s1 = str(entadi.get())
    s2 = str(entsoyadi.get())
    s3 = str(entnumara.get())
    lblkarsilama['text'] = "Ho�geldin!\n " + s1 + " " + s2 + " (" + s3 + ")" + \
                           "\nNot Ortalamas� ve Ba�ar� Durumunuzu ��renmek i�in " \
                           "S�nav Notlar�n�z� a�a��daki kutucuklara yazabilirsin..."

    cbolum.current(0)
    entnumara.delete(0, "end")
    entsoyadi.delete(0, "end")
    entadi.delete(0, "end")

def ortalama():
    s1 = int(entvize.get())
    s2 = int(entfinal.get())
    s3 = int(s1 * 20 / 100) + int(s2 * 50 / 100)
    lblnotortalamasi['text'] = s3

def basari():
    s1 = int(entvize.get())
    s2 = int(entfinal.get())
    s3 = int(s1 * 20 / 100) + int(s2 * 50 / 100)
    if s3 >= 60:
        lblbasaridurumu['text'] = "Ge�ti"
    else:
        lblbasaridurumu['text'] = "Kald�"

win = Tk()
win.title("��RENC� NOT TAK�P")
win.geometry("1000x860")
win.resizable(FALSE, FALSE)

lblbaslik = Label(win, text="��RENC� NOT TAK�P S�STEM�", font="Verdana 16 bold", fg="red")
lblbaslik.place(x=230, y=10)

lbladi = Label(win, text="��rencinin Ad�", font="Verdana 10 bold")
lbladi.place(x=40, y=70)
lblsoyadi = Label(win, text="��rencinin Soyad�", font="Verdana 10 bold")
lblsoyadi.place(x=500, y=70)
lblnumara = Label(win, text="��renci Okul No", font="Verdana 10 bold")
lblnumara.place(x=40, y=120)
lblbolum = Label(win, text=" B�l�m", font="Verdana 10 bold")
lblbolum.place(x=500, y=120)

lblvize = Label(win, text=" Al�nan Vize Notu", font="Verdana 10 bold")
lblvize.place(x=40, y=350)
lblfinal = Label(win, text=" Al�nan Final/B�t�nleme  Notu", font="Verdana 10 bold ")
lblfinal.place(x=40, y=450)

lblkarsilama = Label(win, font="Verdana 10 bold")
lblkarsilama.place(x=50, y=240)

lblnotortalamasi = Label(win, font="Verdana 10 bold", fg="blue")
lblnotortalamasi.place(x=750, y=400)
lblbasaridurumu = Label(win, font="Verdana 10 bold", fg="blue")
lblbasaridurumu.place(x=740, y=500)

lblnot = Label(win, text="Not:S�nav puanlar� hesaplamas�nda V�ZE notunun %20'si \n"
                         "F�NAL Notunun %80'i al�narak toplan�r. \n"
                         "Not ortalamas�n�n 60 �zeri olmas� durumunda dersten ge�ilir.", font="Verdana 12 bold ")
lblnot.place(x=40, y=540)

entadi = Entry(win, font="Verdana 10 bold", fg="blue", width=22)
entadi.place(x=240, y=70)
entsoyadi = Entry(win, font="Verdana 10 bold", fg="blue", width=22)
entsoyadi.place(x=690, y=70)
entnumara = Entry(win, font="Verdana 10 bold", fg="blue", width=22)
entnumara.place(x=240, y=120)
entvize = Entry(win, font="Verdana 10 bold", fg="blue", width=22)
entvize.place(x=250, y=350)
entfinal = Entry(win, font="Verdana 10 bold", fg="blue", width=22)
entfinal.place(x=250, y=450)

cbolum = ttk.Combobox(win, font="Verdana 10 bold")
cbolum['values'] = ("Okudu�unuz B�l�m� Se�iniz...", "Bilgisayar Programc�l���", "Hukuk", "Mimarl�k", "��letme"
                    "M�hendislik Fak�ltesi", "Eczac�l�k Fak�ltesi", "T�p Fak�ltesi", "�ktisat Fak�ltesi")

cbolum.current(0)
cbolum.place(x=690, y=120)

btnkaydet = Button(win, text="Sisteme Giri�", font="Verdana 10 bold", fg="blue", command=karsila)
btnkaydet.place(x=430, y=190)
btnnotortalamasi = Button(win, text="Not Ortalamas�", font="Verdana 10 bold", fg="blue", command=ortalama)
btnnotortalamasi.place(x=690, y=350)
btnbasaridurumu = Button(win, text="Ba�ar� Durumu", font="Verdana 10 bold", fg="blue", command=basari)
btnbasaridurumu.place(x=690, y=450)

win.mainloop()
