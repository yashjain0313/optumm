from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    employee_id: str = Field(min_length=3, max_length=32)
    password: str = Field(min_length=6, max_length=128)


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    employee_id: str
    name: str


class PayCopayRequest(BaseModel):
    amount: float = Field(gt=0, le=500)
    source: str = Field(pattern="^(HSA|FSA)$")
    description: str = Field(default="Copay payment", max_length=120)
