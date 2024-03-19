import flet as ft
import requests
from bs4 import BeautifulSoup
import threading

class SearchView(ft.View):
    def __init__(self,page:ft.Page):
        super().__init__(route="/search", bottom_appbar = page.bottom_appbar)
        self.page = page
        
        self.page.views.append(self)        

        self.list_boocks = ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls = []
        )
        self.page_number = 2
        self.main_screen = ft.Container(
            padding=ft.padding.only(top=20,left=15,right=15),
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Stack(
                        right=True,
                        controls=[
                            ft.TextField(label="Buscar....",color=ft.colors.WHITE, border_color=ft.colors.WHITE,
                                         on_submit=self.search),
                            ft.IconButton(icon=ft.icons.SEARCH,icon_color=ft.colors.RED_600,right=0,
                                          style=ft.ButtonStyle(
                                              padding=ft.Padding(0, 10, 0, 0),
                                          ), on_click=self.search)
                        ]
                    ),
                    ft.Divider(height=5,color=ft.colors.WHITE10),
                    self.list_boocks
                ]
            )
        )
        
        self.controls.append(ft.SafeArea(content=self.main_screen))
        self.scroll="always"
        self.page.update()

    def search(self,e):
        self.list_boocks.controls = []
        self.list_boocks.controls.append(
            ft.ProgressBar()
        )
        self.bottom_appbar = self.page.bottom_appbar
        self.page.update()
        value = self.main_screen.content.controls[0].controls[0].value
        parse_value = str(value).replace(" ","+")
        search_link = f"https://ww3.lectulandia.com/search/{parse_value}"
        page_ = requests.get(search_link)
        data = page_.text
        soup = BeautifulSoup(data, 'html.parser')
        cards = soup.find_all(class_='card')
        self.list_boocks.controls = []
        for card in cards:
            title = card.find('a', class_='title').text.strip()
            image_src = card.find('img')['src']
            book_link = card.find('a', class_='title')['href']
            self.list_boocks.controls.append(
                ft.TextButton(
                    content=ft.Column(
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Image(
                                src=image_src,
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
        extras = requests.get(f"https://ww3.lectulandia.com/search/{parse_value}/page/{self.page_number}/")
        if extras.status_code == 200:
            self.list_boocks.controls.append(
                ft.TextButton("Mostrar Más", data = f"https://ww3.lectulandia.com/search/{parse_value}/page/", on_click=self.show_more)
            )
            self.update()
        self.page.update()

    def show_more(self, e):
        value = e.control.data
        self.list_boocks.controls.pop()
        self.list_boocks.controls.append(ft.ProgressBar())
        self.update()
        pagina = requests.get(f"{value}{self.page_number}/")
        self.page_number +=1
        data = pagina.text
        soup = BeautifulSoup(data, 'html.parser')
        cards = soup.find_all(class_='card')
        self.list_boocks.controls.pop()
        for card in cards:
            title = card.find('a', class_='title').text.strip()
            image_src = card.find('img')['src']
            book_link = card.find('a', class_='title')['href']
            self.list_boocks.controls.append(
                ft.TextButton(
                    content=ft.Column(
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Image(
                                src=image_src,
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
        extras = requests.get(f"{value}{self.page_number}")
        if extras.status_code == 200:
            self.list_boocks.controls.append(
                ft.TextButton("Mostrar Más", data = f"{value}{self.page_number}", on_click=self.show_more)
            )
            self.update()
        self.update()


    def go_boock(self,e):
        data = e.control.data
        self.page.session.set("url",data)
        self.page.session.set("page","/search")
        self.page.go("/boock")
