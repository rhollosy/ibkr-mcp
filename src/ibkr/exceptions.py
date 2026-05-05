class IBKRError(Exception):
    """Base class for IBKR API errors."""
    pass

class AuthenticationError(IBKRError):
    """Raised when authentication fails."""
    pass

class GatewayTimeoutError(IBKRError):
    """Raised when the gateway fails to respond."""
    pass

class RequestError(IBKRError):
    """Raised for general request failures."""
    pass
