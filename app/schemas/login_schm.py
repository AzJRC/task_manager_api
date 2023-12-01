from pydantic import BaseModel


class ReturnToken(BaseModel):
    access_token: str
    token_type: str

    class Config:
        from_attributes: True


class GetTokenData(BaseModel):
    username: str | None = None

    class Config:
        from_attributes: True