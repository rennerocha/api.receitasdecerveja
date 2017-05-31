from flask import Flask
from flask import jsonify
from flask_cors import CORS
from pony import orm

import models

app = Flask(__name__)
CORS(app)


@app.route('/beerStyles')
def beer_styles():
    response = []
    with orm.db_session:
        all_beer_styles = orm.select(b for b in models.BeerStyle)[:]
        for beer_style in all_beer_styles:
            beer_style = beer_style.to_dict()
            response.append({
                'key': beer_style.get('key', ''),
                'text': beer_style.get('name', ''),
                'value': beer_style.get('key', ''),
            })
    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True)

# https://editor.ponyorm.com/user/rennerocha/receitasdecerveja#python-code
