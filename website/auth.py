from email.policy import strict
import re
from unittest import result
from flask import Flask, jsonify, json,request
from flask import Blueprint,render_template, request,flash, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from .models import *
from .models import db
from requests import  get
from flask_marshmallow import Marshmallow
from marshmallow import Schema, fields
ma = Marshmallow(app)
db.init_app(app)

app.config['SECRET_KEY'] = "groupe5"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:groupe5@localhost/template1'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
 
auth = Blueprint('auth', __name__)



#########MARSMALLOW#############
class usersSchema(ma.Schema):
    
    id = fields.Integer()
    name = fields.String()
    username = fields.String()
    email = fields.String()
    phone = fields.String()
    website = fields.String()
    street = fields.String()
    suite = fields.String()
    city = fields.String()
    zipcode = fields.String()
    lat = fields.String()
    lng = fields.String()
    name_company = fields.String()
    catchPrase =  fields.String()
    bs = fields.String()
   
    
useSchema = usersSchema()
userSchema = usersSchema(many = True)


class postsSchema(ma.Schema):
       class Meta:
              fields = ("id","title","body","userId")
posSchema = postsSchema()
postSchema = postsSchema(many = True)



class albumsSchema(ma.Schema):
       class Meta:
              fields = ("id","title","userId")
albuSchema = albumsSchema()
albumSchema = albumsSchema(many = True)


class commentsSchema(ma.Schema):
       class Meta:
              fields = ("id","name","email","body","postId")
commenSchema = commentsSchema()
commentSchema = commentsSchema(many = True)


class todosSchema(ma.Schema):
       class Meta:
              fields = ("id","title","completed","userId")
todSchema = todosSchema()
todoSchema = todosSchema(many = True)


class photosSchema(ma.Schema):
       class Meta:
              fields = ("id","title","url","thumbnailUrl","albumId")
photSchema = photosSchema()
photoSchema = photosSchema(many = True)


#######USERS##########

# @auth.route("/users", methods = ["GET"])
# def users():
#    users = Users.query.filter_by(visibility = 1)
#    result = userSchema.dump(users)
#    return jsonify(result)

# @auth.route("/users/<id>", methods = ["GET"])
# def userId(id):
#    users = Users.query.get(id)
#    result = useSchema.dump(users)
#    return jsonify(result)

@auth.route("/users", methods = ["GET"])
def users():
   users = Users.query.filter_by(visibility=1)
   result=[]
   
   for u in users:
            user={'id':u.id,'name':u.name,'username':u.username,'email':u.email,'phone':u.phone,'website':u.website,'address':{'street':u.street,'suite':u.suite,'city':u.city,'zipcode':u.zipcode,'geo':{'lng':u.lng,'lat':u.lat}},'company':{'name_company':u.name_company,'catchPrase':u.catchPrase,'bs':u.bs}}
            result.append(user)
   return jsonify(result)

@auth.route("/users/<id>", methods = ["GET"])
def userId(id):
   u = Users.query.get(id).query.filter_by(visibility = 1).first()
   user={'id':u.id,'name':u.name,'username':u.username,'email':u.email,'phone':u.phone,'website':u.website,'address':{'street':u.street,'suite':u.suite,'city':u.city,'zipcode':u.zipcode,'geo':{'lng':u.lng,'lat':u.lat}},'company':{'name_company':u.name_company,'catchPrase':u.catchPrase,'bs':u.bs}}

   return jsonify(user)

@auth.route("/users", methods = ["POST"])
def createuser():
    data = request.get_json()
    new_users = Users(
        id = data.get("id"),
        name = data.get("name"),
        username = data.get("username"),
        email= data.get("email"),
        phone = data.get("phone"),
        website = data.get("website"),
        street = data.get("street"),
        suite = data.get("suite"),
        city = data.get("city"),
        zipcode = data.get("Zipcode"),
        lng = data.get("lng"),
        lat = data.get("lat"),
        name_company = data.get("name_company"),
        catchPrase = data.get("catchPrase"),
        bs = data.get("bs")
    )
    db.session.add(new_users)
    db.session.commit() 
    return jsonify(result), 201
    
@auth.route("/users/<id>", methods = ["PUT"])
def updateuser(id):
    updateuser = Users.query.get(id)   
    data = request.get_json()
    id = data.get("id"),
    updateuser.name = data.get("name"),
    updateuser.username = data.get("username"),
    updateuser.email= data.get("email"),
    updateuser.phone = data.get("phone"),
    updateuser.website = data.get("website"),
    updateuser.street = data.get("street"),
    updateuser.suite = data.get("suite"),
    updateuser.city = data.get("city"),
    updateuser.zipcode = data.get("Zipcode"),
    updateuser.lng = data.get("lng"),
    updateuser.lat = data.get("lat"),
    updateuser.name_company = data.get("name_company"),
    updateuser.catchPrase = data.get("catchPrase"),
    updateuser.bs = data.get("bs")
    db.session.commit() 
    result = useSchema.dump(updateuser)  
    return jsonify(result)

@auth.route("/posts/<id>", methods = ["DELETE"])
def deleteusers(id):
      deleteusers = Users.query.get(id).query.filter_by(visibility = 1)
      deleteusers.visibility = 0  
      return jsonify({"message":"user deleted"})
    
##########TODOS##########

@auth.route("/todos", methods = ["GET"])
def todos():
      todos = Todos.query.filter_by(visibility = 1)
      result = todoSchema.dump(todos)
      return jsonify(result)

@auth.route("/todos/<id>", methods = ["GET"])
def todoId(id):
      todos = Todos.query.get(id).query.filter_by(visibility = 1).first()
      result = todSchema.dump(todos)
      return jsonify(result)

@auth.route("/todos", methods = ["POST"])
def createtodos():
    data = request.get_json()
    new_todo = Todos(
        id = data.get("id"),
        title = data.get("title"),
        completed = data.get("completed"),
        userId = data.get("userId")
    )
    db.session.add(new_todo)
    db.session.commit()
    result = todSchema.dump(new_todo)   
    return jsonify(result), 201
    
@auth.route("/todos/<id>", methods = ["PUT"])
def updatetodos(id):
    updatetodo = Todos.query.get(id)   
    data = request.get_json()
    updatetodo.title = data.get("title")
    updatetodo.completed = data.get("completed")
    updatetodo.userId = data.get("userId")
    db.session.commit() 
    result = todSchema.dump(updatetodo)  
    return jsonify(result)

@auth.route("/users/<userId>/todos", methods = ["GET"])
def todosUserid(userId):
      yes = Todos.query.filter_by(userId = userId).all()
      return postSchema.jsonify(yes)



########POSTS############

@auth.route("/posts/<id>", methods = ["GET"])
def postid(id):
      postid = Posts.query.get(id).query.filter_by(visibility = 1).first()   
      return posSchema.jsonify(postid)


@auth.route("/posts/<id>", methods = ["PUT"])
def updatepostid(id):
    updatepostid = Posts.query.get(id).query.filter_by(visibility = 1).first()   
    data = request.get_json()
    updatepostid.title = data.get("title")
    updatepostid.body = data.get("body")
    updatepostid.userId = data.get("userId")
    db.session.commit() 
    result = posSchema.dump(updatepostid)  
    return jsonify(result)

@auth.route("/posts/<id>", methods = ["DELETE"])
def deletepostid(id):
      deletepostid = Posts.query.get(id).query.filter_by(visibility = 1)
      deletepostid.visibility = 0
      return jsonify({"message":"post deleted"})


@auth.route("/posts", methods = ["POST"])
def createpostid():
    data = request.get_json()
    new_post = Posts(
        id = data.get("id"),
        title = data.get("title"),
        body = data.get("body"),
        userId = data.get("userId")
    )
    db.session.add(new_post)
    db.session.commit()
    result = posSchema.dump(new_post)   
    return jsonify(result), 201


@auth.route("/users/<userId>/posts", methods = ["GET"])
def postUserid(userId):
      yes = Posts.query.filter_by(userId = userId).all()
      return postSchema.jsonify(yes)

@auth.route("/posts", methods = ["GET"])
def posts():
      posts = Posts.query.filter_by(visibility = 1)
      result = postSchema.dump(posts)
      return jsonify(result)
#######COMMENTS#############

@auth.route("/comments/<id>", methods = ["GET"])
def commentId(id):
      comments = Comments.query.get(id).query.filter_by(visibility = 1).first()
      result = commenSchema.dump(comments)
      return jsonify(result)

@auth.route("/comments", methods = ["POST"])
def createcomments():
    data = request.get_json()
    new_comment = Comments(
        id = data.get("id"),
        email = data.get("email"),
        name = data.get("name"),
        body = data.get("body"),
        postId = data.get("postId")
    )
    db.session.add(new_comment)
    db.session.commit()
    result = commenSchema.dump(new_comment)   
    return jsonify(result), 201

@auth.route("/comments/<id>", methods = ["PUT"])
def updatecomments(id):
    updatecomments = Comments.query.get(id)   
    data = request.get_json()
    updatecomments.name = data.get("name")
    updatecomments.email = data.get("email")
    updatecomments.body = data.get("body")
    updatecomments.albumId = data.get("albumId")
    db.session.commit() 
    result = commenSchema.dump(updatecomments)  
    return jsonify(result)


@auth.route("/posts/<postId>/comments", methods = ["GET"])
def commentpostId(postId):
      pot = Comments.query.filter_by(postId = postId).all()
      return commentSchema.jsonify(pot)

@auth.route("/comments", methods = ["GET"])
def comments():
      comments = Comments.query.filter_by(visibility = 1)
      result = commentSchema.dump(comments)
      return jsonify(result)
@auth.route("/comments/<id>", methods = ["DELETE"])
def deletecomments(id):
      deletecomments = Comments.query.get(id).query.filter_by(visibility = 0)
      if Comments.visibility == 0:
         db.session.query(Comments).filter_by(visibility = 0).first()
      db.session.delete(deletecomments)   
      return jsonify({"message":"comments deleted"})

#########ALBUMS###############

@auth.route("/albums", methods = ["GET"])
def albums():
      albums = Albums.query.filter_by(visibility = 1)
      result = albumSchema.dump(albums)
      return jsonify(result)

@auth.route("/albums/<id>", methods = ["GET"])
def albumId(id):

      albums = Albums.query.get(id).query.filter_by(visibility = 1).first()
      result = albuSchema.dump(albums)
      return jsonify(result)

@auth.route("/albums", methods = ["POST"])
def createalbums():
    data = request.get_json()
    new_album = Albums(
        id = data.get("id"),
        title = data.get("title"),
        userId = data.get("userId")
    )
    db.session.add(new_album)
    db.session.commit()
    result = albuSchema.dump(new_album)   
    return jsonify(result), 201
    
@auth.route("/albums/<id>", methods = ["PUT"])
def updatealbums(id):
    updatealbum = Photos.query.get(id)   
    data = request.get_json()
    updatealbum.title = data.get("title")
    updatealbum.userId = data.get("userId")
    db.session.commit() 
    result = albuSchema.dump(updatealbum)  
    return jsonify(result)

@auth.route("/users/<userId>/albums", methods = ["GET"])
def albumsuserId(userId):
      pot = Albums.query.filter_by(userId = userId).all()
      return albumSchema.jsonify(pot)

@auth.route("/albums/<id>", methods = ["DELETE"])
def deletealbums(id):
      deletealbums = Albums.query.get(id).query.filter_by(visibility = 1).first()
      deletealbums.visibility = 0
      if  deletealbums.visibility ==  0:
          Photos.query.filter_by(albumId = id, visibility = 0)
      return jsonify({"message":"albums deleted"})

##########PHOTOS################

@auth.route("/photos", methods = ["GET"])
def photos():
      photos = Photos.query.filter_by(visibility = 1)
      result = photoSchema.dump(photos)
      return jsonify(result)

@auth.route("/photos", methods = ["POST"])
def createphotos():
    data = request.get_json()
    new_photo = Photos(
        id = data.get("id"),
        title = data.get("title"),
        url = data.get("url"),
        thumbnailUrl = data.get("thumbnailUrl"),
        albumId = data.get("albumId")
    )
    db.session.add(new_photo)
    db.session.commit()
    result = photSchema.dump(new_photo)   
    return jsonify(result), 201
    
@auth.route("/photos/<id>", methods = ["PUT"])
def updatephotos(id):
    updatephoto = Photos.query.get(id)   
    data = request.get_json()
    updatephoto.title = data.get("title")
    updatephoto.url = data.get("url")
    updatephoto.thumbnailUrl = data.get("thumbnailUrl")
    updatephoto.albumId = data.get("albumId")
    db.session.commit() 
    result = photSchema.dump(updatephoto)  
    return jsonify(result)


@auth.route("/photos/<id>", methods = ["GET"])
def photoId(id):
      photos = Photos.query.get(id)
      result = photSchema.dump(photos)
      return jsonify(result)

@auth.route("/albums/<albumId>/photos", methods = ["GET"])
def photoalbumId(albumId):
      pot = Photos.query.filter_by(albumId = albumId).all()
      return photoSchema.jsonify(pot)

@auth.route("/photos/<id>", methods = ["DELETE"])
def deletephotos(id):
      deletephoto = Photos.query.get(id)
      if Photos.visibility == 0:
         db.session.query(Photos).filter_by(visibility = 0).first()
      db.session.delete(deletephoto)   
      return jsonify({"message":"photo deleted"})
##########SERVER ERROR#################
@auth.errorhandler(500)
def internal_server(error):
    return jsonify({"message":"internal error"}),500
##########PAGE NOT FOUND###############
@auth.errorhandler(404)
def not_found(error):
    return jsonify({"message":"page not found"}),404
       
###############CETTE TACHE PERMET A L'UTILISATEUR########################
###############DE CHARGER LES DONNEES DE L'API DANS LA BASE###############
#############IL EXISTE UN BOUTON DANS LA ROUTE HOME#######################
###################### VOUS POUVEZ LE CLICKER POUR CHARGER################
######################UNE FOIS FAIS C'EST TERMIN€ ########################
@auth.route("/", methods = ["GET","POST"])
def home():
  load_data("users")
  load_data("albums")
  load_data("posts")
  load_data("comments")
  load_data("photos")
  load_data("todos")

  return render_template("home.html")



































































###########FONCTIONS POUR LES DONNEES DE L'API#############
def searchapi(end):
    url = get('https://jsonplaceholder.typicode.com/'+end)
    return url.json()


def load_data(type):
    if type == 'users':
         
      users_from_apis= searchapi('users')

      for data in users_from_apis:
            perso = Users(id = data.get("id"),
               name = data.get("name"), 
                              username = data.get("username"), email = data.get("email"), 
                              phone = data.get("phone"),
                              website = data.get("website"), street = data["address"]["street"],
                              suite = data["address"]["suite"], 
                              city = data["address"]["city"],zipcode = data["address"]["zipcode"],
                              lng = data["address"]["geo"]["lat"], lat = data["address"]["geo"]["lat"],
                              name_company = data["company"]["name"], catchPrase = data["company"]["catchPhrase"],
                              bs = data["company"]["bs"])
            
            db.session.add(perso)
      db.session.commit()
            
    elif  type == 'posts':
        
        posts_from_apis= searchapi('posts') 

        for post in posts_from_apis:
            posts = Posts(
                id = post.get('id'),
                title = post.get('title'), 
                body = post.get('body'), 
                userId = post.get("userId")
            )

            db.session.add(posts)
        db.session.commit()
           
    elif type == "comments":
           
            comments_from_apis=searchapi('comments')

            for comment in comments_from_apis:
              
                comments = Comments(
                    id = comment.get("id"),
                    name = comment.get('name'), 
                    body= comment.get('body'),
                    email = comment.get('email'),
                    postId =comment.get("postId")
                )
         
            
                db.session.add(comments)
            db.session.commit()
      
       
    
    elif type == 'todos':
        todos = searchapi('todos')
        for todo in todos:
            todos = Todos(
            id = todo.get("id"),
            userId = todo.get("userId"),
            title =todo.get("title"),
            completed = todo.get("completed"))
            
       
            db.session.add(todos)
        db.session.commit()
            
    elif type == 'albums':
        albums_from_apis =searchapi('albums') 

        for album in albums_from_apis:
            albums = Albums(
                id = album.get('id'),
                title = album.get('title'),
                userId = album.get('userId')
               )
            
            db.session.add(albums)
        db.session.commit()
       
    elif type == 'photos':
            photos_from_apis= searchapi('photos')
            for photo in photos_from_apis:
                photos= Photos(
                    id = photo.get("id"),
                    albumId = photo.get("albumId"), 
                    title = photo.get("title"),
                    url = photo.get("url"),
                    thumbnailUrl = photo.get("thumbnailUrl"))
              
                db.session.add(photos)
            db.session.commit()
      
       
  
