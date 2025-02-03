import flet as ft

APP_WHITE = "0xE5E9EC"
APP_SALMON = "0xFF6F59"
APP_JUNGLE = "0x254441"
APP_TURQUOISE = "0x43AA8B"
APP_BEIGE = "0xB2B09B"

button_style_standard = ft.ButtonStyle(
    color={
        ft.MaterialState.HOVERED: ft.colors.WHITE,
        ft.MaterialState.FOCUSED: ft.colors.WHITE,
        ft.MaterialState.DEFAULT: ft.colors.BLACK,
    },
    side={
        ft.MaterialState.HOVERED: ft.BorderSide(1, ft.colors.RED),
        ft.MaterialState.FOCUSED: ft.BorderSide(1, ft.colors.BLUE),
        ft.MaterialState.DEFAULT: None,
    }, # type: ignore
    bgcolor={
        ft.MaterialState.HOVERED: ft.colors.BLACK,
        ft.MaterialState.FOCUSED: ft.colors.BLUE,
        ft.MaterialState.DEFAULT: ft.colors.WHITE,
    },
)

app_text_theme_clear = ft.TextTheme(
    display_small=ft.TextStyle(
        size=22,
        weight=ft.FontWeight.W_200,
        color=APP_JUNGLE
    ),
    display_medium=ft.TextStyle(
        size=30,
        weight=ft.FontWeight.W_200,
        color=APP_JUNGLE
    ),
    body_large=ft.TextStyle(
        size=30,
        weight=ft.FontWeight.W_200,
        color=APP_JUNGLE
    ),
    body_small=ft.TextStyle(
        size=15,
        weight=ft.FontWeight.W_200,
        color=APP_JUNGLE
    ),
    body_medium=ft.TextStyle(
        size=22,
        weight=ft.FontWeight.W_200,
        color=APP_JUNGLE
    ),
    display_large=ft.TextStyle(
        size=35,
        weight=ft.FontWeight.W_200,
        color=APP_JUNGLE
    ),
)

app_color_scheme_clear = ft.ColorScheme(
    background=APP_BEIGE,
    on_background=APP_JUNGLE,
    primary=APP_BEIGE,
    on_primary=APP_SALMON,
    primary_container=APP_TURQUOISE,
    on_primary_container=APP_JUNGLE
)

theme_clear = ft.Theme(
    color_scheme_seed=APP_BEIGE,
    text_theme=app_text_theme_clear,
    color_scheme=app_color_scheme_clear
)