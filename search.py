import requests
import mysql.connector

# Replace these with your actual API key, Custom Search Engine ID, and MySQL credentials
api_key = 'AIzaSyAe-f0NF7Mz-KHtdva2skx7cxZdRoaSl0U'  # Your API key from Google Cloud
search_engine_id = '55d861a5b151b48da'  # Your CSE ID from Google Custom Search Engine

# MySQL Database connection details


def google_search(query):
    search_url = "https://www.googleapis.com/customsearch/v1"
    params = {
        'q': query,
        'key': api_key,
        'cx': search_engine_id,
    }
    response = requests.get(search_url, params=params)
    response.raise_for_status()  # Raise an error for bad status codes
    search_results = response.json()
    return search_results

def save_to_mysql(results_list, query):
    try:
        # Connect to the MySQL database
        connection = mysql.connector.connect(user= 'root',password='password',host="127.0.0.1",database="search_results_db")
        cursor = connection.cursor()

        # Insert each result into the database
        for result in results_list:
            title = result['title']
            snippet = result['snippet']
            url = result['link']
            cursor.execute(
                "INSERT INTO search_results (query, title, snippet, url) VALUES (%s, %s, %s, %s)",
                (query, title, snippet, url)
            )
        
        # Commit the transaction
        connection.commit()

        print(f"Results for '{query}' saved to MySQL database.")
    
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    


def generate_serp(search_results):
    results_list = []
    for result in search_results.get('items', []):
        title = result['title']
        snippet = result['snippet']
        url = result['link']
        results_list.append({"title": title, "snippet": snippet, "link": url})
    return results_list

# Example Usage
query = "Python programming"
search_results = google_search(query)
results_list = generate_serp(search_results)
save_to_mysql(results_list, query)
