from pprint import pprint
from pydantic import BaseModel, EmailStr, Field
from typing import Optional

# Nested model for Address
class Address(BaseModel):
    full_address: str = Field(..., description="User's full address")
    city: str = Field(..., description="User's city")

# Nested model for Bio Data
class BioData(BaseModel):
    name: str = Field(..., description="User's full name")
    cnic: Optional[str] = Field(None, description="User's CNIC number (optional)")
    cell_number: str = Field(..., description="User's cell phone number, e.g., '0345-1122999'")
    email: EmailStr = Field(..., description="User's email address")
    address: Address = Field(..., description="User's address details")
    age: int = Field(..., ge=8, description="User's age, must be at least 8")
    gender: str = Field(..., pattern="^(Male|Female|Other)$", description="User's gender: Male, Female, or Other")

# Nested model for Academic Record
class AcademicRecord(BaseModel):
    education_level: str = Field(..., description="User's education level, e.g., High School, Bachelor’s")
    skills: str = Field(..., description="List of skills, e.g., 'Python, Java'")
    expertise: str = Field(..., description="Areas of expertise, e.g., 'Machine Learning'")

# Main Admission Schema
class AdmissionSchema(BaseModel):
    bio_data: BioData = Field(..., description="User's bio data")
    academic_record: AcademicRecord = Field(..., description="User's academic record")
    profession: Optional[str] = Field(None, description="User's profession (optional)")
    reference: str = Field(..., description="How the user learned about AI HUB Institute")

# Example data
admission_data = {
    "bio_data": {
        "name": "Ahmed Khan",
        "cnic": "12345-1234567-1",
        "cell_number": "0300-1234567",
        "email": "ahmed.khan@example.com",
        "address": {
            "full_address": "123 Main Street",
            "city": "Karachi"
        },
        "age": 22,
        "gender": "Male"
    },
    "academic_record": {
        "education_level": "Bachelor’s",
        "skills": "Python, Java",
        "expertise": "Machine Learning"
    },
    "profession": "Student",
    "reference": "Through a friend"
}

# Create an instance of the schema
admission = AdmissionSchema(**admission_data)

# Convert to JSON
# pprint(admission.model_dump(mode="json" , exclude=None, exclude_unset=True))


