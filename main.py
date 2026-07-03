import os
import pandas as pd
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup

# ==========================================
# MOCK WEB DATA (AS PER INSTRUCTION #3)
# ==========================================
html_content = """
<html>
    <body>
        <div class="product-card" data-category="Electronics">
            <h2 class="title">Wireless Headphones</h2>
            <span class="price">$89.99</span>
            <span class="rating">4.5</span>
        </div>
        <div class="product-card" data-category="Electronics">
            <h2 class="title">Mechanical Keyboard</h2>
            <span class="price">$120.00</span>
            <span class="rating">4.7</span>
        </div>
        <div class="product-card" data-category="Accessories">
            <h2 class="title">Ergonomic Mouse</h2>
            <span class="price">$45.50</span>
            <span class="rating">4.2</span>
        </div>
        <div class="product-card" data-category="Electronics">
            <h2 class="title">Gaming Monitor</h2>
            <span class="price">$299.99</span>
            <span class="rating">4.8</span>
        </div>
        <div class="product-card" data-category="Accessories">
            <h2 class="title">USB-C Hub</h2>
            <span class="price">$25.00</span>
            <span class="rating">4.0</span>
        </div>
    </body>
</html>
"""

def run_web_scraper():
    print("[INFO] Starting Python Web Scraper...")
    soup = BeautifulSoup(html_content, 'html.parser')
    products = soup.find_all('div', class_='product-card')
    
    extracted_data = []
    for item in products:
        name = item.find('h2', class_='title').text.strip()
        category = item.get('data-category')
        price = float(item.find('span', class_='price').text.replace('$', ''))
        rating = float(item.find('span', class_='rating').text)
        
        extracted_data.append({
            "Product Name": name,
            "Category": category,
            "Price ($)": price,
            "Rating": rating
        })
        
    df = pd.DataFrame(extracted_data)
    csv_file = "competitor_market_data.csv"
    df.to_csv(csv_file, index=False)
    print(f"[SUCCESS] Scraped data saved to sheet: '{csv_file}'")
    return csv_file

def analyze_market_data(csv_path):
    print("[INFO] Initializing Data Analysis...")
    df = pd.read_csv(csv_path)
    
    print("\n--- Extracted Data Summary ---")
    print(df.to_string(), "\n")
    
    mean_price = df["Price ($)"].mean()
    mean_rating = df["Rating"].mean()
    print(f"Metrics Calculated -> Average Price: ${mean_price:.2f} | Average Rating: {mean_rating:.2f}/5")
    
    print("[INFO] Generating analytical charts...")
    plt.figure(figsize=(9, 5))
    bar_colors = ['#1f77b4' if cat == 'Electronics' else '#2ca02c' for cat in df['Category']]
    
    plt.bar(df["Product Name"], df["Price ($)"], color=bar_colors, edgecolor='black', width=0.6)
    plt.title("Competitor Product Price Benchmarking", fontsize=14, fontweight='bold', pad=15)
    plt.xlabel("Product Models", fontsize=12, labelpad=10)
    plt.ylabel("Price Index ($)", fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.5)
    
    chart_output = "pricing_analysis_chart.png"
    plt.tight_layout()
    plt.savefig(chart_output, dpi=200)
    plt.close()
    print(f"[SUCCESS] Analytical chart generated: '{chart_output}'\n")

if __name__ == "__main__":
    data_sheet = run_web_scraper()
    analyze_market_data(data_sheet)