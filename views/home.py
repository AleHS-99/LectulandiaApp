import flet as ft
import requests
from bs4 import BeautifulSoup
import threading


class homeView(ft.View):
    def __init__(self, page:ft.Page):
        super().__init__(route="/", bottom_appbar=page.bottom_appbar)
        
        self.page = page
        
        self.page.views.append(self)
        #self.bottom_appbar = self.page.bottom_appbar
        
        self.boock_list = ft.GridView(
            expand=True,
            horizontal=True,
            child_aspect_ratio=1.65
        )
           
        self.lo_mas_semana = ft.GridView(
            expand=True,
            horizontal=True,
            child_aspect_ratio=1.65
        )
        #self.scroll = "always"   
        home_screen = ft.Container(
            padding=ft.padding.only(top=20,left=15,right=15),
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Text(
                        "Lectulandia Downloader",
                        size=15,
                        weight="bold"
                    ),
                    ft.Divider(height=5,color="white10"),
                    ft.Container(
                        height=280,
                        content=ft.Column(
                            controls=[
                                ft.Row(
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    controls=[
                                        ft.Text("Las últimas novedades", size=14)
                                    ]
                                ),
                                self.boock_list
                            ]
                        )
                    ),
                    ft.Divider(height=5,color="white10"),
                    ft.Container(
                        height=280,
                        content=ft.Column(
                            controls=[
                                ft.Row(
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    controls=[
                                        ft.Text("Los más leídos de la semana", size=14)
                                    ]
                                ),
                                self.lo_mas_semana
                            ]
                        )
                    )
                ]
            )
        )
        self.adaptive = True
        self.scroll = "always"
        self.controls.append(ft.SafeArea(content=home_screen))
        page.update()
        load1 = threading.Thread(target=self.loading_books1)
        load2 = threading.Thread(target=self.loading_books2)
        load1.start()
        load2.start()
        load2.join()
    
    def loading_books1(self):
        ultimas_novedades = requests.get("https://ww3.lectulandia.com/book/#post-114232")
        
        data = ultimas_novedades.text
        soup = BeautifulSoup(data, 'html.parser')
        cards = soup.find_all(class_='card')
        
        for card in cards:
            title = card.find('a', class_='title').text.strip()
            image_src = card.find('img')['src']
            book_link = card.find('a', class_='title')['href']
            self.boock_list.controls.append(
                ft.TextButton(
                    content=ft.Column(
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Image(
                                src=image_src,
                                #width=200,
                                height=180,
                                fit=ft.ImageFit.NONE,
                                repeat=ft.ImageRepeat.NO_REPEAT,
                                border_radius=ft.border_radius.all(10),
                            ),
                            ft.Text(f"{title}", color="white"),
                        ]
                    ),
                    style=ft.ButtonStyle(
                        color={
                            ft.MaterialState.HOVERED: ft.colors.WHITE,
                            ft.MaterialState.FOCUSED: ft.colors.BLUE,
                            ft.MaterialState.DEFAULT: ft.colors.BLACK,
                        }
                    ),
                    data=book_link,
                    on_click=self.go_boock
                )
            )
        self.page.update()
         
    def loading_books2(self):
        lm_semana = requests.get("https://ww3.lectulandia.com/compartidos-semana/")
        data = lm_semana.text
        soup = BeautifulSoup(data, 'html.parser')
        cards2 = soup.find_all(class_='card')
        for card in cards2:
            title = card.find('a', class_='title').text.strip()
            author = card.find('div', class_='subdetail').a.text.strip()
            description = card.find('div', class_='description').p.text.strip()
            image_src = card.find('img')['src']
            book_link = card.find('a', class_='title')['href']
            self.lo_mas_semana.controls.append(
                ft.TextButton(
                    content=ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Image(
                            src=image_src,
                            #width=200,
                            height=180,
                            fit=ft.ImageFit.NONE,
                            repeat=ft.ImageRepeat.NO_REPEAT,
                            border_radius=ft.border_radius.all(10),
                        ),
                        ft.Text(f"{title}", color="white"),
                    ]
                ),
                    data=book_link,
                    on_click=self.go_boock
                )
                
            )
        self.page.update()
    
    def go_boock(self,e):
        data = e.control.data
        self.page.session.set("url",data)
        self.page.session.set("page","/")
        self.page.go("/boock")
