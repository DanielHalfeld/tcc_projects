import math
import numpy as np
import speech_recognition
import whisper
import torch

import flet as ft
from components import styles as st
from components import text_1
from components import selector

from datetime import datetime, timedelta
from queue import Queue
from time import sleep
from sys import platform

class RecordPage(ft.UserControl):
    def __init__(self, page):
        super().__init__()
        self.recording=True
        self.transcription = text_1.transcription_text
        self.copyButton = ft.IconButton(icon=ft.icons.COPY, on_click=self.copy_to_clipboard)
        self.selector = selector.selector
        self.transcript_row = ft.Row(controls=[self.transcription, self.copyButton, self.selector], spacing=25, alignment=ft.MainAxisAlignment.START, wrap=True, scroll=ft.ScrollMode.ADAPTIVE)
        self.recordLabel = ft.Text("Iniciar transcrição.")
        self.recordButton = ft.IconButton(icon= ft.icons.MIC, on_click= self.start_record)
        
        

    def build(self):
        # application's root control (i.e. "view") containing all other controls
        return ft.Container(
            padding=25,
            content=ft.Column(
                controls=[
                    ft.Column(
                        controls=[
                            ft.Text("Taquígrafo App", color=st.APP_TURQUOISE, style=ft.TextStyle(size=35, weight=ft.FontWeight.BOLD)),
                            self.recordLabel,
                            self.recordButton
                        ],
                    ),
                    self.transcript_row,
                ],
            )
        )
            
    
    def test(self):
        self.transcription.value=""

        while self.recording == True :
            try:
                self.transcription.value += "O"
                self.update()
                sleep(0.5)
            except KeyboardInterrupt:
                break
    
    def copy_to_clipboard(self,e):
        self.page.set_clipboard(value=self.transcription.value) # type: ignore
        self.update()
    
    def start_recording(self):
        self.transcription.value = "Gravando..."
        self.update()
        # The last time a recording was retrieved from the queue.
        phrase_time = None
        # Thread safe Queue for passing data from the threaded recording callback.
        data_q = Queue()
        # Use SpeechRecognizer to record our audio. And turn off dynamic threshold
        recorder = speech_recognition.Recognizer()
        recorder.energy_threshold = 1000
        recorder.dynamic_energy_threshold = False

        # Important for linux users.
        # if 'linux' in platform:
        #     mic_name = "list"
        #     if not mic_name or mic_name == 'list':
        #         print("Available microphone devices are: ")
        #         for index, name in enumerate(speech_recognition.Microphone.list_microphone_names()):
        #             print(f"Microphone with name \"{name}\" found")
        #         return
        #     else:
        #         for index, name in enumerate(speech_recognition.Microphone.list_microphone_names()):
        #             if mic_name in name:
        #                 source = speech_recognition.Microphone(sample_rate=16000, device_index=index)
        #                 break
        # else:
        source = speech_recognition.Microphone(sample_rate=16000)

        # Load model
        audio_model = whisper.load_model(self.selector.value if self.selector.value != None else "small" )

        record_timeout = 3
        phrase_timeout = 4

        transcription = ['']

        with source: # type: ignore
            recorder.adjust_for_ambient_noise(source)

        def record_callback(_, audio:speech_recognition.AudioData) -> None:
            """
            Threaded callback function to receive audio data when recordings finish.
            audio: An AudioData containing the recorded bytes.
            """
            # Get the data and push it on the Queue
            data = audio.get_raw_data()
            data_q.put(data)

        # Create a background thread that will pass us raw audio bytes.
        recorder.listen_in_background(source, record_callback, phrase_time_limit=record_timeout)

        self.transcription.value = "OK : "
        self.update()

        while self.recording:
            try:
                now = datetime.now(datetime.timezone.now)
                # Pull raw recorded audio from the queue.
                if not data_q.empty():
                    phrase_complete = False
                    # If enough time has passed between recordings, consider the phrase complete.
                    # Clear the current working audio buffer to start over with the new data.
                    if phrase_time and now - phrase_time > timedelta(seconds=phrase_timeout):
                        print ('...')
                        # Flush stdout.
                        print('', end='', flush=True)
                        phrase_complete = True

                    phrase_time = now
                    
                    # Combine audio data from queue
                    audio_data = b''.join(data_q.queue)
                    data_q.queue.clear()
                    
                    # Convert in-ram buffer to something the model can use directly without needing a temp file.
                    # Convert data from 16 bit wide integers to floating point with a width of 32 bits.
                    # Clamp the audio stream frequency to a PCM wavelength compatible default of 32768hz max.
                    audio_np = np.frombuffer(audio_data, dtype=np.int16).astype(np.float32) / 32768.0
                    
                    # Include marker from duration to obtain transcription times
                    time_zero = now
                    # Read the transcription.
                    result = audio_model.transcribe(audio_np, fp16=torch.cuda.is_available())
                    text = result['text'].strip() # type: ignore
                    
                    # If we detected a pause between recordings, add a new item to our transcription.
                    # Otherwise edit the existing one.
                    if phrase_complete:
                        self.transcription.value += text
                    else:
                        self.transcription.value += text
                    '''
                    # Clear the console to reprint the updated transcription.
                    os.system('cls' if os.name=='nt' else 'clear')
                    for line in self.transcription.value:
                        print(line)

                    # Flush stdout.
                    print('', end='', flush=True)
                    '''
                    self.update()
                else:
                    # Infinite loops are bad for processors, must sleep.
                    sleep(0.25)
            except KeyboardInterrupt:
                break

    def start_record(self,e):
        self.recording = True
        self.recordButton.icon =  ft.icons.STOP
        self.recordButton.on_click = self.stop_record
        self.start_recording()

    def stop_record(self,e):
        self.recording = False
        self.recordButton.icon =  ft.icons.MIC
        self.recordButton.on_click = self.start_record
        self.update()     

    