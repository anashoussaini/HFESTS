from flask import Flask, render_template, request, jsonify
import mysql.connector

app = Flask(__name__)

# Configure MySQL connection
mysql_config = {
  'user': 'wac353_4',
  'password': 'db3535', # replace with your actual password
  'host': 'wac353.encs.concordia.ca',
  'port': 3306,
  'database': 'wac353_4'
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/execute', methods=['POST'])
def execute():
    query = request.form['query']

    # create a new MySQL connection object
    conn = mysql.connector.connect(**mysql_config)

    # execute query and return result as JSON
    cursor = conn.cursor()
    cursor.execute(query)


    if cursor.description is not None:
        # if the query is a SELECT query, return the result set as JSON
        headers = [i[0] for i in cursor.description]
        result = cursor.fetchall()
        tablesql = render_template('table.html', headers=headers, result_set=result)
    else:
        # if the query is a DDL or DML query, return the number of affected rows as JSON
        result = cursor.rowcount

        # if the query is an INSERT or DELETE query, commit the changes
        if query.strip().lower().startswith('insert') or query.strip().lower().startswith('delete') or query.strip().lower().startswith('insert') :
            conn.commit()
            tablesql = jsonify(result=result)
    # close the MySQL connection
    conn.close()


    return tablesql

if __name__ == '__main__':
    app.run(debug=True)
