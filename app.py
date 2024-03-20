from Configuration.DbConection.DbConnect import DbConnection
from Configuration.DbConection.queries import prods_query, stock_query
from dotenv import load_dotenv
from flask import Flask, jsonify, render_template
from flask_cors import CORS
import os


class DatabaseHandler:
    def __init__(self):
        load_dotenv()    
        self.db_conn = DbConnection(
            host=os.environ.get('HOST', False), 
            port=os.environ.get('PORT', False), 
            dbname=os.environ.get('DBNAME', False), 
            user=os.environ.get('USER', False), 
            password=os.environ.get('PASSWD', False)
        )

    def connect(self):
        return self.db_conn.connect()

    def execute_query(self, query):
        return self.db_conn.sqlquery(query)

class StockChecker:
    def __init__(self, database_handler):
        self.database_handler = database_handler

    def get_negative_stock_items(self, doc):
        result = self.database_handler.execute_query(prods_query.format(doc))
        negative_stock_items = []

        for res in result:
            qtitem =  res['qtorcamento']
            id = res['iddetalhe']
            cd = res['cdprincipal']
            des = res['dsdetalhe']
            stock_result = self.database_handler.execute_query(stock_query.format(id))
            stock_quantity = stock_result[0]['qtestoque']

            if stock_quantity < qtitem:
                negative_stock_items.append({
                    'estoque': stock_quantity,
                    'cdprincipal': cd,
                    'dsdetalhe': des
                })

        return negative_stock_items


app = Flask(__name__)
CORS(app)

@app.route('/')
def render_index():
    return render_template('index.html')


@app.route('/negativos/<doc>')
def get_negatives(doc):
    database_handler = DatabaseHandler()
    if not database_handler.connect():
        
        return jsonify({'error': str(database_handler.db_conn.error)})

    doc = '0000' + doc
    stock_checker = StockChecker(database_handler)
    negative_stock_items = stock_checker.get_negative_stock_items(doc)
    
    return jsonify(negative_stock_items)
    
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
