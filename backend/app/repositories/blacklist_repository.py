from app.models.blacklisted_token import BlacklistedToken


class BlacklistRepository:
    def __init__(self, session):
        self.session = session

    def is_blacklisted(self, token: str) -> bool:
        return self.session.query(BlacklistedToken).filter(BlacklistedToken.token == token).first() is not None

    def add_to_blacklist(self, token: str):
        blacklisted = BlacklistedToken(token=token)
        self.session.add(blacklisted)
        self.session.commit()
