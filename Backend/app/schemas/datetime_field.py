"""
DateTime field for Pydantic models with proper Poland timezone handling.
"""
from datetime import datetime
from pydantic import field_validator
from app.utils.datetime_utils import to_pl, format_iso_no_ms

class DateTimeField:
    """
    Mixin for Pydantic models to properly handle datetime fields.
    
    Usage:
        class MySchema(BaseModel, DateTimeField):
            created_at: datetime
            
            # The model_config and validators will handle timezone conversion
    """
    
    @field_validator('*', mode='before')
    @classmethod
    def ensure_poland_timezone(cls, value, info):
        """
        Ensure datetime fields have Poland timezone info.
        
        Args:
            value: The value to validate.
            info: Field information.
            
        Returns:
            datetime: The datetime with Poland timezone info.
        """
        if isinstance(value, datetime):
            return to_pl(value)
        return value
    
    # You can also add a method to format datetimes for JSON response
    def model_dump_json(self, **kwargs):
        """
        Override model_dump_json to format datetimes without milliseconds.
        
        Returns:
            str: JSON representation with formatted datetimes.
        """
        data = self.model_dump()
        # Format datetime fields
        for key, value in data.items():
            if isinstance(value, datetime):
                data[key] = format_iso_no_ms(value)
        
        return data
