import flet as ft
import requests
import time
from bs4 import BeautifulSoup
import werkzeug
werkzeug.cached_property = werkzeug.utils.cached_property
from robobrowser import RoboBrowser
import os

class BoockInfo(ft.View):
    def __init__(self,page:ft.Page):
        super().__init__(route="/boock")
        self.page = page
        self.page.views.append(self)
        self.bottom_appbar = self.page.bottom_appbar
        
        book_url = self.page.session.get("url")
        go_back = self.page.session.get("page")
        book = requests.get(f"https://ww3.lectulandia.com{book_url}")
        data = book.text
        soup = BeautifulSoup(data, 'html.parser')
        titulo = soup.find('div', id='title').h1.text
        self.titulo = titulo

        # Extraer la fuente de la imagen de portada
        imagen_portada = soup.find('div', id='cover').img['src']

        # Extraer el autor del libro
        autor = soup.find('div', id='autor').a.text
        # Extraer la sinopsis del libro
        sinopsis = ""
        try:
            sinopsis = soup.find('div', id='sinopsis').span.text
        except Exception:
            try:
                sinopsis = soup.find('div', id='description').span.text
            except Exception:
                try:
                    sinopsis = soup.find('div', id='sinopsis').p.text
                except Exception:
                    try:
                        sinopsis = soup.find('p', class_='description').text
                    except Exception:

                        sinopsis = "No hay descripción disponible"
        
        # Extraer el enlace relacionado al libro
        enlace_libro = soup.find('div', id='downloadContainer').a['href']

        prueba = requests.get(f"https://ww3.lectulandia.com{enlace_libro}")
        data = prueba.text
        soup = BeautifulSoup(data, 'html.parser')
        scripts = soup.find_all('script',type='text/javascript')
        linkCode_value = ''

        for i in scripts:
            content = i.string
            for line in str(content).splitlines():
                if 'var linkCode' in line:
                    linkCode_value = line.split('=')[1].strip().strip('";')
                    break
        download_link = f"https://www.antupload.com/file/{linkCode_value}"
        self.controls.append(
            ft.SafeArea(
                content=ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Row(
                            controls=[
                                ft.IconButton(icon=ft.icons.ARROW_BACK, icon_color='white', on_click= lambda x: self.page.go(go_back))
                            ]
                        ),
                        ft.Divider(height=5,color='transparent'),
                        ft.Text(f"{titulo}", size=18,weight="bold"),
                        ft.Image(src=f"{imagen_portada}",
                                height=180,
                                    fit=ft.ImageFit.FILL,
                                    repeat=ft.ImageRepeat.NO_REPEAT,
                                    border_radius=ft.border_radius.all(10),),
                        ft.Text(f"{autor}"),
                        ft.TextButton("Descargar", data=download_link,icon=ft.icons.DOWNLOAD,icon_color="white",on_click=self.download),
                        ft.Text(sinopsis)
                        
                    ]
                )
            )
            
        )
        self.scroll="always"
        self.page.update()
        
    def download(self,e):
        dlg_modal = ft.AlertDialog(
            modal=True,
            title=ft.Text("Descargando"),
            content=ft.Column(
              controls=[
                  ft.Text("Por favor espere"),
                  ft.ProgressRing(stroke_width=20)
              ],
              height=100,
              horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ),
            actions_alignment=ft.MainAxisAlignment.END,
        )
        self.page.dialog = dlg_modal
        dlg_modal.open = True
        self.page.update()
        try:
            pagina = requests.get(e.control.data)
            data  = pagina.text
            soup = BeautifulSoup(data,"html.parser")
            a = soup.find('div',id='fileDownload').a['href']
            link_book = f"https://www.antupload.com{a}"
            session = requests.Session()
            browser = RoboBrowser(history=True, parser='html.parser', session=session)
            browser.open(link_book)

            filename = browser.find(
                    "div", id="fileDescription").find_all("p")[1].text.replace(
                        "Name: ", "")
            file_url = browser.find("a", id="downloadB")
            time.sleep(2)
            browser.follow_link(file_url)
            with open(f"/sdcard/Download/{filename}", "wb") as epub_file:
                epub_file.write(browser.response.content)
            dlg_modal.content = ft.Text("Descarga Realizada")
            self.page.update()
            time.sleep(2)
        except Exception:
            dlg_modal.content = ft.Text("Descarga fallida, revise su conexion a internet.")
            self.page.update()
            time.sleep(2)
        self.page.update()
        
        