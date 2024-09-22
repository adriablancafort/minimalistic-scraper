from curl_cffi import requests
from selectolax.parser import HTMLParser


def request_content(URL: str) -> str | None:
    """Request the content of a URL and return it as a string."""

    response = requests.get(URL, impersonate="safari_ios")
    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        return None
    return response.text


def scrape_amazon_product(ASIN: str) -> None:
    """Scrape the price of an Amazon product given its ASIN."""

    URL = f"https://www.amazon.com/dp/{ASIN}"

    html = request_content(URL)

    tree = HTMLParser(html)

    title_element = tree.css_first("span#title")
    price_symbol_element = tree.css_first("span.a-price-symbol")
    price_whole_element = tree.css_first("span.a-price-whole")
    price_fraction_element = tree.css_first("span.a-price-fraction")

    PRODUCT_TITLE = title_element.text().strip() if title_element else "Title not found"
    PRICE_SYMBOL = price_symbol_element.text() if price_symbol_element else "Symbol not found"
    PRICE_WHOLE = price_whole_element.text().replace(".", "") if price_whole_element else "Whole part not found"
    PRICE_FRACTION = price_fraction_element.text() if price_fraction_element else "Fraction not found"

    print(f"Product Title: {PRODUCT_TITLE}")
    print(f"Price Symbol: {PRICE_SYMBOL}")
    print(f"Price Whole: {PRICE_WHOLE}")
    print(f"Price Fraction: {PRICE_FRACTION}")


def main():
    ASINs = ["B09LNW3CY2", "B009KYJAJY", "B0B2D77YB8", "B0D3KPGFHL"]
    for ASIN in ASINs:
        scrape_amazon_product(ASIN)


if __name__ == "__main__":
    main()