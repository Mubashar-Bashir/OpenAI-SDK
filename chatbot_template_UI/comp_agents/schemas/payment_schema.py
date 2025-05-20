from pydantic import BaseModel, Field, PositiveFloat
from datetime import datetime
from typing import Literal, Optional, Annotated
from uuid import UUID
from pydantic.types import StringConstraints

class FeePaymentSchema(BaseModel):
    """Schema for tracking fee payment records at AI HUB Institute."""
    user_id: UUID = Field(..., description="Unique identifier for the user (UUID format)")
    amount: PositiveFloat = Field(..., description="Payment amount in PKR, must be positive")
    fee_type: Literal["Seminar", "Registration", "Course"] = Field(..., description="Type of fee: Seminar (PKR 5,000), Registration (PKR 10,000), or Course (PKR 50,000 per quarter)")
    quarter: Optional[Literal["Q1", "Q2", "Q3", "Q4"]] = Field(None, description="Quarter for Course fee, if applicable")
    program: Optional[str] = Field(None, description="Program enrolled (e.g., AI Programming), if applicable")
    payment_method: Literal["JazzCash", "EasyPaisa", "Bank Transfer", "Cash", "Cheque"] = Field(..., description="Payment method used")
    custom_payment_method: Optional[Annotated[str, StringConstraints(max_length=50)]] = Field(None, description="Custom payment method, if not listed")
    payment_date: datetime = Field(default_factory=datetime.utcnow, description="Date and time of payment (UTC)")
    payment_status: Literal["Pending", "Paid", "Failed", "Refunded"] = Field(..., description="Status of the payment")
    transaction_id: Optional[Annotated[str, StringConstraints(min_length=1, max_length=100)]] = Field(None, description="Transaction ID, if applicable (e.g., for digital payments)")
    #receipt_url: Optional[Annotated[str, StringConstraints(max_length=500)]] = Field(None, description="URL to payment receipt, if available")
    notes: Optional[Annotated[str, StringConstraints(max_length=500)]] = Field(None, description="Additional notes about the payment")
    currency: Literal["PKR"] = Field(default="PKR", description="Currency of payment (PKR only, per AI HUB’s fee structure)")

    class Config:
        """Pydantic configuration for schema validation."""
        json_encoders = {datetime: lambda v: v.isoformat()}
        extra = "forbid"  # Prevent unexpected fields