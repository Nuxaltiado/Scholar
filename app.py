from flask import Flask, jsonify, request
from scholarly import scholarly

app = Flask(__name__)

@app.route('/api/scholar-scraper')
def scholar_scraper():
    user_id = request.args.get('user')
    if not user_id:
        return jsonify({'error': 'Missing "user" parameter'}), 400

    try:
        author = scholarly.search_author_id(user_id)
        scholarly.fill(author, sections=['indices', 'publications'])

        citations_by_year = author.get('citedby_year', {})
        years = sorted(citations_by_year.keys())
        citations = [citations_by_year[year] for year in years]

        return jsonify({
            'labels': years,
            'values': citations
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run()
