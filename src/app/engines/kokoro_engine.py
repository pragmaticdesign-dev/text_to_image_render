import io
import numpy as np
from kokoro import KPipeline
from pydub import AudioSegment
from src.app.core.interfaces.engine_contract import BaseRenderingEngine
from src.app.schemas.requests import RenderOptions

class KokoroEngine(BaseRenderingEngine):
    def __init__(self, lang_code='a'):
        print("Initializing Kokoro TTS pipeline...")
        # Initialize once to keep it hot in memory
        self.pipeline = KPipeline(lang_code=lang_code, repo_id='hexgrad/Kokoro-82M')
        self.sample_rate = 24000
        print("Kokoro Initialization complete.")

    def _numpy_to_audiosegment(self, audio_array):
        # Convert float32 [-1,1] to int16
        audio_int16 = (audio_array * 32767).astype(np.int16)
        return AudioSegment(
            audio_int16.tobytes(),
            frame_rate=self.sample_rate,
            sample_width=2,
            channels=1
        )

    async def render(self, source_code: str, options: RenderOptions) -> bytes:
        # source_code is the input text
        lines = [line.strip() for line in source_code.split('\n') if line.strip()]
        
        combined_audio = AudioSegment.empty()
        silence = AudioSegment.silent(duration=500)  # 500ms gap

        for line in lines:
            generator = self.pipeline(line, voice=options.voice, speed=options.speed)
            line_chunks = [audio for _, _, audio in generator]

            if line_chunks:
                full_line_numpy = np.concatenate(line_chunks)
                segment = self._numpy_to_audiosegment(full_line_numpy)
                combined_audio += segment + silence

        # Export to in-memory bytes buffer
        buffer = io.BytesIO()
        combined_audio.export(buffer, format="mp3", bitrate="192k")
        return buffer.getvalue()