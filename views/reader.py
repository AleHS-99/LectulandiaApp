import flet as ft

class ReadBook(ft.View):
    def __init__(self,page:ft.Page):
        super().__init__(route="/read")
        self.page = page
        self.page.views.append(self)
        self.bottom_appbar = self.page.bottom_appbar
        
        