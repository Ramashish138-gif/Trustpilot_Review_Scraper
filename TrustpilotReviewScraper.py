from playwright.sync_api import sync_playwright
import requests
import pandas as pd

def fetch(sku="lendingclub.com", page=1):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36",
        )
        page_obj = context.new_page()  

        page_obj.goto(f"https://www.trustpilot.com/review/{sku}")
        page_obj.wait_for_load_state("domcontentloaded")
        page_obj.wait_for_timeout(3000)

        build_id = page_obj.evaluate("""
            () => {
                const el = document.querySelector('script#__NEXT_DATA__');
                if (el) {
                    const data = JSON.parse(el.textContent);
                    return data.buildId;
                }
                return null;
            }
        """)
       
        cookies = context.cookies()
        cookie_dict = {c['name']: c['value'] for c in cookies}

        browser.close()

    if not build_id:
        return []

    if page <= 1:
        api_url = f"https://www.trustpilot.com/_next/data/{build_id}/review/{sku}.json?languages=all&businessunit={sku}"
    else:
        api_url = f"https://www.trustpilot.com/_next/data/{build_id}/review/{sku}.json?page={page}&languages=all&businessunit={sku}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36",
        "x-nextjs-data": "1",
        "Accept": "*/*",
        "Referer": f"https://www.trustpilot.com/review/{sku}",
    }

    response = requests.get(api_url, headers=headers, cookies=cookie_dict, allow_redirects=True)
    print(f" Status: {response.status_code}")

    data = response.json()
    page_props = data.get("pageProps", {})
    product_name = page_props.get("businessUnit", {}).get("displayName")

    reviews = []
    for item in page_props.get("reviews", []):
        review = {
            "review_id": item.get("id"),
            "author": item.get("consumer", {}).get("displayName"),
            "title": item.get("title"),
            "text": item.get("text"),
            "rating": item.get("rating"),
            "date": item.get("labels", {}).get("verification", {}).get("createdDateTime"),
            "product_name": product_name,
            "location": item.get("consumer", {}).get("countryCode"),
            "brand_response": item.get("reply", {}).get("message") if item.get("reply") else None,
            "is_verified": item.get("labels", {}).get("verification", {}).get("isVerified"),
        }
        reviews.append(review)

    df = pd.DataFrame(reviews)
    file_name = f"{sku}_reviews_{page}.csv"
    df.to_csv(file_name, index=False, encoding="utf-8-sig")
    print(f"Saved reviews to {file_name}")

    return reviews


fetch("lendingclub.com", page=3)