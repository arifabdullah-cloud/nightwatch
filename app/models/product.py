from pydantic import BaseModel, ConfigDict, Field


class Product(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": 1,
                "name": "Wireless Keyboard",
                "description": "Compact wireless keyboard",
                "price": 49.90,
                "stock_quantity": 25,
                "is_active": True,
            }
        }
    )

    id: int = Field(gt=0)
    name: str = Field(min_length=1, max_length=100)
    description: str = Field(min_length=1, max_length=500)
    price: float = Field(gt=0)
    stock_quantity: int = Field(ge=0)
    is_active: bool = True


class ProductListResponse(BaseModel):
    items: list[Product]
    count: int
