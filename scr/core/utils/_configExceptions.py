from typing import Optional, cast, Any


class TigrexsError(Exception):
    pass

class configMiss(TigrexsError): # TODO:Если что-то окажется бесполезным - вырезать
    message: str

    body: object | None
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

        # if is_dict(body):
        #     self.code = cast(Any, construct_type(type_=Optional[str], value=body.get("code")))
        #     self.param = cast(Any, construct_type(type_=Optional[str], value=body.get("param")))
        #     self.type = cast(Any, construct_type(type_=str, value=body.get("type")))
        # else:
        #     self.code = None
        #     self.param = None
        #     self.type = None
        
class configParamMiss(TigrexsError):
    message : str
    
