from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime

db = SQLAlchemy()
app = Flask(__name__)
CORS(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://admin:WHQ21cd1c689742@commentdb.cyww6g5eerrg.us-east-1.rds.amazonaws.com:3306/comments_database?charset=utf8"
db.init_app(app)

class Comments(db.Model):
    __tablename__ = "comments"
    comment_id = db.Column('comment_id', db.Integer, primary_key=True)
    post_id = db.Column('post_id', db.Integer)
    user_id = db.Column('user_id', db.Integer)
    content = db.Column('content', db.Text)
    date = db.Column('date', db.String(200))

    def __init__(self, postId, userId, content):
        self.user_id = userId
        self.post_id = postId
        self.content = content
        self.date = str(datetime.now())

    def toJson(self):
        return {
            'comment_id': self.comment_id,
            'post_id': self.post_id,
            'user_id': self.user_id,
            'content': self.content,
            'date': self.date
        }

@app.route("/hello")
def helloworld():
    print('received')
    return "hello, client!"

@app.route("/comment/create", methods=["POST"])
def createComment():
    try:
        postId, content, userId = request.json['post_id'], request.json['content'], request.json['user_id']
        comment = Comments(postId, userId, content)
        db.session.add(comment)
        db.session.commit()
        ret = dict(success=True)
        return ret
    except Exception as e:
        print(e)
        ret = dict(success=False)
        return ret

@app.route("/comment/delete/", methods=['DELETE'])
def deleteComment():
    args = request.args
    try:
        if 'comment_id' in args:
            commentId = args.get('comment_id', type=int)
            comment = Comments.query.filter(Comments.comment_id == commentId)
            cnt = comment.delete()
            db.session.commit()
            ret = dict(success=True, cnt=cnt)
            return ret
    except Exception as e:
        print(e)
        ret = dict(success=False)
        return ret

@app.route("/comment/query", methods=["GET"])
def queryByPostId():
    args = request.args
    try:
        if 'post_id' in args:
            print(args.get('post_id', type=int))
            postId = args.get('post_id', type=int)
            comments = Comments.query.filter(Comments.post_id == postId).all()
            return {'success': True, 'content': [i.toJson() for i in comments]}
    except Exception as e:
        print(e)
        return {'success': False}

@app.route("/comment/update", methods=["POST"])
def updateByIdWithContent():
    try:
        commentId, content = request.json['comment_id'], request.json['content']
        comment = Comments.query.filter(Comments.comment_id == commentId).first()
        comment.content = content
        comment.date = str(datetime.now())
        db.session.add(comment)
        db.session.commit()
        return {'success': True}
    except Exception as e:
        print(e)
        return {'success': False}


if __name__ == '__main__':
    # with app.app_context():
    #     db.create_all()
    #     print("executed create_all")
    # print('out_context')
    app.run(host='0.0.0.0', debug=True, port=5011)