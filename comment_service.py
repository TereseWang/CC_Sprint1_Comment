from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://admin:dbuserdbuser@e6156cloud-computing.cvxubkmggxrp.us-east-1.rds.amazonaws.com:3306/comments_database?charset=utf8"
db.init_app(app)

class Comments(db.Model):
    __tablename__ = "comments"
    comment_id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    content = db.Column(db.Text)

    def __init__(self, postId, userId, content):
        self.user_id = userId
        self.post_id = postId
        self.content = content

    def toJson(self):
        return {
            'commentId': self.comment_id,
            'postId': self.post_id,
            'userId': self.user_id,
            'content': self.content
        }

@app.route("/hello")
def helloworld():
    print('received')
    return "hello, client!"

@app.route("/comment/create", methods=["POST"])
def createComment():
    try:
        postId, content, userId = request.form['postId'], request.form['content'], request.form['userId']
        comment = Comments(postId, userId, content)
        db.session.add(comment)
        db.session.commit()
        ret = dict(success=True)
        return ret
    except Exception as e:
        print(e)
        ret = dict(success=False)
        return ret

@app.route("/comment/delete/<commentId>", methods=['DELETE'])
def deleteComment(commentId):
    try:
        # comment = Comments.query.get(commentId)
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
        if 'postId' in args:
            print(args.get('postId', type=int))
            postId = args.get('postId', type=int)
            comments = Comments.query.filter(Comments.post_id == postId).all()
            return {'success': False, 'content': [i.toJson() for i in comments]}
    except Exception as e:
        print(e)
        return {'success': False}

@app.route("/comment/update", methods=["POST"])
def updateByIdWithContent():
    try:
        commentId, content = request.form['commentId'], request.form['content']
        comment = Comments.query.filter(Comments.comment_id == commentId).first()
        comment.content = content
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