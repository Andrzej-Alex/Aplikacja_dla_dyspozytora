import os
import wx
import wx.grid as grid
from collections import defaultdict, deque
import sqlite3
from datetime import datetime
import dijkstra as dij
from datetime import datetime, date
from datetime import timedelta
import time

graph = dij.Graph()
db = sqlite3.connect('ASJW.db')
db.row_factory = sqlite3.Row
kursor = db.cursor()
kursor.execute(
        """
        SELECT miejscowosc_A, miejscowosc_B, czas FROM PUNKTY_MAPY
        """)
punkty = kursor.fetchall()
zbior = list()
z = list()
s = list()
t = list()
for PUNKTY_MAPY in punkty:
    z.append(PUNKTY_MAPY['miejscowosc_A'])
    s.append(PUNKTY_MAPY['miejscowosc_B'])
    t.append(PUNKTY_MAPY['czas'])
zbior = z + s
        
for node in zbior:
    graph.add_node(node)

i = 0
while i < len(z):
    graph.add_edge(str(z[i]), str(s[i]), int(t[i]))
    i = i + 1

newzbior = list(dict.fromkeys(zbior))
newzbior = sorted(newzbior)
newzbior.remove('A')
newzbior.remove('B')
newzbior.remove('C')
newzbior.remove('D')
newzbior.remove('E')
newzbior.remove('F')

class PanelOne(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent, size=(800,100))
        self.quote = wx.StaticText(self,label="Witaj w aplikacji:", pos=(35,30))
        font = wx.Font(18, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        self.quote.SetFont(font)

class PanelZlecDodaj(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent, size=(800,500), pos=(0,110))
        font = wx.Font(18, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        font2 = wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        self.miejscA = str()
        self.miejscB = str()
        self.ciezar = str()
        self.kierowca = str()
        self.quote = wx.StaticText(self, label="Trwa dodawanie zlecenia...", pos=(10, 10))
        self.quote.SetFont(font)
        self.sampleList = newzbior
        self.lblhear1 = wx.StaticText(self, label="Miejscowosc poczatkowa:", pos=(10, 80))
        self.lblhear1.SetFont(font)
        self.edithear1 = wx.ComboBox(self, pos=(350, 80), size=(150,30), choices=self.sampleList, style=wx.CB_DROPDOWN)
        self.edithear1.SetFont(font2)
        self.Bind(wx.EVT_COMBOBOX, self.MiejscA, self.edithear1)
        self.lblhear2 = wx.StaticText(self, label="Miejscowosc koncowa:", pos=(10, 140))
        self.lblhear2.SetFont(font)
        self.edithear2 = wx.ComboBox(self, pos=(350, 140), size=(150,30), choices=self.sampleList, style=wx.CB_DROPDOWN)
        self.edithear2.SetFont(font2)
        self.Bind(wx.EVT_COMBOBOX, self.MiejscB, self.edithear2)
        waga = ['100', '200', '300', '400', '500', '600', '700', '800', '900', '1000']
        self.sampleList2 = waga
        self.lblhear3 = wx.StaticText(self, label="Waga:", pos=(10, 200))
        self.lblhear3.SetFont(font)
        self.edithear3 = wx.ComboBox(self, pos=(350, 200), choices=self.sampleList2, style=wx.CB_DROPDOWN)
        self.edithear3.SetFont(font2)
        self.Bind(wx.EVT_COMBOBOX, self.Ciezar, self.edithear3)
        self.buttonZlec = wx.Button(self, label="Dodaj", pos=(600,340))
        self.buttonZlec.SetFont(font2)
        self.Bind(wx.EVT_BUTTON, self.OnClickZlec, self.buttonZlec)
        self.buttonZlec2 = wx.Button(self, label="Wyjdź", pos=(500,340))
        self.buttonZlec2.SetFont(font2)
        self.Bind(wx.EVT_BUTTON, self.wyjdz, self.buttonZlec2)

    def MiejscA(self, event):
        self.miejscA = event.GetString()

    def MiejscB(self, event):
        self.miejscB = event.GetString()

    def Ciezar(self, event):
        self.ciezar = event.GetString()

    def OnClickZlec(self, event):
        if self.miejscA == '' or self.miejscB == '' or self.ciezar == '':
            bladZlec = wx.MessageDialog(self, "Wybierz wszystkie pozycje", "Błąd wyboru", wx.OK)
            bladZlec.ShowModal()
            bladZlec.Destroy()
        else:
            # można dodać info czy jestes pewny
            now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            task = (self.miejscA, self.miejscB, self.ciezar, now)
            sql = """ INSERT INTO Zlecenia(skad,dokad,masa,data_przyjscia) VALUES(?,?,?,?) """
            kursor.execute(sql, task)
            db.commit()
            
            kursor.execute(
                """
                SELECT ID_zlecenia FROM zlecenia
                """)
            zlecenia = kursor.fetchall()
            for ID_zlecenia in zlecenia:
                aktualne = ID_zlecenia
            sql2 = """ INSERT INTO Wykonania(ID_zlecenia,ID_samochodu,data_wykonania) VALUES(?,NULL,NULL) """
            kursor.execute(sql2, aktualne)
            db.commit()
            self.potwierdzenie = wx.StaticText(self, label="Dodano zlecenie do bazy...", pos=(10, 260))
            self.potwierdzenie.Hide()

    def wyjdz(self, e):
        self.Hide()

class PanelZlecPrzydziel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent, size=(800,500), pos=(0,110))
        font = wx.Font(18, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        font2 = wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        self.wiadomosc = wx.StaticText(self, label="Lista wolnych zleceń:", pos=(10, 10))
        self.wiadomosc.SetFont(font)
        kursor.execute(
        """
        SELECT ID_zlecenia, skad, dokad, masa, data_przyjscia FROM Zlecenia NATURAL JOIN Wykonania WHERE ID_samochodu IS NULL ORDER BY data_przyjscia
        """)
        wykonania = kursor.fetchall()
        self.pier = list()
        self.dwa = list()
        self.trzy = list()
        lista = list()
        
        for i in wykonania:
            self.pier.append(i['skad'])
            self.dwa.append(i['dokad'])
            self.trzy.append(i['ID_zlecenia'])
            lista.append(i['skad'] + ":" + i['dokad'] + " - " + str(i['masa']) + " - " + i['data_przyjscia'])
        if len(lista) == 0:
            self.napis = wx.StaticText(self, label="0", pos=(250,10))
            self.napis.SetFont(font)
        else:
            self.listbox = wx.ListBox(self, pos=(10, 60), size=(770, 320))
            self.listbox.SetFont(font2)
            self.Bind(wx.EVT_LISTBOX, self.skad, self.listbox) 
            self.listbox.InsertItems(lista,0)
            self.buttonPrzydziel = wx.Button(self, label="Przydziel kierowcę", pos=(10,430), size=(150,30))
            self.buttonPrzydziel.SetFont(font2)
            self.Bind(wx.EVT_BUTTON, self.PrzydzielKier, self.buttonPrzydziel)

    def skad(self, event):
        self.skad = self.listbox.GetSelection()
        self.pier1 = self.pier[self.skad]
        self.dwa1 = self.dwa[self.skad]
        self.trzy1 = self.trzy[self.skad]

    def PrzydzielKier(self, event):
        font = wx.Font(18, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        font2 = wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        self.listbox.Hide()
        self.buttonPrzydziel.Hide()
        self.ppaarr11 = wx.StaticText(self, label="Miejscowosc poczatkowa:", pos=(10, 80))
        self.ppaarr11.SetFont(font)
        self.par1 = wx.StaticText(self, label="%s" %self.pier1, pos=(350, 80))
        self.par1.SetFont(font)
        self.ppaarr22 = wx.StaticText(self, label="Miejscowosc koncowa:", pos=(10, 140))
        self.ppaarr22.SetFont(font)
        self.par2 = wx.StaticText(self, label="%s" %self.dwa1, pos=(350, 140))
        self.par2.SetFont(font)
        kursor.execute(
                """
                SELECT id_samochodu, miejsce_przebywania FROM SAMOCHODY WHERE miejsce_przebywania IS NOT NULL
                """)
        kierowcy = kursor.fetchall()
        k = list()
        m = list()
        for SAMOCHODY in kierowcy:
            k.append(SAMOCHODY['miejsce_przebywania'])
            m.append(SAMOCHODY['id_samochodu'])
        w = {}
        e = {}
        for i in range(len(k)):
            w[m[i]],e[m[i]] = dij.shortest_path(graph, str(k[i]), self.pier1)
        lista = sorted(w.items(), key=lambda x: x[1])
        lista2 = []
        self.idkierowcy = list()
        self.czas = list()
        for elem in lista:
            self.idkierowcy.append(int(elem[0]))
            self.czas.append(int(elem[1]))
            lista2.append(str(elem[0]) + "::" + str(elem[1]) + "min")
        self.sampleList3 = lista2
        self.edithear4 = wx.ComboBox(self, pos=(350,200), size=(150,30), choices=self.sampleList3, style=wx.CB_DROPDOWN)
        self.edithear4.SetFont(font2)
        self.Bind(wx.EVT_COMBOBOX, self.Kierowca, self.edithear4)
        self.buttonEnd1 = wx.Button(self, label="Zaakceptuj", pos=(600,340), size=(150,30))
        self.buttonEnd1.SetFont(font2)
        self.Bind(wx.EVT_BUTTON, self.OnClickAccept, self.buttonEnd1)

    def Kierowca(self, event):
        self.kierowca = event.GetSelection()
        self.kierowcaID = self.idkierowcy[self.kierowca]
        self.podroz = self.czas[self.kierowca]

    def OnClickAccept(self, event):
        if self.kierowca == '':
            bladZlec2 = wx.MessageDialog(self, "Wybierz kierowcę", "Błąd wyboru kierowcy", wx.OK)
            bladZlec2.ShowModal()
            bladZlec2.Destroy()
        else:
            kursor.execute(
                """
                UPDATE Wykonania
                SET ID_samochodu = ?
                WHERE ID_zlecenia = ?
                """, (self.kierowcaID, self.trzy1))
            db.commit()
            kursor.execute(
                """
                UPDATE Samochody
                SET miejsce_przebywania = ?
                WHERE ID_samochodu = ?
                """, (None, self.kierowcaID))
            db.commit()
            czas_podrozy, droga = dij.shortest_path(graph, self.pier1, self.dwa1)
            czas_podrozy2 = czas_podrozy + self.podroz + 30
            data_wyk = datetime.now() + timedelta(seconds=czas_podrozy2)
            kursor.execute(
                """
                UPDATE Wykonania
                SET data_wykonania = ?
                WHERE ID_zlecenia = ?
                """, (data_wyk,self.trzy1))
            db.commit()

            potwierdzenie2 = wx.MessageDialog(self, "Przydzielono kierowcę do zlecenia", "Potwierdzenie", wx.OK)
            potwierdzenie2.ShowModal()
            potwierdzenie2.Destroy()
            self.Hide()

class PanelZlecPrzegladaj(wx.Panel):
    def __init__ (self, parent):
        wx.Panel.__init__(self, parent=parent, size=(800,500), pos=(0,110))
        font = wx.Font(18, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        font2 = wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        self.wiadomosc = wx.StaticText(self, label="Lista zleceń:", pos=(10, 10))
        self.wiadomosc.SetFont(font)
        kursor.execute(
            """
            SELECT samochody.ID_samochodu, ID_zlecenia, skad, dokad, masa, data_przyjscia, data_wykonania FROM Samochody NATURAL JOIN (Wykonania NATURAL JOIN Zlecenia)
            """)
        przeglad = kursor.fetchall()
        sam = list()
        zle = list()
        ska = list()
        dok = list()
        mas = list()
        dat_p = list()
        dat_w = list()
        for p in przeglad:
            sam.append(p['ID_samochodu'])
            zle.append(p['ID_zlecenia'])
            ska.append(p['skad'])
            dok.append(p['dokad'])
            mas.append(p['masa'])
            dat_p.append(p['data_przyjscia'])
            dat_w.append(p['data_wykonania'])
        self.grid1 = grid.Grid(self, pos=(10, 60), size=(770,350))
        self.grid1.CreateGrid(len(sam), 7)

        self.grid1.SetColLabelValue(0, "ID Zlecenia")
        self.grid1.SetColLabelValue(1, "Data przyjścia")
        self.grid1.SetColLabelValue(2, "Miejsc. początkowa")
        self.grid1.SetColLabelValue(3, "Miejsc. końcowa")
        self.grid1.SetColLabelValue(4, "Masa [kg]")
        self.grid1.SetColLabelValue(5, "Kierowca")
        self.grid1.SetColLabelValue(6, "Data zakończenia")

        for i in range(len(sam)):
            self.grid1.SetCellValue(i,0, str(zle[i]))
            self.grid1.SetReadOnly(i,0, True)
            self.grid1.SetCellValue(i,1, dat_p[i])
            self.grid1.SetReadOnly(i,1, True)
            self.grid1.SetCellValue(i,2, ska[i])
            self.grid1.SetReadOnly(i,2, True)
            self.grid1.SetCellValue(i,3, dok[i])
            self.grid1.SetReadOnly(i,3, True)
            self.grid1.SetCellValue(i,4, str(mas[i]))
            self.grid1.SetReadOnly(i,4, True)
            self.grid1.SetCellValue(i,5, str(sam[i]))
            self.grid1.SetReadOnly(i,5, True)
            self.grid1.SetCellValue(i,6, dat_w[i])
            self.grid1.SetReadOnly(i,6, True)

        self.grid1.AutoSizeColumns(True)
        self.grid1.AutoSizeRows(True)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.grid1, 1, wx.EXPAND|wx.ALL)
        self.SetSizer(sizer)
        self.button5 = wx.Button(self, label="Wyjdź", pos=(10,430), size=(150,30))
        self.button5.SetFont(font2)
        self.Bind(wx.EVT_BUTTON, self.zakprzeg, self.button5)

    def zakprzeg(self, e):
        self.Hide()
        
class Okno(wx.Frame):
    def __init__(self,parent,title):
        wx.Frame.__init__(self,parent,title=title,size=(810,700))
        self.panel_one = PanelOne(self)
        self.panel_zlec_dodaj = PanelZlecDodaj(self)
        self.panel_zlec_dodaj.Hide()
        self.panel_zlec_przydziel = PanelZlecPrzydziel(self)
        self.panel_zlec_przydziel.Hide()
        self.panel_zlec_przegladaj = PanelZlecPrzegladaj(self)
        self.panel_zlec_przegladaj.Hide()
        self.CreateStatusBar()

        menubar = wx.MenuBar()
        
        menu1 = wx.Menu()
        DodajZlec = menu1.Append(wx.ID_ANY, "Dodaj", "Dodaje zlecenie")
        PrzydzielZlec = menu1.Append(wx.ID_ANY, "Przydziel pojazd", "Przydziela kierowcę do zlecenia")
        PrzegladajZlec = menu1.Append(wx.ID_ANY, "Przegladaj", "Przeglądaj zlecenia")

        menubar.Append(menu1,"Zlecenia")
        self.SetMenuBar(menubar)
        
        menu2 = wx.Menu()
        #DodajKier = menu2.Append(wx.ID_ANY, "Dodaj", "Dodaje kierowców")
        PrzegladajKier = menu2.Append(wx.ID_ANY, "Przegladaj", "Przeglądaj kierowców")

        menubar.Append(menu2,"Kierowcy")
        self.SetMenuBar(menubar)
        
        menu3 = wx.Menu()
        Pomoc = menu3.Append(wx.ID_ABOUT, "Pomoc", "Menu pomocy")
        Wyjscie = menu3.Append(wx.ID_EXIT, "Zamknij", "Zamyka okno")

        menubar.Append(menu3,"Opcje")
        self.SetMenuBar(menubar)

        #TIMER REFRESH

        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.OnRefresh)
        self.timer.Start(10000)

        #EVENTS

        self.Bind(wx.EVT_MENU, self.DodZlec, DodajZlec)
        self.Bind(wx.EVT_MENU, self.PrzydzZlec, PrzydzielZlec)
        self.Bind(wx.EVT_MENU, self.PrzegZlec, PrzegladajZlec)

        #self.Bind(wx.EVT_MENU, self.DodKier, DodajKier)
        #self.Bind(wx.EVT_MENU, self.PrzegKier, PrzegladajKier)
        
        self.Bind(wx.EVT_MENU, self.OnHelp, Pomoc)
        self.Bind(wx.EVT_MENU, self.OnExit, Wyjscie)

    def OnRefresh(self, e):
        kursor.execute(
            """
            SELECT samochody.ID_samochodu, MAX(data_wykonania), dokad, ID_wykonania FROM Samochody NATURAL JOIN (Wykonania NATURAL JOIN Zlecenia) GROUP BY samochody.ID_samochodu
            """)
        daty_wykon = kursor.fetchall()
        auto = list()
        datawyk = list()
        cel = list()
        wykon = list()
        for DATY in daty_wykon:
            auto.append(DATY['ID_samochodu'])
            datawyk.append(DATY['MAX(data_wykonania)'])
            cel.append(DATY['dokad'])
            wykon.append(DATY['ID_wykonania'])
        kursor.execute(
            """
            SELECT datetime('now', 'localtime')
            """)
        teraz = kursor.fetchall()
        teraz2 = list()
        for TERAZ3 in teraz:
            teraz2.append(TERAZ3["datetime('now', 'localtime')"])
        kursor.execute(
            """
            SELECT ID_wykonania FROM Zakonczenia
            """)
        zakon = kursor.fetchall()
        zakoncz = list()
        for ZAKONC in zakon:
            zakoncz.append(ZAKONC['ID_wykonania'])
        for (p,q,r,s) in zip(auto,datawyk,cel,wykon):
            if q < teraz2[0]:
                kursor.execute(
                    """
                    UPDATE Samochody
                    SET miejsce_przebywania = ?
                    WHERE ID_samochodu = ?
                    """, (r,p))
                db.commit()
                if s in zakoncz:
                    continue
                else:
                    sql4 = """ INSERT INTO Zakonczenia(data_zakonczenia, ID_wykonania) VALUES(?,?) """
                    task4 = (q, s)
                    kursor.execute(sql4, task4)
                    db.commit()
            else:
                print('*')
        print('elo')
        
    def DodZlec(self, e):
        self.panel_zlec_przegladaj.Hide()
        self.panel_zlec_przydziel.Hide()
        self.panel_zlec_dodaj = PanelZlecDodaj(self)
        self.panel_zlec_dodaj.Show()

    def PrzydzZlec(self, e):
        self.panel_zlec_przegladaj.Hide()
        self.panel_zlec_dodaj.Hide()
        self.panel_zlec_przydziel = PanelZlecPrzydziel(self)
        self.panel_zlec_przydziel.Show()

    def PrzegZlec(self, e):
        self.panel_zlec_przydziel.Hide()
        self.panel_zlec_dodaj.Hide()
        self.panel_zlec_przegladaj = PanelZlecPrzegladaj(self)
        self.panel_zlec_przegladaj.Show()
    
    def OnHelp(self, e):
        dialog = wx.MessageDialog(self, "W celu uzyskania pomocy pisz do jedrekwisniewski@wp.pl", "Okno Pomocy", wx.OK)
        dialog.ShowModal()
        dialog.Destroy()
        
    def OnExit(self,e):
        db.close()
        self.Close()
        
app = wx.App(False)
frame = Okno(None, "Aplikacja dyspozytora")
frame.Show()
app.MainLoop()
