import logging

from sanic import Sanic
# from sanic_mongo import Mongo
from sanic.response import json, text, html

from my_blueprint import bp

logging_format = "[%(asctime)s] %(process)d-%(levelname)s "
logging_format += "%(module)s::%(funcName)s():l%(lineno)d: "
logging_format += "%(message)s"

logging.basicConfig(
    format=logging_format,
    level=logging.DEBUG
)
log = logging.getLogger()


app = Sanic('test')
app.blueprint(bp)

db_settings = {
    'DB_HOST': 'localhost',
    'DB_NAME': 'appdb',
    'DB_USER': 'appuser'
}
app.config.update(db_settings)

# mongo_uri = "mongodb://{host}:{port}/{database}".format(
#     database='test',
#     port=27017,
#     host='localhost'
# )
#
# mongo = Mongo(mongo_uri)
# db = mongo(app)


@app.route("/")
async def index(request):
    # logger.info(f'Here is your log')
    log.info("received request; responding with 'hey'")
    # return json({"hello": "world"})
    return html('hello, mixin')


@app.route("/auth")
async def auth(request):
    return json({'auth': 'ok'})


@app.route("/json", methods=['POST'])
def post_json(request):
    return json({"received": True, "message": request.json})


@app.route("/query_string")
def query_string(request):
    return json({"parsed": True, "args": request.args, "url": request.url, "query_string": request.query_string})


@app.route("/test_request_args")
async def test_request_args(request):
    return json({
        "parsed": True,
        "url": request.url,
        "query_string": request.query_string,
        "args": request.args,
        "raw_args": request.raw_args,
        "query_args": request.query_args,
    })


@app.route("/files", methods=['GET', 'POST'])
def post_file(request):
    if request.method == 'POST':
        test_file = request.files.get('file')
        file_parameters = {
            # 'body': test_file.body,
            'name': test_file.name,
            'type': test_file.type,
        }
        return json({"received": True, "file_names": request.files.keys(), "test_file_parameters": file_parameters})
    elif request.method == 'GET':
        return html('''
            <!doctype html>
            <title>Upload new File</title>
            <h1>Upload new File</h1>
            <form method=post enctype=multipart/form-data>
              <input type=file name=file>
              <input type=submit value=Upload>
            </form>
            ''')


@app.route("/form", methods=['POST'])
def post_form(request):
    return json({"received": True, "form_data": request.form, "test": request.form.get('test')})


@app.route("/users", methods=["POST", ])
def create_user(request):
    return text("You are trying to create a user with the following POST: %s" % request.body)


@app.route("/read_cookie")
async def read_cookie(request):
    test_cookie = request.cookies.get('test')
    return text("Test cookie set to: {}".format(test_cookie))


@app.route("/write_cookie")
async def write_cookie(request):
    response = text("There's a cookie up in this response")
    response.cookies['test'] = 'It worked!'
    response.cookies['test']['domain'] = 'localhost'
    response.cookies['test']['httponly'] = True
    return response


@app.route("/delete_cookie")
async def test(request):
    response = text("Time to eat some cookies muahaha")
    # This cookie will be set to expire in 0 seconds
    # 该Cookie将设置为在0秒后过期
    del response.cookies['kill_me']
    # This cookie will self destruct in 5 seconds
    # 该Cookie将在5秒内自毁
    response.cookies['short_life'] = 'Glad to be here'
    response.cookies['short_life']['max-age'] = 5
    del response.cookies['favorite_color']
    # This cookie will remain unchanged
    # 该Cookie将保持不变
    response.cookies['favorite_color'] = 'blue'
    response.cookies['favorite_color'] = 'pink'
    del response.cookies['favorite_color']
    return response


@app.route('/tag/<tag>')
async def tag_handler(request, tag):
    print(f'tag: {tag}')
    return text('Tag - {}'.format(tag))


# @app.get('/objects')
# async def get(request):
#     docs = await db().test_col.find().to_list(length=100)
#     for doc in docs:
#         doc['id'] = str(doc['_id'])
#         del doc['_id']
#     return json(docs)
#
#
# @app.post('/objects')
# async def new(request):
#     doc = request.json
#     object_id = await db("test_col").save(doc)
#     return json({'object_id': str(object_id)})


if __name__ == "__main__":
    # app.run(host="0.0.0.0", port=1337, access_log=False, workers=4, debug=False)
    app.run(host="0.0.0.0", port=1337)
