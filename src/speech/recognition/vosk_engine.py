"""Vosk Offline Speech Recognition Engine"""

import json
from pathlib import Path
from typing import Optional, Tuple
import subprocess

from vosk import Model, KaldiRecognizer
import pyaudio

from ...config.settings import get_settings
from ...config.logger import get_logger

logger = get_logger(__name__)


class VoskEngine:
    """Vosk offline speech recognition engine"""

    def __init__(self):
        """Initialize Vosk engine"""
        settings = get_settings()
        self.model_path = settings.speech_recognition.vosk_model_path
        self.sample_rate = settings.audio.sample_rate
        self.confidence_threshold = settings.speech_recognition.confidence_threshold

        self.model: Optional[Model] = None
        self.recognizer: Optional[KaldiRecognizer] = None
        self.is_initialized = False

        # Try to initialize
        self._initialize_model()

    def _initialize_model(self) -> bool:
        """Initialize Vosk model"""
        try:
            if not Path(self.model_path).exists():
                logger.warning(f"Vosk model not found at {self.model_path}")
                logger.info("Please download model from: https://alphacephei.com/vosk/models")
                return False

            self.model = Model(self.model_path)
            self.recognizer = KaldiRecognizer(self.model, self.sample_rate)
            self.is_initialized = True

            logger.info(f"Vosk engine initialized with model: {self.model_path}")
            return True

        except Exception as e:
            logger.error(f"Failed to initialize Vosk: {e}")
            return False

    def transcribe_audio(self, audio_data: bytes) -> Tuple[str, float]:
        """
        Transcribe audio data

        Args:
            audio_data: Audio bytes (PCM int16)

        Returns:
            Tuple of (transcribed_text, confidence)
        """
        if not self.is_initialized:
            logger.error("Vosk engine not initialized")
            return "", 0.0

        try:
            if self.recognizer.AcceptWaveform(audio_data):
                try:
                    result = json.loads(self.recognizer.Result())
                except json.JSONDecodeError as e:
                    logger.error(f"Invalid JSON from Vosk: {e}")
                    return "", 0.0

                # Extract text from result array
                text_items = result.get("result", [])
                if text_items and isinstance(text_items, list):
                    # Join words from recognized phrases
                    text_str = " ".join([item.get("result", "") for item in text_items if "result" in item])
                    confidence = 0.9 if text_str else 0.0
                else:
                    text_str = ""
                    confidence = 0.0

            else:
                try:
                    result = json.loads(self.recognizer.PartialResult())
                except json.JSONDecodeError as e:
                    logger.error(f"Invalid JSON from Vosk: {e}")
                    return "", 0.0

                # Partial result might have different structure
                text_items = result.get("result", [])
                text_str = " ".join([item.get("result", "") for item in text_items if "result" in item]) if text_items else ""
                confidence = 0.0

            return text_str, confidence

        except Exception as e:
            logger.error(f"Error transcribing with Vosk: {e}")
            return "", 0.0

    def transcribe_stream(self, frames, max_frames: int = 1000, timeout_seconds: float = 300):
        """
        Transcribe audio stream (generator)

        Args:
            frames: Generator/iterable of audio frame bytes
            max_frames: Maximum frames to process (prevents DoS)
            timeout_seconds: Maximum duration for stream processing

        Yields:
            Transcribed text chunks
        """
        if not self.is_initialized:
            logger.error("Vosk engine not initialized")
            return

        import time
        start_time = time.time()
        frame_count = 0

        try:
            for data in frames:
                # Check resource limits
                if frame_count >= max_frames:
                    logger.warning(f"Frame limit exceeded ({max_frames})")
                    break

                if time.time() - start_time > timeout_seconds:
                    logger.warning(f"Stream processing timeout exceeded ({timeout_seconds}s)")
                    break

                if isinstance(data, bytes):
                    try:
                        self.recognizer.AcceptWaveform(data)
                        result = json.loads(self.recognizer.Result())

                        if "result" in result and result["result"]:
                            # Extract text properly (not "conf")
                            text = " ".join([item.get("result", "") for item in result["result"] if "result" in item])
                            if text:
                                yield text

                    except json.JSONDecodeError as e:
                        logger.error(f"Invalid JSON from Vosk stream: {e}")
                        continue
                    except Exception as e:
                        logger.error(f"Error processing stream frame: {e}")
                        continue

                frame_count += 1

        except Exception as e:
            logger.error(f"Error in stream transcription: {e}")

    def get_status(self) -> dict:
        """Get engine status"""
        return {
            "engine": "vosk",
            "initialized": self.is_initialized,
            "model_path": self.model_path,
            "sample_rate": self.sample_rate,
            "model_loaded": self.model is not None
        }

    @staticmethod
    def download_model(model_url: str = None):
        """Download Vosk model"""
        logger.info("To download Vosk models, visit: https://alphacephei.com/vosk/models")
        logger.info("Recommended: vosk-model-small-en (50MB)")
        logger.info("Alternative: vosk-model-en (1.4GB)")
        return True


# Global instance
_vosk_instance: Optional[VoskEngine] = None


def get_vosk_engine() -> VoskEngine:
    """Get or create Vosk engine instance"""
    global _vosk_instance
    if _vosk_instance is None:
        _vosk_instance = VoskEngine()
    return _vosk_instance
