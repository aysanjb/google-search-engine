from datetime import date
import requests
import mysql.connector

api_key = ' '  
search_engine_id = ' '  



def google_search(query):
    search_url = "https://www.googleapis.com/customsearch/v1"
    params = {
        'q': query,
        'key': api_key,
        'cx': search_engine_id,
    }
    response = requests.get(search_url, params=params)
    response.raise_for_status()  
    search_results = response.json()
    return search_results

def save_to_mysql(results_list, query):
    connection = mysql.connector.connect(user='root', password='password', host="127.0.0.1", database="search_results_db")
  

    try:
        cursor = connection.cursor()

        for result in results_list:
            title = result['title']
            url = result['link']
            date_today = date.today()

            cursor.execute(
                "INSERT INTO search_results (query, title, link, date) VALUES (%s, %s, %s, %s)",
                (query, title, url, date_today)
            )
        
        connection.commit()

        print(f"Results for '{query}' saved to MySQL database.")
    
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def generate_serp(search_results, query):
    results_list = []
    for result in search_results.get('items', []):
        title = result['title']
        link = result['link']
        date_today = date.today()

        results_list.append({"query": query, "title": title, "link": link, "date": date_today})
    return results_list

# Example Usage
query = "مهاجرت به انگلیس"
search_results = google_search(query)
results_list = generate_serp(search_results, query)
save_to_mysql(results_list, query)
