from fastapi import APIRouter, HTTPException, status

from models.product import Product, ProductListResponse

router = APIRouter(
    prefix="/products",
    tags=["Products"],
)

PRODUCTS: list[Product] = [
    Product(
        id=1,
        name="Wireless Keyboard",
        description="Compact wireless keyboard with Bluetooth connectivity.",
        price=49.90,
        stock_quantity=25,
        is_active=True,
    ),
    Product(
        id=2,
        name="Wireless Mouse",
        description="Ergonomic wireless mouse with adjustable sensitivity.",
        price=29.90,
        stock_quantity=40,
        is_active=True,
    ),
    Product(
        id=3,
        name="USB-C Hub",
        description="Multi-port USB-C hub with HDMI and Ethernet support.",
        price=69.90,
        stock_quantity=15,
        is_active=True,
    ),
    Product(
        id=4,
        name="Laptop Stand",
        description="Adjustable aluminium stand for laptops.",
        price=39.90,
        stock_quantity=0,
        is_active=True,
    ),
    Product(
        id=5,
        name="Discontinued Headset",
        description="Legacy headset retained for test scenarios.",
        price=59.90,
        stock_quantity=0,
        is_active=False,
    ),
]


@router.get("", response_model=ProductListResponse)
def list_products() -> ProductListResponse:
    active_products = [product for product in PRODUCTS if product.is_active]

    return ProductListResponse(
        items=active_products,
        count=len(active_products),
    )


@router.get("/{product_id}", response_model=Product)
def get_product(product_id: int) -> Product:
    product = next(
        (
            item
            for item in PRODUCTS
            if item.id == product_id and item.is_active
        ),
        None,
    )

    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product {product_id} was not found.",
        )

    return product
