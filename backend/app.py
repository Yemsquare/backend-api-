from flask import Flask, request
from flask_restx import Api,Resource,fields, marshal_with
from config import DevConfig
from models import Recipe
from exts import db

app=Flask(__name__)

app.config.from_object(DevConfig)

#db = SQLAlchemy()
#DB_NAME = "database.db"

db.init_app(app)


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


@api.route('/hello')
class HelloResource(Resource):
    def get(self):
        return {"message":"Hello World"}


@api.marshal_with(recipe_model)
@api.route('/recipes')
class RecipesResources(Resource):

    @api.marshal_list_with(recipe_model)
    def get(self):
        """Get all recipes"""

        recipes=Recipe.query.all()

        return recipes

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