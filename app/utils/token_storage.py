class TokenStorage:
    _token = None

    @classmethod
    def set_token(cls, token: str):
        cls._token = token

    @classmethod
    def get_token(cls) -> str:
        if cls._token is None:
            raise ValueError("Token not set. Please authenticate.")
        return cls._token