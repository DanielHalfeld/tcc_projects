import flet as ft
from components import styles

selector = ft.Dropdown( "small", 
                        label="modelo",
                        label_style= ft.TextStyle(
        size=16,
        weight=ft.FontWeight.W_200,
        color=styles.APP_JUNGLE
    ),
                        options=[
                            ft.dropdown.Option("tiny"),
                            ft.dropdown.Option("small"),
                            ft.dropdown.Option("medium"),
                            ft.dropdown.Option("large"),
                        ],
                        border_width=2, 
                        border_color=styles.APP_JUNGLE, 
                        border_radius=5, 
                        focused_border_color=styles.APP_SALMON,
                        width= 150
                        )