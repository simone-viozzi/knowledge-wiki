from flask import Flask, jsonify, abort, request

app = Flask(__name__)

quotes = [
    {
        "id": 1,
        "quote": "I'm gonna make him an offer he can't refuse.",
        "movie": "The Godfather",
    },
    {
        "id": 2,
        "quote": "Get to the choppa!",
        "movie": "Predator",
    },
    {
        "id": 3,
        "quote": "Nobody's gonna hurt anybody. We're gonna be like three little Fonzies here.",
        "movie": "Pulp Fiction",
    },
]


def _get_quote(qid):
    return [quote for quote in quotes if quote["id"] == qid]


def _quote_exists(existing_quote):
    return [quote for quote in quotes if quote["quote"] == existing_quote]


@app.route("/api/quotes", methods=["GET"])
def get_quotes():
    return {"quotes": quotes}


@app.route("/api/quotes/<int:qid>", methods=["GET"])
def get_quote(qid):
    quote = _get_quote(qid)
    if not quote:
        abort(404)

    return {"quotes": quote}


@app.route("/api/quotes", methods=["POST"])
def create_quote():
    if not request.json:
        abort(400)

    quote = request.json.get("quote")
    movie = request.json.get("movie")
    if quote is None or movie is None:
        abort(400)

    if _quote_exists(quote):
        abort(400)

    last_quote_id = quotes[-1].get("id", 0)
    new_quote = dict(id=last_quote_id + 1, quote=quote, movie=movie)
    quotes.append(new_quote)

    return {"quote": new_quote}, 201


@app.route("/api/quotes/<int:qid>", methods=["PUT"])
def update_quote(qid):
    if not request.json:
        abort(400)

    matching_quotes = _get_quote(qid)
    if len(matching_quotes) != 1:
        abort(404)

    update_quote = matching_quotes[0]
    update_quote["quote"] = request.json.get("quote") or update_quote["quote"]
    update_quote["movie"] = request.json.get("movie") or update_quote["movie"]

    return {"quote": update_quote}, 200


@app.route("/api/quotes/<int:qid>", methods=["DELETE"])
def delete_quote(qid):
    del_quote = _get_quote(qid)
    if len(del_quote) != 1:
        abort(404)

    quotes.remove(del_quote[0])
    return {}, 204
