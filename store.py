from bottle import route, run, template, static_file, get, post, delete, request
from sys import argv
import json
import pymysql

connection = pymysql.connect(host='localhost',
                             user='root',
                             password='mysql25II',
                             db='office',
                             charset='utf8',
                             cursorclass=pymysql.cursors.DictCursor)


@get("/admin")
def admin_portal():
    return template("pages/admin.html")


@get("/")
def index():
    return template("index.html")


@get('/js/<filename:re:.*\.js>')
def javascripts(filename):
    return static_file(filename, root='js')


@get('/css/<filename:re:.*\.css>')
def stylesheets(filename):
    return static_file(filename, root='css')


@get('/images/<filename:re:.*\.(jpg|png|gif|ico)>')
def images(filename):
    return static_file(filename, root='images')


@post("/category")
def new_category():
    try:
        with connection.cursor() as cursor:
            newcatname = request.forms.get("name");
            sql2 = "SELECT name FROM categories"
            cursor.execute(sql2)
            result = cursor.fetchall()
            if (newcatname == ""):
                dict = {
                    "STATUS": "ERROR",
                    "MSG": "name parameter is missing",
                    "CODE": "400"
                }
                return json.dumps(dict)
            elif newcatname in [d['name'].lower() for d in result]:
                dict = {
                    "STATUS": "ERROR",
                    "MSG": "category already exists",
                    "CODE": "200"
                }
                return json.dumps(dict)
            else:
                sql = "INSERT INTO categories VALUES({},'{}')".format("NULL", newcatname)
                cursor.execute(sql)
                dict = {
                    "STATUS": "SUCCESS",
                    "CAT_ID": "",
                    'MSG': "category created successfully",
                    'CAT_ID': cursor.lastrowid,
                    "CODE": "201"
                }
                return json.dumps(dict)
    except:
        dict = {
            "STATUS": "ERROR",
            "MSG": "internal error",
            "CATEGORIES": "",
            "CODE": "500"
        }
        return json.dumps(dict)


@delete("/category/<id>")
def delete_category(id):
    try:
        with connection.cursor() as cursor:
            sql2 = "SELECT id FROM categories"
            cursor.execute(sql2)
            result = cursor.fetchall()
            if int(id) in [d['id'] for d in result]:
                sql = "DELETE FROM categories WHERE id={}".format(int(id))
                cursor.execute(sql)
                dict = {
                    "STATUS": "SUCCESS",
                    "CAT_ID": "",
                    "CODE": "201"
                }
                return json.dumps(dict)
            else:
                dict = {
                    "STATUS": "ERROR",
                    "MSG": "category not found",
                    "CODE": "404"
                }
                return json.dumps(dict)
    except:
        dict = {
            "STATUS": "ERROR",
            "MSG": "internal error",
            "CATEGORIES": "",
            "CODE": "500"
        }
        return json.dumps(dict)


@get("/categories")
def store():
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM categories"
            cursor.execute(sql)
            result = cursor.fetchall()
            dict = {
                "STATUS": "SUCCESS",
                "CATEGORIES": result,
                "CODE": "200"
            }
            return json.dumps(dict)
    except:
        dict = {
            "STATUS": "ERROR",
            "MSG": "internal error",
            "CATEGORIES": "",
            "CODE": "500"
        }
        return json.dumps(dict)


@post("/product")
def new_product():
    try:
        with connection.cursor() as cursor:
            title = request.POST.get('title')
            descri = request.POST.get('desc')
            price = int(request.POST.get('price'))
            img_url = request.POST.get('img_url')
            category = request.POST.get('category')
            favorite = 1 if request.POST.get('favorite') == 'on' else 0
            sql2 = "SELECT id FROM categories WHERE id = {}".format(category)
            cursor.execute(sql2)
            result = cursor.fetchall()

            if not result:
                dict = {
                    "STATUS": "ERROR",
                    "MSG": "category not found",
                    "PRODUCT_ID": "",
                    "CODE": "404"
                }
                return json.dumps(dict)

            else:
                sql2 = """INSERT IGNORE INTO product (title, descri, price, img_url, category, favorite) 
                       VALUES ('{}', '{}', {}, '{}', {}, {});"""
                dict = {
                    "STATUS": "SUCCESS",
                    'MSG': "product created/updated successfully",
                    'PRODUCT_ID': cursor.lastrowid,
                    "CODE": "201"
                }
                connection.commit()
                return json.dumps(dict)

    except pymysql.err.InternalError:
        dict = {
            "STATUS": "ERROR",
            "MSG": "bad request",
            "PRODUCT ID": "",
            "CODE": "400"
        }
        return json.dumps(dict)

    except Exception:
        dict = {
            "STATUS": "ERROR",
            "MSG": "internal error",
            "CATEGORIES": "",
            "CODE": "500"
        }
        return json.dumps(dict)


@get("/product/<id>")
def add_product(id):
    try:
        with connection.cursor() as cursor:
            sql2 = "SELECT * FROM product WHERE id={}".format(id)
            cursor.execute(sql2)
            result = cursor.fetchall()
            dict = {
                "STATUS": "SUCCESS",
                'PRODUCT_ID': result,
                "CODE": "201"
            }
            connection.commit()
            return json.dumps(dict)

    except pymysql.err.InternalError:
        dict = {
            "STATUS": "ERROR",
            "MSG": "category not found",
            "PRODUCT ID": "",
            "CODE": "404"
        }
        return json.dumps(dict)

    except Exception:
        dict = {
            "STATUS": "ERROR",
            "MSG": "internal error",
            "CATEGORIES": "",
            "CODE": "500"
        }
        return json.dumps(dict)


@delete("/product/<id>")
def delete_product():
    try:
        with connection.cursor() as cursor:
            sql2 = "SELECT id FROM product WHERE id={}".format(id)
            cursor.execute(sql2)
            dict = {
                "STATUS": "SUCCESS",
                "CODE": "201"
            }
            connection.commit()
            return json.dumps(dict)

    except pymysql.err.InternalError:
        dict = {
            "STATUS": "ERROR",
            "MSG": "category not found",
            "CODE": "404"
        }
        return json.dumps(dict)

    except Exception:
        dict = {
            "STATUS": "ERROR",
            "MSG": "internal error",
            "CODE": "500"
        }
        return json.dumps(dict)


@get("/products")
def products():
    try:
        with connection.cursor() as cursor:
            sql2 = "SELECT * FROM product"
            cursor.execute(sql2)
            result = cursor.fetchall()
            dict = {
                "STATUS": "SUCCESS",
                "PRODUCT_ID": result,
                "CODE": "200"
            }
            return json.dumps(dict)
    except:
        dict = {
            "STATUS": "ERROR",
            "MSG": "internal error",
            "PRODUCT_ID": "",
            "CODE": "500"
        }
        return json.dumps(dict)


@get("/category/<id>/products")
def category_products(id):
    try:
        with connection.cursor() as cursor:
            sql2 = "SELECT * FROM product WHERE category={}".format(id)
            cursor.execute(sql2)
            result = cursor.fetchall()
            dict = {
                "STATUS": "SUCCESS",
                'PRODUCT_ID': result,
                "CODE": "201"
            }
            return json.dumps(dict)

    except pymysql.err.InternalError:
        dict = {
            "STATUS": "ERROR",
            "MSG": "category not found",
            "PRODUCT ID": "",
            "CODE": "404"
        }
        return json.dumps(dict)

    except Exception:
        dict = {
            "STATUS": "ERROR",
            "MSG": "internal error",
            "CATEGORIES": "",
            "CODE": "500"
        }
        return json.dumps(dict)


run(host='0.0.0.0', port=7000)

