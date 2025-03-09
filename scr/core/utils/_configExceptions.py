from typing import Optional, cast, Any


class TigrexsError(Exception):
    pass

class configMiss(TigrexsError): # TODO:Если что-то окажется бесполезным - вырезать
    message: str

    body: Optional[object] = None
    """
    Create new config, or fix exsits.
    """

    code: Optional[str] = None
    param: Optional[str] = None
    type: Optional[str]
    
    def __init__(self, message: str, *, body: object | None) -> None:
        super().__init__(message)
        self.message = message
        self.body = body
        
class configParamMiss(TigrexsError):
    message : str
    
