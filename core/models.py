# core/models.py
from pydantic import BaseModel, Field, field_validator, FieldValidationInfo # <<< THE FIX IS HERE
from typing import Literal, List, Optional

class PlanStep(BaseModel):
    command: Literal["CREATE_FILE", "WRITE_TO_FILE", "CREATE_DIR", "INSTALL_LIBRARIES"]
    path: Optional[str] = None
    content: Optional[str] = None
    libraries: Optional[List[str]] = None

    @field_validator('path')
    @classmethod
    def check_path_is_required(cls, v: str, info: FieldValidationInfo):
        # Path is required for file/dir commands
        if info.data.get('command') in ["CREATE_FILE", "WRITE_TO_FILE", "CREATE_DIR"] and v is None:
            raise ValueError('A "path" is required for this command')
        return v
        
    @field_validator('content')
    @classmethod
    def check_content_is_required(cls, v: str, info: FieldValidationInfo):
        # Content MUST exist if the command is WRITE_TO_FILE
        if info.data.get('command') == 'WRITE_TO_FILE' and v is None:
            raise ValueError('A "content" key is required for the WRITE_TO_FILE command')
        return v
    
    @field_validator('libraries')
    @classmethod
    def check_libraries_are_required(cls, v: str, info: FieldValidationInfo):
        # The 'libraries' list MUST exist if the command is INSTALL_LIBRARIES
        if info.data.get('command') == 'INSTALL_LIBRARIES' and v is None:
            raise ValueError('A "libraries" key with a list of packages is required for the INSTALL_LIBRARIES command')
        return v

class Plan(BaseModel):
    steps: List[PlanStep]