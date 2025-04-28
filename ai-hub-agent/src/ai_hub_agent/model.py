from pydantic import BaseModel, Field
from typing import Literal, Optional
import pprint

class FeedbackFormSchema(BaseModel):
    name: str = Field(..., title="Name of the respondent")
    institution: str = Field(..., title="Institution Name")
    contact: str = Field(..., title="Contact Number", pattern=r"^\d{10,15}$")  # Validates phone numbers
    designation: Literal["Student", "Teacher", "Other"] = Field(..., title="Designation")

    content_relevance: Literal["Excellent", "Good", "Average", "Poor"] = Field(..., title="Relevance of content")
    clarity_of_explanation: Literal["Very Clear", "Clear", "Somewhat Unclear", "Very Unclear"] = Field(..., title="Clarity of explanation")

    presenter_engagement: Literal["Very Engaging", "Moderately", "Neutral", "Not Engaging"] = Field(..., title="Presenter Engagement")
    communication_effectiveness: Literal["Excellent", "Good", "Average", "Poor"] = Field(..., title="Communication Effectiveness")

    overall_rating: Literal["Excellent", "Good", "Average", "Poor"] = Field(..., title="Overall Rating")
    suggestions_for_improvement: Optional[str] = Field(None, title="Suggestions for Improvement")

    interest_in_more_sessions: Literal["Yes", "No"] = Field(..., title="Interest in More Sessions")
    preferred_topics: Optional[str] = Field(None, title="Preferred Topics")

# Example usage
example_data = {
    "name": "M Suleman",
    "institution": "Government G.CIG",
    "contact": "03236390067",
    "designation": "Student",
    "content_relevance": "Good",
    "clarity_of_explanation": "Very Clear",
    "presenter_engagement": "Very Engaging",
    "communication_effectiveness": "Good",
    "overall_rating": "Excellent",
    "suggestions_for_improvement": "Nothing special",
    "interest_in_more_sessions": "Yes",
    "preferred_topics": None
}

validated_feedback = FeedbackFormSchema(**example_data)
pprint.pprint(validated_feedback)