import datetime
import random

from fastmcp import FastMCP

from moov_mcp.models.analysis import SentimentAnalysisResult

analysis_mcp = FastMCP(name="Analysis")

FEATURED_PRODUCTS = [
    "iPhone 15 Pro", "MacBook Air M3", "Samsung Galaxy S24", "Google Pixel 8", "iPad Pro M2",
    "Dell XPS 13", "Surface Pro 9", "AirPods Pro 2", "Sony WH-1000XM5", "Tesla Model Y",
    "Nintendo Switch OLED", "Steam Deck", "Meta Quest 3", "Apple Watch Series 9", "Garmin Fenix 7",
    "DJI Mini 4 Pro", "GoPro Hero 12", "Canon EOS R5", "Sony A7 IV", "Framework Laptop",
    "Asus ROG Ally", "MSI Gaming Laptop", "NVIDIA RTX 4090", "AMD Ryzen 9 7950X", "Intel Core i9-13900K",
    "Samsung QN90C TV", "LG C3 OLED", "Sonos Era 300", "Amazon Echo Show 15", "Google Nest Hub Max",
    "Ring Video Doorbell", "Nest Thermostat", "Philips Hue Bridge", "Razer DeathAdder V3", "Logitech MX Master 3S",
    "Corsair K100 RGB", "HyperX Cloud Alpha", "Elgato Stream Deck", "Anker PowerCore", "MagSafe Charger",
    "Samsung Galaxy Buds2 Pro", "Nothing Phone 2", "OnePlus 11", "Xiaomi 13 Pro", "Huawei P60 Pro",
    "Surface Laptop 5", "ThinkPad X1 Carbon", "Alienware Aurora R15", "HP Spectre x360", "Asus ZenBook Pro"
]

@analysis_mcp.tool()
def get_featured_products() -> list[str]:
    """Get a list of the current featured products.
    
    Returns:
        list: A list of featured products.
    """
    random.seed(datetime.datetime.today().timestamp())  # noqa: DTZ002
    return random.sample(FEATURED_PRODUCTS, 5)


@analysis_mcp.tool()
def sentiment_analysis(
    product: str, n_results: int = 10
) -> list[SentimentAnalysisResult]:
    """Perform sentiment analysis on a product.

    Args:
        product (str): The name of the product to analyze.
        n_results (int): The number of sentiment analysis results to return.

    Returns:
        list[SentimentAnalysisResult]: A list of sentiment analysis results.
    """
    random.seed(product)

    general_sentiment = random.random() * 2 - 1  # noqa: S311, Random sentiment between -1 and 1
    generate_variate = random.uniform(0.5, 1.5)  # noqa: S311, Variance for the number of results

    return [
        SentimentAnalysisResult(
            sentiment=max(
                -1.0,
                min(1.0, random.normalvariate(general_sentiment, generate_variate)),
            ),
            confidence=random.uniform(0.5, 1.0),  # noqa: S311
        )
        for _ in range(n_results)
    ]
