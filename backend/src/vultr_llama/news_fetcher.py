import requests
import pandas as pd
from typing import *
# Function to get the news from news api
def get_news(company_name: str, api_key: str) -> Optional[Tuple[pd.DataFrame, List]]:
    """
    Fetches news headlines for the given company using the News API.
    Args:
        company_name ,api_key
    Returns:
        A Pandas Dataframe
    """
    # Load the Url
    url = f'https://newsapi.org/v2/everything?q={company_name}&apiKey={api_key}&pageSize=50'
    response = requests.get(url)
    # Check is response is generated
    if response.status_code != 200:
        print(f"Error fetching news: {response.status_code}")
        return None
    
    articles = response.json().get('articles', [])
    valid_articles = []
    # get the title url etc
    for article in articles:
        if article['title'] and article['url'] and 'removed' not in article['url']:
            valid_articles.append({
                'title': article['title'],
                'url': article['url'],
                'urlToImg': article.get('urlToImage', ''),
                'publishedAt': article['publishedAt']
            })

    # Sort by published date and limit to the top 30 articles
    valid_articles.sort(key=lambda x: x['publishedAt'], reverse=True)
    limited_headlines = valid_articles[:30]

    # Return as DataFrame and list of valid articles
    return pd.DataFrame(limited_headlines)
