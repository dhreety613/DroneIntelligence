from app.schemas.setup import SetupRequest


class SessionService:
    _setup: SetupRequest | None = None

    def set_setup(self, payload: SetupRequest):
        self._setup = payload
        return payload

    def get_setup(self) -> SetupRequest:
        if self._setup is None:
            raise ValueError("No setup provided. Please configure setup first.")
        return self._setup


session_service = SessionService()