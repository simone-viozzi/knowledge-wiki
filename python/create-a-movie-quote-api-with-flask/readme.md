# Create a movie quote API with Flask 

Implement a full-blown CRUD app to manage movie quotes using Flask. Implement the following routes:

```python
@app.route('/api/quotes', methods=['GET'])
@app.route('/api/quotes/', methods=['GET'])
@app.route('/api/quotes', methods=['POST'])
@app.route('/api/quotes/', methods=['PUT'])
@app.route('/api/quotes/', methods=['DELETE'])
```

To not distract you from the building API aspect, we just store the data in a list of dicts, in real life you would use a database though.

Make sure you check the tests for the required return codes for both good and bad calls to the API and use jsonify on your return data.