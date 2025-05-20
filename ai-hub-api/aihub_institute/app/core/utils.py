from dataclasses import asdict, is_dataclass
from typing import Any, Dict, Type, TypeVar, Optional
from sqlmodel import SQLModel

T = TypeVar('T')

def dataclass_to_dict(obj: Any) -> Dict[str, Any]:
    """Convert a dataclass instance to a dictionary, filtering out None values."""
    if is_dataclass(obj):
        # Convert to dict and filter out None values
        return {k: v for k, v in asdict(obj).items() if v is not None}
    elif hasattr(obj, "dict"):
        # Handle Pydantic models
        return obj.dict(exclude_none=True)
    else:
        # Regular object, use __dict__
        return {k: v for k, v in obj.__dict__.items() if v is not None}

def model_to_dataclass(model_instance: SQLModel, dataclass_type: Type[T]) -> T:
    """Convert an SQLModel instance to a dataclass instance."""
    # Get all fields that are in the dataclass
    model_dict = {}
    for field_name in dataclass_type.__annotations__.keys():
        if hasattr(model_instance, field_name):
            model_dict[field_name] = getattr(model_instance, field_name)
    
    return dataclass_type(**model_dict)

def dataclass_to_model(dataclass_instance: Any, model_type: Type[SQLModel]) -> SQLModel:
    """Convert a dataclass instance to an SQLModel instance."""
    model_dict = dataclass_to_dict(dataclass_instance)
    return model_type(**model_dict)