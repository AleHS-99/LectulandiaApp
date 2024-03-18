import flet as ft
from views import home, book, list, search


def main(page: ft.Page):
    """
    The on route function its for whe you pass the page.go() property
    it will loock for what is on you route and show the view that you define
    """
    def route_change(route):
        if page.route == "/":
            home.homeView(page)
        if page.route == "/boock":
            book.BoockInfo(page)
        if page.route == "/listgender":
            list.listBook(page)
        if page.route == "/search":
            search.SearchView(page) 

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)
        
    page.on_route_change = route_change
    page.theme_mode = 'dark'
    page.on_view_pop = view_pop
    page.bottom_appbar = ft.BottomAppBar(
        bgcolor=ft.colors.RED_600,
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.IconButton(icon=ft.icons.HOME, icon_color=ft.colors.WHITE, on_click= lambda x: page.go("/")),
                ft.IconButton(icon=ft.icons.SEARCH, icon_color=ft.colors.WHITE, on_click= lambda x: page.go("/search")),
                ft.IconButton(icon=ft.icons.BOOK, icon_color=ft.colors.WHITE, on_click= lambda x: page.go("/listgender")),
            ]
        )
    )
    page.go(page.route)
    page.update()

if __name__ == "__main__":
    ft.app(main, assets_dir="assets", view=ft.WEB_BROWSER)