from flask import Flask, request,jsonify
from flask_restx import Api,Resource,fields, marshal_with
from config import DevConfig
from models import Recipe, user
from exts import db
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManger, create_access_token, create_refresh_token

app=Flask(__name__)

app.config.from_object(DevConfig)

#db = SQLAlchemy()
#DB_NAME = "database.db"

db.init_app(app)

migrate =Migrate(app,db)

JWTManger(app)

api=Api(app,doc='/docs')

#model(serialier)
recipe_model = api.model(
    "Recipe", 
    {
        "id":fields.Integer(),
        "title":fields.String(),
        "description":fields.String() 
    }
)

signup_model=api.model(
    "SignUp",{
        "username":fields.String(),
        "email":fields.String(),
        "password":fields.String()
    }
)

login_model=api.model(
    "Login",{
        "username":fields.String(),
        "password":fields.String()
    }
)

@api.route('/hello')
class HelloResource(Resource):
    def get(self):
        return {"message":"Hello World"}

@api.route('/signup')
class Signup(Resource):
    @api.marshal_with(signup_model)
    @api.expect(signup_model)
    def post(self):
        data=request.get_json()

        username=data.get('username')

        db_user = user.query.filter_by(username=username).first()

        if db_user is not None:
            return jsonify({"message":"User with username {username} already exit"})
        else:
            new_user=user(
                username=data.get('username'),
                email=data.get('email'),
                password=generate_password_hash(data.get('password'))
            )
            new_user.save()

            return jsonify({"message":"User created successfully"})
            

@api.route('/login')
class Login(Resource):

    @api.expect(login_model)
    def post(self):
        data=request.get_json()

        username = data.get('username')
        password = data.get('password')

        db_user=user.query.filter_by(username=username).first()

        if db_user and check_password_hash(db_user.password,password):

            access_tokem = create_access_token(identity=db_user.username)
            refresh_token = create_refresh_token(identity=db_user.username)

            return jsonify({"access toekn":access_tokem, "refresh_token":refresh_token})


@api.route('/logout')
class Logout(Resource):
    def post(self):
        pass



@api.marshal_with(recipe_model)
@api.route('/recipes')
class RecipesResources(Resource):

    @api.marshal_list_with(recipe_model)
    def get(self):
        """Get all recipes"""

        recipes=Recipe.query.all()

        return recipes

    @api.marshal_with(recipe_model)
    @api.expect(recipe_model)
    def post(self):
        """Create a new recipe"""

        data=request.get_json()

        new_recipe = Recipe(
            title=data.get('title'),
            description=data.get('description')
        )

        new_recipe.save()

        return new_recipe,201

@api.route('/recipe/<int:id>') 
class RecipeResource(Resource):

    @api.marshal_with(recipe_model)
    def get(self, id):
        """Get a recipe by id """
        recipe=Recipe.query.get_or_404(id)

        return recipe
        
    @api.marshal_with(recipe_model)
    def put(self, id):
        """Update recipe by id"""
        recipe_to_update=Recipe.query.get_or_404(id)
        data=request.get_json()

        recipe_to_update.update(data.get('title'),data.get('description'))

        return recipe_to_update

    @api.marshal_with(recipe_model)
    def delete(self, id):
        """delete a recipe by id"""
        recipe_to_delete=Recipe.query.get_or_404(id)
        
        recipe_to_delete.delete()

        return recipe_to_delete

        


@app.shell_context_processor
def make_shell_context():
    return {
        "db":db,
        "Recipe" : Recipe
    }
""""
def createdb():
    with app.app_context():
        db.create_all()
        print("Database created")
"""
if __name__ == '__main__':
    app.run()