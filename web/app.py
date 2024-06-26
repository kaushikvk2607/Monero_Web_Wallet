from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/')
def index():
    url = 'https://miningpoolstats.stream/monero'

    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        pool_elements = soup.find_all('div', class_='pool-details')  # Replace with the actual class or tag

        pool_data = []

        for pool_element in pool_elements:
            pool_name = pool_element.find('h3').text.strip()
            pool_fee = pool_element.find('p', string='Fee:').find_next_sibling('p').text.strip()
            hashrate = pool_element.find('p', string='Hashrate:').find_next_sibling('p').text.strip()
            blocks_in_last_100 = pool_element.find('p', string='Blocks in last 100:').find_next_sibling('p').text.strip()
            last_block_found = pool_element.find('p', string='Last Block Found:').find_next_sibling('p').text.strip()

            pool_data.append({
                'name': pool_name,
                'fee': pool_fee,
                'hashrate': hashrate,
                'blocks_in_last_100': blocks_in_last_100,
                'last_block_found': last_block_found
            })

        return render_template('index.html', pool_data=pool_data)

    else:
        return f"Failed to retrieve the page. Status code: {response.status_code}"

if __name__ == '__main__':
    app.run(debug=True)
