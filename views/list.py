import flet as ft
import requests
from bs4 import BeautifulSoup

class listBook(ft.View):
    def __init__(self,page:ft.Page):
        super().__init__(route="/listgender")
        self.page = page
        self.page.views.append(self)
        self.bottom_appbar = self.page.bottom_appbar
        
        self.scroll = "always"
        self.adaptive = True
        
        self.list_genders = ft.GridView(
            child_aspect_ratio=5,
            controls=[
                
            ]
        )
        link = requests.get("https://ww3.lectulandia.com/")
        link = link.text
        soup = BeautifulSoup(link, "html.parser")
        section = soup.find(id = "secgenero")
        a = section.find_all('a', class_ = "term")
        for i in a:
            titulo = i.text.strip()
            link_g = i['href']
            self.list_genders.controls.append(
                ft.TextButton(
                    text=f"{titulo}",
                    data=link_g,
                    on_click=self.gender
                )
            )
        self.horizontal_alignment = "center"
        self.main_screen = ft.Column(
                    horizontal_alignment="center",
                    controls=[
                        ft.Text("Generos",size=24),
                        self.list_genders
                    ]
                )
        self.controls.append(
            ft.SafeArea(
                content=self.main_screen
            )
        )
        self.page_number = 2
        self.page.update()
    
    def gender(self,e):
        value = e.control.data
        nombre = str(value).split("/")[2]
        self.main_screen.controls = []
        self.main_screen.controls.append(ft.ProgressBar())
        self.update()
        self.main_screen.controls = []
        self.main_screen.controls.append(
            ft.Text(f"{nombre}",size=24)
        )
        self.main_screen.controls.append(ft.Divider(height=10,color=ft.colors.WHITE10))
        pagina = requests.get(f"https://ww3.lectulandia.com{value}")
        data = pagina.text
        soup = BeautifulSoup(data, 'html.parser')
        cards = soup.find_all(class_='card')
        for card in cards:
            title = card.find('a', class_='title').text.strip()
            image_src = card.find('img')['src']
            book_link = card.find('a', class_='title')['href']
            self.main_screen.controls.append(
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
        self.update()
        try:
            extras = requests.get(f"https://ww3.lectulandia.com{value}/page/2/")
            if extras.status_code == 200:
                self.main_screen.controls.append(
                    ft.TextButton("Mostrar Más", data = f"https://ww3.lectulandia.com{value}/page/", on_click=self.show_more)
                )
            self.update()
        except Exception:
            pass
    
    def show_more(self,e):
        value = e.control.data
        self.main_screen.controls.pop()
        self.main_screen.controls.append(ft.ProgressBar())
        self.update()
        pagina = requests.get(f"{value}{self.page_number}/")
        self.page_number +=1
        data = pagina.text
        soup = BeautifulSoup(data, 'html.parser')
        cards = soup.find_all(class_='card')
        self.main_screen.controls.pop()
        for card in cards:
            title = card.find('a', class_='title').text.strip()
            image_src = card.find('img')['src']
            book_link = card.find('a', class_='title')['href']
            self.main_screen.controls.append(
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
        self.update()
        try:
            extras = requests.get(f"{value}{self.page_number}/")
            if extras.status_code == 200:
                self.main_screen.controls.append(
                    ft.TextButton("Mostrar Más", data = f"{value}{self.page_number}", on_click=self.show_more)
                )
            self.update()
        except Exception:
            pass


    def go_boock(self,e):
        data = e.control.data
        self.page.session.set("url",data)
        self.page.session.set("page","/listgender")
        self.page.go("/boock")