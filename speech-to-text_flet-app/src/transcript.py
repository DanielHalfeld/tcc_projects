import math
import queue
import numpy as np
import speech_recognition
import whisper
import torch

import flet as ft
from components import styles as st
from components import text_1
from components import selector

from datetime import datetime, timedelta, timezone
from queue import Queue
from time import sleep
from sys import platform

class RecordPage(ft.UserControl):
    def __init__(self, page):
        super().__init__()
        self.page = page  # Added missing page attribute
        self.recording = False  # Changed to False initially
        self.transcription = text_1.transcription_text
        self.copyButton = ft.IconButton(icon=ft.icons.COPY, on_click=self.copy_to_clipboard)
        self.selector = selector.selector
        self.transcript_row = ft.Row(
            controls=[self.transcription, self.copyButton, self.selector], 
            spacing=25, 
            alignment=ft.MainAxisAlignment.START, 
            wrap=True, 
            scroll=ft.ScrollMode.ADAPTIVE
        )
        self.recordLabel = ft.Text("Iniciar transcrição.")
        self.recordButton = ft.IconButton(icon=ft.icons.MIC, on_click=self.start_record)
        self.loading_indicator = ft.ProgressRing(visible=False)
        self.loading_text = ft.Text("Carregando modelo...", visible=False)
        self.loading_row = ft.Row(controls=[self.loading_indicator, self.loading_text], visible=False)
        self.transcribe_indicator = ft.ProgressRing(visible=False)
        self.transcribe_text = ft.Text("Realizando transcrição...")
        self.transcribe_row = ft.Row(controls=[self.transcribe_indicator, self.transcribe_text], visible=False)
        self.stop_listening = None
        self.source = None
        self.audio_model = None  # Added model storage
        self.recorder = speech_recognition.Recognizer()  # Moved recorder initialization

    def build(self):
        return ft.Container(
            padding=25,
            content=ft.Column(
                controls=[
                    ft.Column(
                        controls=[
                            ft.Text(
                                "Speech-To-Text App", 
                                color=st.APP_TURQUOISE, 
                                style=ft.TextStyle(size=35, weight=ft.FontWeight.BOLD)
                            ),
                            self.recordLabel,
                            self.recordButton,
                            self.loading_row
                        ],
                    ),
                    self.transcript_row,
                ],
            )
        )

    def copy_to_clipboard(self, e):
        self.page.set_clipboard(self.transcription.value)
        self.update()

    def transcript(self):
        try:
            self.transcription.value = "Gravando..."
            self.update()

            data_q = Queue()

            # Initialize recorder settings
            self.recorder.energy_threshold = 1000
            self.recorder.dynamic_energy_threshold = False

            # Initialize microphone
            self.source = speech_recognition.Microphone(
                device_index=None,  # Uses default microphone
                sample_rate=16000
            )

            # Show loading indicator
            self.loading_indicator.visible = True
            self.loading_text.visible = True
            self.loading_row.visible = True
            self.update()

            # Load model if not already loaded
            if not self.audio_model:
                self.audio_model = whisper.load_model(
                    self.selector.value if self.selector.value else "small"
                )

            # Hide loading indicator
            self.loading_indicator.visible = False
            self.loading_text.visible = False
            self.loading_row.visible = False
            self.update()

            record_timeout = 3

            def record_callback(_, audio: speech_recognition.AudioData) -> None:
                data = audio.get_raw_data()
                data_q.put(data)

            # Adjust for ambient noise
            with self.source as source:
                self.recorder.adjust_for_ambient_noise(source)
                print("Sem fala...")

            # Start background listening
            self.stop_listening = self.recorder.listen_in_background(
                self.source, 
                record_callback, 
                phrase_time_limit=record_timeout
            )
            
            while self.recording:
                
                if not data_q.empty():
                    
                    audio_data = b''.join(data_q.queue)
                    data_q.queue.clear()

                    audio_np = np.frombuffer(audio_data, dtype=np.int16).astype(np.float32) / 32768.0

                    self.loading_indicator.visible = True
                    self.transcribe_text.visible = True
                    self.transcribe_row.visible = True
                    
                    result = self.audio_model.transcribe(
                        audio_np,
                    )

                    self.loading_indicator.visible = False
                    self.transcribe_text.visible = False
                    self.transcribe_row.visible = False
                                        
                    text = result['text'].strip()

                    self.transcription.value = f"{text}"

                    self.update()
                    
                else:
                    sleep(1)
                    print("Dormindo...")

        except Exception as e:
            self.transcription.value = f"Error: {str(e)}"
            self.update()
            self.stop_record(None)

    def start_record(self, e):
        self.recording = True
        self.recordButton.icon = ft.icons.STOP
        self.recordButton.on_click = self.stop_record
        self.recordLabel.value = "Realizando transcrição:"
        self.update()
        self.transcript()

    def stop_record(self, e):
        self.recording = False
        self.recordButton.icon = ft.icons.MIC
        self.recordButton.on_click = self.start_record
        self.recordLabel.value = "Transcrição:"
        if self.stop_listening:
            self.stop_listening(wait_for_stop=False)
        self.update()
        print("Parado...")