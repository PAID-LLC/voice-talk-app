"""Voice Talk Application CLI - Interactive Command-Line Interface"""

import click
import sys
from pathlib import Path
from typing import Optional

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.config.settings import get_settings
from src.config.logger import LoggerManager, get_logger
from src.speech.synthesis.pyttsx3_engine import get_pyttsx3_engine
from src.ai.conversation.huggingface_client import get_huggingface_client
from src.ai.quota_manager import get_quota_manager
from src.audio.capture import AudioCapture
from src.audio.processor import AudioProcessor

logger = get_logger(__name__)


@click.group()
@click.version_option(version="0.1.0")
def cli():
    """Voice Talk Application - Command-line interface for voice interaction"""
    LoggerManager.initialize()


@cli.command()
@click.option("--voice", default="default", help="Voice to use for speech")
@click.option("--speed", default=1.0, type=float, help="Speech speed (0.5-2.0)")
def talk(voice: str, speed: float):
    """
    Interactive conversational mode - Speak and hear responses

    Start the application in conversational mode. You can type messages
    and the AI will respond with voice.
    """
    click.clear()
    click.secho("=" * 60, fg="cyan")
    click.secho(" Voice Talk Application - Conversational Mode", fg="cyan", bold=True)
    click.secho("=" * 60, fg="cyan")
    click.secho("\nWelcome! Type your messages or voice commands.", fg="green")
    click.secho("Type 'exit' or 'quit' to exit.\n", fg="yellow")

    # Initialize engines
    try:
        tts_engine = get_pyttsx3_engine()
        ai_client = get_huggingface_client()
        quota_mgr = get_quota_manager()

        if not tts_engine.is_initialized:
            click.secho("Warning: TTS engine not initialized", fg="red")

        # Set voice and speed
        if voice != "default":
            voices = tts_engine.list_voices()
            for i, v in enumerate(voices):
                if v["name"].lower() == voice.lower():
                    tts_engine.set_voice(i)
                    break

        tts_engine.set_rate(int(150 * speed))

    except Exception as e:
        click.secho(f"Error initializing engines: {e}", fg="red")
        return

    # Main conversation loop
    session_id = ""
    message_count = 0

    while True:
        try:
            # Get user input
            user_input = click.prompt("\nYou", default="").strip()

            if not user_input:
                continue

            # Check for exit commands
            if user_input.lower() in ["exit", "quit", "bye", "goodbye"]:
                click.secho("\nGoodbye!", fg="green")
                tts_engine.speak("Goodbye!")
                break

            # Show quota status periodically
            if message_count % 5 == 0:
                quota_check = quota_mgr.check_quota("huggingface")
                if not quota_check[0]:
                    click.secho(
                        f"Warning: API quota low ({quota_check[1]} remaining)",
                        fg="yellow"
                    )

            # Get AI response
            click.secho("Assistant", fg="blue", nl=False)
            click.secho(": ", nl=False)

            response, success = ai_client.chat(user_input, session_context=[])

            if success and response:
                # Display response
                click.secho(response, fg="green")

                # Speak response
                try:
                    tts_engine.speak(response[:500])  # Limit to 500 chars for TTS
                except Exception as e:
                    logger.warning(f"TTS error: {e}")

                message_count += 1

            else:
                fallback = "I'm having trouble understanding. Could you rephrase that?"
                click.secho(fallback, fg="yellow")
                tts_engine.speak(fallback)

        except KeyboardInterrupt:
            click.secho("\n\nInterrupted by user", fg="yellow")
            break

        except Exception as e:
            click.secho(f"Error: {e}", fg="red")
            logger.error(f"Conversation error: {e}")


@cli.command()
@click.option("--file", type=click.Path(exists=True), help="Audio file to transcribe")
@click.option("--format", default="srt", type=click.Choice(["srt", "txt", "json"]), help="Output format")
def transcribe(file: Optional[str], format: str):
    """
    Transcribe audio files to text

    Converts audio files (WAV, MP3, FLAC) to text transcriptions.
    """
    try:
        if not file:
            file = click.prompt("Enter audio file path")

        file_path = Path(file)

        if not file_path.exists():
            click.secho(f"File not found: {file}", fg="red")
            return

        click.secho(f"\nTranscribing: {file_path.name}", fg="cyan")

        # Load audio
        from src.audio.io import AudioFileIO

        audio_data, sample_rate = AudioFileIO.read_audio_file(str(file_path))

        # Transcribe
        from src.speech.recognition.vosk_engine import get_vosk_engine

        vosk_engine = get_vosk_engine()

        if not vosk_engine.is_initialized:
            click.sehe("Vosk not initialized. Download model first.", fg="red")
            return

        # Process in chunks
        chunks = AudioProcessor.split_audio_chunks(audio_data, sample_rate, 5000)
        transcript_parts = []

        with click.progressbar(chunks, label="Transcribing") as bar:
            for chunk in bar:
                chunk_bytes = chunk.astype("int16").tobytes()
                text, confidence = vosk_engine.transcribe_audio(chunk_bytes)
                if text:
                    transcript_parts.append(text)

        full_transcript = " ".join(transcript_parts)

        click.secho(f"\nTranscript:\n{full_transcript}\n", fg="green")

        # Save output
        output_file = file_path.stem + "." + format

        if format == "txt":
            Path(output_file).write_text(full_transcript)
        elif format == "srt":
            # Simple SRT format
            srt_content = f"1\n00:00:00,000 --> 00:00:01,000\n{full_transcript}\n"
            Path(output_file).write_text(srt_content)
        elif format == "json":
            import json
            json_content = json.dumps({
                "transcript": full_transcript,
                "word_count": len(full_transcript.split()),
                "format": format
            })
            Path(output_file).write_text(json_content)

        click.secho(f"Saved to: {output_file}", fg="green")

    except Exception as e:
        click.secho(f"Error: {e}", fg="red")
        logger.error(f"Transcription error: {e}")


@cli.command()
def status():
    """Show application status"""
    try:
        from src.speech.synthesis.pyttsx3_engine import get_pyttsx3_engine
        from src.speech.recognition.vosk_engine import get_vosk_engine
        from src.ai.conversation.huggingface_client import get_huggingface_client
        from src.ai.quota_manager import get_quota_manager

        click.secho("\n" + "=" * 60, fg="cyan")
        click.secho(" Voice Talk Application Status", fg="cyan", bold=True)
        click.secho("=" * 60 + "\n", fg="cyan")

        # Settings
        settings = get_settings()
        click.secho("Configuration:", fg="yellow", bold=True)
        click.echo(f"  App Name: {settings.app_name}")
        click.echo(f"  Version: {settings.version}")
        click.echo(f"  Host: {settings.host}:{settings.port}")

        # Audio
        click.secho("\nAudio:", fg="yellow", bold=True)
        click.echo(f"  Sample Rate: {settings.audio.sample_rate}Hz")
        click.echo(f"  Channels: {settings.audio.channels}")

        # Engines
        click.secho("\nEngines Status:", fg="yellow", bold=True)

        vosk = get_vosk_engine()
        click.echo(f"  Vosk STT: {'Initialized' if vosk.is_initialized else 'Not initialized'}")

        pyttsx3 = get_pyttsx3_engine()
        click.echo(f"  Pyttsx3 TTS: {'Initialized' if pyttsx3.is_initialized else 'Not initialized'}")
        if pyttsx3.is_initialized:
            click.echo(f"    Voices: {len(pyttsx3.available_voices)}")

        hf = get_huggingface_client()
        click.echo(f"  HuggingFace API: {'Configured' if hf.is_initialized else 'Not configured'}")

        # Quota Status
        quota = get_quota_manager()
        click.secho("\nAPI Quotas:", fg="yellow", bold=True)
        quota_status = quota.get_quota_status()
        for service, status_info in quota_status.items():
            available = "Available" if status_info["available"] else "Exceeded"
            click.echo(f"  {service}: {available} ({status_info['calls_remaining']} remaining)")

        # Backend Status
        click.secho("\nCurrent Backends:", fg="yellow", bold=True)
        backends = quota.get_backend_status()
        click.echo(f"  AI: {backends['ai_backend']}")
        click.echo(f"  STT: {backends['stt_backend']}")
        click.echo(f"  TTS: {backends['tts_backend']}")

        click.secho("\n" + "=" * 60 + "\n", fg="cyan")

    except Exception as e:
        click.secho(f"Error: {e}", fg="red")
        logger.error(f"Status error: {e}")


@cli.command()
def list_devices():
    """List available audio devices"""
    try:
        click.secho("\nAudio Input Devices:", fg="cyan", bold=True)

        capture = AudioCapture()
        devices = capture.list_devices()

        for device in devices:
            marker = "→ " if device.get("default") else "  "
            click.echo(
                f"{marker}[{device['index']}] {device['name']} "
                f"({device['channels']}ch, {device['sample_rate']}Hz)"
            )

        click.secho("\nAudio Output Devices:", fg="cyan", bold=True)

        from src.audio.playback import AudioPlayback

        playback = AudioPlayback()
        devices = playback.list_output_devices()

        for device in devices:
            marker = "→ " if device.get("default") else "  "
            click.echo(
                f"{marker}[{device['index']}] {device['name']} "
                f"({device['channels']}ch, {device['sample_rate']}Hz)"
            )

        click.echo()

    except Exception as e:
        click.secho(f"Error: {e}", fg="red")


@cli.command()
def server():
    """Start the FastAPI server"""
    import uvicorn
    from src.core.app_instance import create_app

    settings = get_settings()

    click.secho("\nStarting Voice Talk Server...", fg="green")
    click.secho(f"Server: http://{settings.host}:{settings.port}", fg="cyan")
    click.secho(f"Docs: http://{settings.host}:{settings.port}/docs\n", fg="cyan")

    try:
        uvicorn.run(
            "src.core.app_instance:create_app",
            host=settings.host,
            port=settings.port,
            reload=settings.debug,
            factory=True,
            log_level="info"
        )

    except Exception as e:
        click.secho(f"Error starting server: {e}", fg="red")


@cli.command()
def gui():
    """Launch the PyQt6 graphical user interface"""
    click.secho("\nLaunching Voice Talk GUI Application...", fg="green")

    try:
        # Import and run the GUI
        from src.gui.main_window import MainWindow
        from PyQt6.QtWidgets import QApplication

        app = QApplication(sys.argv)
        app.setApplicationName("Voice Talk Application")
        app.setApplicationVersion("0.1.0")

        window = MainWindow()
        window.show()

        click.secho("✓ GUI application launched", fg="green")
        sys.exit(app.exec())

    except ImportError as e:
        click.secho(f"Error: PyQt6 is not installed. Please run: pip install PyQt6", fg="red")
        logger.error(f"PyQt6 import error: {e}")
    except Exception as e:
        click.secho(f"Error launching GUI: {e}", fg="red")
        logger.error(f"GUI launch error: {e}")


if __name__ == "__main__":
    cli()
