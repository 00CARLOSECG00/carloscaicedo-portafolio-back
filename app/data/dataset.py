"""
ONE coherent fictional dataset — mirrors `carloscaicedo-portfolio/data/fallback/dataset.ts`.
All database paradigm views are derived from this single source of truth.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Customer:
    id: int
    name: str
    city: str
    country: str
    latitude: float
    longitude: float
    interests: list[str]
    segment: str


@dataclass(frozen=True)
class Product:
    id: int
    name: str
    category: str
    price: int


@dataclass(frozen=True)
class Order:
    id: int
    customer_id: int
    product_id: int
    quantity: int
    date: str


@dataclass(frozen=True)
class Review:
    id: int
    customer_id: int
    product_id: int
    rating: int
    text: str


CUSTOMERS: list[Customer] = [
    Customer(1, "Ana Restrepo", "Bogotá", "Colombia", 4.711, -74.072, ["technology", "photography"], "Enthusiast"),
    Customer(2, "John Herrera", "Medellín", "Colombia", 6.244, -75.581, ["gaming", "hardware"], "Power user"),
    Customer(3, "Lucía Fernández", "Buenos Aires", "Argentina", -34.603, -58.381, ["design", "audio"], "Creative"),
    Customer(4, "Mateo Silva", "São Paulo", "Brazil", -23.55, -46.633, ["data", "cloud"], "Professional"),
    Customer(5, "Valentina Rojas", "Santiago", "Chile", -33.447, -70.673, ["technology", "productivity"], "Professional"),
    Customer(6, "Diego Morales", "Lima", "Peru", -12.046, -77.043, ["photography", "travel"], "Enthusiast"),
    Customer(7, "Camila Vargas", "Ciudad de México", "Mexico", 19.433, -99.133, ["gaming", "streaming"], "Power user"),
    Customer(8, "Sofía Núñez", "Quito", "Ecuador", -0.18, -78.468, ["audio", "music"], "Creative"),
]

PRODUCTS: list[Product] = [
    Product(101, "Aurora Laptop 14", "Computers", 1299),
    Product(102, "Nimbus Wireless Headphones", "Audio", 199),
    Product(103, "Pulse Mechanical Keyboard", "Accessories", 129),
    Product(104, "Vertex 4K Monitor", "Displays", 449),
    Product(105, "Orbit Mirrorless Camera", "Photography", 899),
]

ORDERS: list[Order] = [
    Order(5001, 1, 101, 1, "2024-11-03"),
    Order(5002, 1, 105, 1, "2024-11-20"),
    Order(5003, 2, 103, 2, "2024-10-12"),
    Order(5004, 3, 102, 1, "2024-12-01"),
    Order(5005, 4, 104, 2, "2024-09-28"),
    Order(5006, 5, 101, 1, "2024-12-15"),
    Order(5007, 7, 102, 1, "2024-11-30"),
    Order(5008, 8, 105, 1, "2024-12-05"),
]

REVIEWS: list[Review] = [
    Review(9001, 1, 101, 5, "Fast, silent and beautifully built. Perfect for data work."),
    Review(9002, 3, 102, 4, "Warm sound and great noise cancelling for studio sessions."),
    Review(9003, 2, 103, 5, "Crisp switches and rock solid for long gaming nights."),
    Review(9004, 4, 104, 4, "Sharp colors, ideal for dashboards and analytics."),
    Review(9005, 6, 105, 5, "Incredible detail for travel photography."),
]


def customer_by_id(customer_id: int) -> Customer | None:
    return next((c for c in CUSTOMERS if c.id == customer_id), None)


def product_by_id(product_id: int) -> Product | None:
    return next((p for p in PRODUCTS if p.id == product_id), None)
