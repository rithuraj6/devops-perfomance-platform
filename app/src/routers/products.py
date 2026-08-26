import json

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..cache import delete_cache, get_cache, set_cache
from ..database import get_db
from ..models import Product
from ..schemas import ProductCreate, ProductResponse


router = APIRouter(
    prefix="/api/products",
    tags=["Products"],
)


PRODUCTS_CACHE_KEY = "products:list"


@router.get(
    "",
    response_model=list[ProductResponse],
)
def get_products(
    db: Session = Depends(get_db),
):
    cached_products = get_cache(PRODUCTS_CACHE_KEY)

    if cached_products:
        return json.loads(cached_products)

    products = db.scalars(
        select(Product)
    ).all()

    product_data = [
        {
            "id": product.id,
            "name": product.name,
            "category": product.category,
            "price": product.price,
        }
        for product in products
    ]

    set_cache(
        PRODUCTS_CACHE_KEY,
        json.dumps(product_data),
        ttl=60,
    )

    return product_data


@router.get(
    "/{product_id}",
    response_model=ProductResponse,
)
def get_product(
    product_id: int,
    db: Session = Depends(get_db),
):
    cache_key = f"product:{product_id}"

    cached_product = get_cache(cache_key)

    if cached_product:
        return json.loads(cached_product)

    product = db.get(Product, product_id)

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found",
        )

    product_data = {
        "id": product.id,
        "name": product.name,
        "category": product.category,
        "price": product.price,
    }

    set_cache(
        cache_key,
        json.dumps(product_data),
        ttl=60,
    )

    return product_data


@router.post(
    "",
    response_model=ProductResponse,
    status_code=201,
)
def create_product(
    product_data: ProductCreate,
    db: Session = Depends(get_db),
):
    product = Product(
        name=product_data.name,
        category=product_data.category,
        price=product_data.price,
    )

    db.add(product)
    db.commit()
    db.refresh(product)

    # Invalidate the product list cache because the dataset changed.
    delete_cache(PRODUCTS_CACHE_KEY)

    return product
