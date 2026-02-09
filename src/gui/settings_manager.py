"""GUI Settings Manager - Persistence layer for user preferences"""

import json
from pathlib import Path
from typing import Dict, Any, Optional

from ..config.logger import get_logger

logger = get_logger(__name__)


class GUISettingsManager:
    """Manages GUI settings persistence"""

    def __init__(self):
        """Initialize settings manager"""
        # Store settings in data directory
        data_dir = Path(__file__).parent.parent.parent / "data"
        data_dir.mkdir(exist_ok=True)
        self.settings_file = data_dir / "gui_settings.json"

        # Default settings
        self.defaults = {
            "theme": "light",
            "chat_font_size": 10,
            "auto_save": True,
            "show_timestamps": True,
            "minimize_to_tray": True,
            "window_geometry": None,
            "audio_input_device": -1,  # -1 = default
            "audio_output_device": -1,
            "sample_rate": 16000,
            "volume": 90,
            "voice_index": 0,
            "speech_speed": 150,
        }

        self.settings = self.load_settings()

    def load_settings(self) -> Dict[str, Any]:
        """Load and validate settings from file"""
        try:
            if self.settings_file.exists():
                with open(self.settings_file, "r", encoding="utf-8") as f:
                    # Check file size to prevent DoS
                    import os
                    if os.path.getsize(self.settings_file) > 1024 * 100:  # 100KB limit
                        logger.warning("Settings file too large, using defaults")
                        return self.defaults.copy()

                    try:
                        loaded = json.load(f)
                    except json.JSONDecodeError as e:
                        logger.warning(f"Invalid JSON in settings file: {e}")
                        return self.defaults.copy()

                    # Validate loaded data structure
                    if not isinstance(loaded, dict):
                        logger.warning("Settings file is not a JSON object")
                        return self.defaults.copy()

                    # Validate each setting
                    validated = self.defaults.copy()
                    for key, value in loaded.items():
                        if key not in self.defaults:
                            logger.warning(f"Unknown setting: {key}")
                            continue

                        # Type validation
                        default_type = type(self.defaults[key])
                        if value is not None and not isinstance(value, (type(None), default_type)):
                            logger.warning(f"Invalid type for {key}, using default")
                            continue

                        validated[key] = value

                    logger.info("GUI settings loaded")
                    return validated
        except Exception as e:
            logger.warning(f"Failed to load settings: {e}")

        logger.info("Using default GUI settings")
        return self.defaults.copy()

    def save_settings(self, settings: Optional[Dict[str, Any]] = None) -> bool:
        """Save settings to file"""
        try:
            if settings:
                self.settings.update(settings)

            with open(self.settings_file, "w", encoding="utf-8") as f:
                json.dump(self.settings, f, indent=2)

            logger.info("GUI settings saved")
            return True
        except Exception as e:
            logger.error(f"Failed to save settings: {e}")
            return False

    def get(self, key: str, default: Any = None) -> Any:
        """Get a setting value"""
        return self.settings.get(key, default if default is not None else self.defaults.get(key))

    def set(self, key: str, value: Any) -> None:
        """Set a setting value"""
        self.settings[key] = value

    def get_all(self) -> Dict[str, Any]:
        """Get all settings"""
        return self.settings.copy()

    def reset_to_defaults(self) -> bool:
        """Reset all settings to defaults"""
        try:
            self.settings = self.defaults.copy()
            self.save_settings()
            logger.info("GUI settings reset to defaults")
            return True
        except Exception as e:
            logger.error(f"Failed to reset settings: {e}")
            return False


# Global instance
_gui_settings_instance: Optional[GUISettingsManager] = None


def get_gui_settings() -> GUISettingsManager:
    """Get or create GUI settings manager instance"""
    global _gui_settings_instance
    if _gui_settings_instance is None:
        _gui_settings_instance = GUISettingsManager()
    return _gui_settings_instance
