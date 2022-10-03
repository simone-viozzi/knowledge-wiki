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
    """Recommended helper"""
    return next((quote for quote in quotes if quote["id"] == qid), None)


def _quote_exists(existing_quote):
    """Recommended helper"""

    # check if existing_quote is in quotes whitout considering the id
    return any(
        quote["quote"] == existing_quote["quote"]
        and quote["movie"] == existing_quote["movie"]
        for quote in quotes
    )


@app.route("/api/quotes", methods=["GET"])
def get_quotes():
    """Return all quotes"""
    return jsonify({"quotes": quotes})


@app.route("/api/quotes/<int:qid>", methods=["GET"])
def get_quote(qid):
    """Return quote with matching id"""
    quote = _get_quote(qid)
    if not quote:
        abort(404)
    return jsonify({"quotes": [quote]})


@app.route("/api/quotes", methods=["POST"])
def create_quote():
    """Create a new quote"""
    if (
        not request.json
        or "quote" not in request.json
        or "movie" not in request.json
        or _quote_exists(request.json)
    ):
        abort(400)
    quote = {
        "id": quotes[-1]["id"] + 1,
        "quote": request.json["quote"],
        "movie": request.json["movie"],
    }
    quotes.append(quote)
    return jsonify({"quote": quote}), 201


@app.route("/api/quotes/<int:qid>", methods=["PUT"])
def update_quote(qid):
    """Update an existing quote"""
    quote = _get_quote(qid)
    if not quote:
        abort(404)
    if not request.json:
        abort(400)
    if "quote" not in request.json or type(request.json["quote"]) is not str:
        abort(400)
    if "movie" not in request.json or type(request.json["movie"]) is not str:
        abort(400)

    quote["quote"] = request.json.get("quote", quote["quote"])
    quote["movie"] = request.json.get("movie", quote["movie"])
    return jsonify({"quote": quote})


@app.route("/api/quotes/<int:qid>", methods=["DELETE"])
def delete_quote(qid):
    """Delete quote with matching id"""
    quote = _get_quote(qid)
    if not quote:
        abort(404)
    quotes.remove(quote)
    return jsonify({"result": True}), 204
