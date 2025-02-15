import flet as ft
from components import styles

transcription_text = ft.TextField("", 
                                read_only=True,
                                adaptive=True,
                                min_lines=5,
                                multiline=True,
                                border_width=2, 
                                border_color=styles.APP_JUNGLE, 
                                border_radius=5, 
                                focused_border_color=styles.APP_SALMON,
                                show_cursor=True,
                                cursor_color=styles.APP_JUNGLE,
                                )