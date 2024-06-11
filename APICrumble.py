from flask import Flask, request, jsonify
import requests

app = Flask(__name__)


def semantic_search(query):
    payload = {"query": query, "limit": 6}
    response = requests.get("https://api.ask.orkg.org/index/search", params=payload)
    response_json = response.json()
    return find_ids(response_json)

def find_ids(json_file, key="id"):
    ids = []
    for item in json_file["payload"]["items"]:
        ids.append(item[key])
    return ids

def synth_abstracs(query, items):
    payload = {"question": query, "item_ids": items}
    response = requests.get("https://api.ask.orkg.org/llm/synthesize/items/abstracts", params=payload)
    return response.json()

@app.route('/api/synthesize', methods=['GET'])
def synthesize():
    # data = request.args.get("query")
    query = request.args.get("query")
    print(query)
    
    # query = data.get('query')

    if not query:
        return jsonify({"error": "Query parameter is required"}), 400

    try:
        item_ids = semantic_search(query)
        synthesis_result = synth_abstracs(query, item_ids)
        return jsonify(synthesis_result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/synthesizeOnly', methods=['GET'])
def synthesizeOnly():
    query = request.args.get("query")
    items = request.args.getlist("item_ids")
    print(items)

    if not query or not items:
        return jsonify({"error": "Query and ItemIds are required"}), 400
    try:
        synthesis_result = synth_abstracs(query, items)
        return jsonify(synthesis_result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

if __name__ == "__main__":
    app.run(debug=True)
