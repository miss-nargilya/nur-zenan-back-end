from pydantic import BaseModel


class BaseSchema(BaseModel):
    name_tm: str
    name_ru: str
    name_eng: str
    
    
class subCategorySchema(BaseSchema):
    category_id: int
    
    
class productSchema(subCategorySchema):
    description_tm: str
    description_ru: str
    description_eng: str
    price: float 
    code: str 
    discount: float
    subcategory_id: int
    
    

class loginSchema(BaseModel):
    username: str
    phone_number: int
    age_feature: int
    skin_position: str        