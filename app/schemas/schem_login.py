from pydantic import BaseModel

# In-code schemas (get)


# Request schemas (create/update/asssign)


# Response schemas (return)

class ReturnToken(BaseModel):
    access_token: str
    token_type: str

    class Config:
        from_attributes: True