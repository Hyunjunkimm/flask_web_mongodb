
from flask import Flask , render_template, request
from werkzeug.utils import redirect
from data import Articles
#import pymysql
from pymongo import MongoClient
from flask_pymongo import PyMongo
from datetime import datetime
from bson import ObjectId


# db_connection = pymysql.connect(
# 	    user    = 'root',
#         passwd  = '1234',
#     	host    = '127.0.0.1',
#     	db      = 'gangnam',
#     	charset = 'utf8'
# )



app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb+srv://root:1234@cluster0.zvwqt.mongodb.net/modu?retryWrites=true&w=majority&tls=true&tlsAllowInvalidCertificates=true"

mongo = PyMongo(app)

list_collection = mongo.db.list


@app.route('/hello')
def hello_world():
    name="KIM"
    return render_template('index.html',data=name)

@app.route('/articles', methods=['GET', 'POST'])
def articles():
    list_data = Articles()
    # cursor = db_connection.cursor()
    # sql = 'SELECT * FROM list;'
    # cursor.execute(sql)
    # topics = cursor.fetchall()
    # print(topics)
    return render_template('articles.html', articles = list_data)



@app.route('/add_article', methods=['GET', 'POST'])
def add_article():
    if request.method == "GET":
        return render_template('add_article.html')
    else: 

        
        title = request.form["title"]
        desc = request.form["desc"]
        author = request.form["author"]
        #mongodb insert
        mongo_insert_data = {
            "title": title,
            "description": desc,
            "author": author,
            "creat_at": datetime.now()
        }
        list_collection.insert_one(mongo_insert_data)

        # mysql insert
        # cursor = db_connection.cursor()
        # sql = f"INSERT INTO list (title, description, author) VALUES ('{title}', '{desc}', '{author}');"
        # cursor.execute(sql)
        # db_connection.commit()

        return redirect('/articles_mongo')

@app.route('/<id>/delete', methods=['GET', 'POST'])
def delete_mongo(id):
#     # cursor = db_connection.cursor()
#     # sql = f'DELETE FROM list WHERE (id = {ids});'
#     # cursor.execute(sql)
#     # db_connection.commit()
      list_collection.delete_one({"_id":ObjectId(id)})
      return redirect('/articles_mongo')

 
@app.route('/detail_mongo/<ids>')
def detail_mongo(ids):

    topic = list_collection.find_one({"_id":ObjectId(ids)})
    print(topic)


    return render_template('article_mongo.html',article=topic)


@app.route('/<ids>/edit', methods=['GET', 'POST'])
def edit_article_mongo(ids):
    if request.method == 'GET':
        topic = list_collection.find_one({"_id":ObjectId(ids)})
        print(topic)
        return render_template('edit_article_mongo.html', article = topic)

    else:
        title = request.form["title"]
        desc = request.form["desc"]
        author = request.form["author"]
        myquery = { 
            "_id": ObjectId(ids)
            
            }
        newvalues = { "$set": { "title": title,
            "description":desc,
            "author":author,
            "create_at":datetime.now()  } }
        list_collection.update_one(myquery, newvalues)
        return redirect('/articles_mongo')

@app.route('/articles_mongo', methods=['GET', 'POST'])
def article_mongo():
    
    data = list_collection.find()
    print(data)
    return render_template('articles_mongo.html', articles =data)




if __name__ == '__main__':
    app.run(debug=True)

