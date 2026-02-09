"""Voice Commands - Intent Recognition and Execution"""

import subprocess
import json
import webbrowser
from typing import Dict, Optional, Tuple
from enum import Enum

from ..config.logger import get_logger

logger = get_logger(__name__)


class CommandType(Enum):
    """Types of voice commands"""
    SYSTEM = "system"  # Launch apps, open files
    CONTROL = "control"  # Media, volume, etc
    QUERY = "query"  # Get information
    CUSTOM = "custom"  # User-defined


class VoiceCommand:
    """Represents a voice command"""

    def __init__(
        self,
        name: str,
        command_type: CommandType,
        description: str,
        patterns: list,
        executor: callable,
        requires_confirmation: bool = True
    ):
        self.name = name
        self.command_type = command_type
        self.description = description
        self.patterns = patterns  # List of command patterns/aliases
        self.executor = executor
        self.requires_confirmation = requires_confirmation

    def to_dict(self):
        return {
            "name": self.name,
            "type": self.command_type.value,
            "description": self.description,
            "patterns": self.patterns,
            "requires_confirmation": self.requires_confirmation
        }


class CommandRegistry:
    """Registry of available voice commands"""

    def __init__(self):
        self.commands: Dict[str, VoiceCommand] = {}
        self._register_default_commands()

    def _register_default_commands(self):
        """Register default system commands"""

        # Open application command
        def open_app(app_name: str) -> Tuple[bool, str]:
            try:
                # Map common app names to executable paths
                app_map = {
                    "notepad": "notepad.exe",
                    "calc": "calc.exe",
                    "calculator": "calc.exe",
                    "paint": "mspaint.exe",
                    "word": "winword.exe",
                    "excel": "excel.exe",
                    "powerpoint": "powerpnt.exe",
                    "chrome": "chrome.exe",
                    "firefox": "firefox.exe",
                    "edge": "msedge.exe",
                }

                app_lower = app_name.lower().strip()
                executable = app_map.get(app_lower, app_name)

                subprocess.Popen(executable)
                logger.info(f"Opened application: {app_name}")
                return True, f"Opening {app_name}"

            except Exception as e:
                logger.error(f"Failed to open {app_name}: {e}")
                return False, f"Could not open {app_name}"

        self.register(VoiceCommand(
            name="open",
            command_type=CommandType.SYSTEM,
            description="Open an application",
            patterns=["open {app}", "launch {app}", "start {app}"],
            executor=open_app,
            requires_confirmation=True
        ))

        # Web search command (safely open browser)
        def web_search(query: str) -> Tuple[bool, str]:
            try:
                # Safely construct URL with proper URL encoding
                import urllib.parse
                encoded_query = urllib.parse.quote(query)
                url = f"https://www.google.com/search?q={encoded_query}"

                # Use webbrowser module instead of shell=True (safe, no command injection)
                webbrowser.open(url)

                logger.info(f"Opened web search: {query}")
                return True, f"Searching for {query}"
            except Exception as e:
                logger.error(f"Web search failed: {e}")
                return False, "Could not open search"

        self.register(VoiceCommand(
            name="search",
            command_type=CommandType.QUERY,
            description="Search the web",
            patterns=["search for {query}", "search {query}", "find {query}"],
            executor=web_search,
            requires_confirmation=False
        ))

        # Timer command (placeholder)
        def set_timer(duration: str) -> Tuple[bool, str]:
            logger.info(f"Timer set for: {duration}")
            return True, f"Timer set for {duration}"

        self.register(VoiceCommand(
            name="timer",
            command_type=CommandType.CONTROL,
            description="Set a timer",
            patterns=["set timer for {duration}", "timer {duration}", "remind me in {duration}"],
            executor=set_timer,
            requires_confirmation=False
        ))

    def register(self, command: VoiceCommand):
        """Register a voice command"""
        self.commands[command.name] = command
        logger.info(f"Registered command: {command.name}")

    def get_command(self, name: str) -> Optional[VoiceCommand]:
        """Get command by name"""
        return self.commands.get(name.lower())

    def list_commands(self) -> list:
        """List all registered commands"""
        return [cmd.to_dict() for cmd in self.commands.values()]

    def search_command(self, query: str) -> Optional[Tuple[VoiceCommand, str]]:
        """
        Search for a command matching the query

        Returns:
            Tuple of (command, parameter) or None
        """
        query_lower = query.lower().strip()

        for cmd in self.commands.values():
            for pattern in cmd.patterns:
                pattern_lower = pattern.lower()

                # Simple pattern matching (would be improved with NLP)
                if "{" in pattern:
                    # Has a parameter placeholder
                    prefix = pattern_lower.split("{")[0].strip()

                    if query_lower.startswith(prefix):
                        # Extract parameter
                        param = query_lower[len(prefix):].strip()
                        return cmd, param

                else:
                    # Exact match or similarity
                    if pattern_lower == query_lower:
                        return cmd, ""

        return None

    def execute_command(
        self,
        command_name: str,
        parameter: str = "",
        require_confirmation: bool = True
    ) -> Tuple[bool, str, Optional[dict]]:
        """
        Execute a command

        Returns:
            Tuple of (success, message, result_data)
        """
        try:
            command = self.get_command(command_name)

            if not command:
                logger.warning(f"Command not found: {command_name}")
                return False, f"Command '{command_name}' not found", None

            # Check if confirmation required
            if command.requires_confirmation and require_confirmation:
                return True, f"Command '{command_name}' requires confirmation", {
                    "awaiting_confirmation": True,
                    "command": command_name,
                    "parameter": parameter
                }

            # Execute
            logger.info(f"Executing command: {command_name} with param: {parameter}")
            success, message = command.executor(parameter)

            return success, message, {
                "command": command_name,
                "parameter": parameter,
                "status": "success" if success else "failed"
            }

        except Exception as e:
            logger.error(f"Error executing command {command_name}: {e}")
            return False, f"Error executing command: {str(e)}", None


# Global registry
_command_registry: Optional[CommandRegistry] = None


def get_command_registry() -> CommandRegistry:
    """Get or create command registry"""
    global _command_registry
    if _command_registry is None:
        _command_registry = CommandRegistry()
    return _command_registry
