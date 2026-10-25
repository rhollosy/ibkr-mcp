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

class InvalidInputError(IBKRError):
    """Raised when a caller-supplied value is rejected before sending a request."""
    pass
