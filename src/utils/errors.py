class ConfigError(Exception):
    """Raised when configuration loading fails."""


class DataFetchError(Exception):
    """Raised when market data cannot be retrieved."""


class SignalError(Exception):
    """Raised when signal calculation fails."""
