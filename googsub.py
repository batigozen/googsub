import requests
from urllib.parse import urlparse

def extract_subdomains_with_api(domain, api_key, search_engine_id, max_queries):
    url = "https://www.googleapis.com/customsearch/v1"
    query = f"site:*.{domain}"

    subdomains = set()
    for start in range(1, max_queries + 1, 10):
        params = {
            "key": api_key,
            "cx": search_engine_id,
            "q": query,
            "start": start
        }

        print(f"Querying Google Custom Search API for subdomains of {domain} (start={start})...")

        response = requests.get(url, params=params)
        if response.status_code != 200:
            print(f"API request failed. Status code: {response.status_code}, Response: {response.text}")
            break

        results = response.json()
        if "items" in results:
            for item in results["items"]:
                link = item["link"]
                parsed_url = urlparse(link)
                if domain in parsed_url.netloc:
                    subdomain = parsed_url.netloc
                    subdomains.add(subdomain)
        else:
            print("No more results found.")
            break

    return sorted(subdomains)

def main():
    domain = input("Enter the target domain (e.g., example.com): ")
    api_key = "$ENTER YOUR CUSTOM API KEY"
    search_engine_id = "$ENTER THE SEARCH ENGINE ID"
    max_queries = int(input("Enter the maximum number of search queries to use (e.g., 10, 50, 100): "))

    subdomains = extract_subdomains_with_api(domain, api_key, search_engine_id, max_queries)

    if subdomains:
        print("\nFound subdomains:")
        for subdomain in subdomains:
            print(subdomain)
    else:
        print("No subdomains found.")

if __name__ == "__main__":
    main()

