from flask import render_template, redirect, request, session
from recipes_app import app
from recipes_app.models.recipe import Recipe
from recipes_app.models.user import User

@app.route('/dashboard')
def dashboard():
    recipes = Recipe.get_all()
    user = User.get_by_id({ 'id' : session['user_id']})
    return render_template('/dashboard.html', user = user, recipes = recipes)

@app.route('/recipes/new')
def add_recipe():
    return render_template('/add_recipe.html')

@app.route('/create_recipe', methods=['post'])
def create_recipe():
    if not Recipe.validate_recipe(request.form):
        return redirect('/recipes/new')
    data = {
        'name' : request.form['name'],
        'description' : request.form['description'],
        'instructions' : request.form['instructions'],
        'created_at' : request.form['created_at'],
        'under_30' : request.form['under_30'],
        'user_id' : session['user_id']
    }
    print(data)
    new_recipe = Recipe.create_recipe(data)
    return redirect(f'/recipe/{new_recipe}')

@app.route('/recipe/<id>')
def show_recipe(id):
    
    user = User.get_by_id({ 'id' : session['user_id']})
    recipe = Recipe.get_ind({ 'id' : id })
    
    return render_template('/created_recipe.html', recipe = recipe, user = user)

@app.route('/recipes/edit/<id>')
def edit_recipe(id):
    user = User.get_by_id({ 'id' : session['user_id']})
    recipe = Recipe.get_ind({ 'id' : id })
    #session['recipe_id'] = recipe
    return render_template('/edit_recipe.html', recipe = recipe, user = user)

@app.route('/update_recipe/<id>', methods=['post'])
def update_recipe(id):
    print(request.form)
    if not Recipe.validate_recipe(request.form):
        return redirect(f'/recipes/edit/{request.form["id"]}')
    data = {
        'name' : request.form['name'],
        'description' : request.form['description'],
        'instructions' : request.form['instructions'],
        'created_at' : request.form['created_at'],
        'under_30' : request.form['under_30'],
        'id' : id
    }
    updated_recipe = Recipe.update_recipe(data)
    session['recipe'] = updated_recipe
    return redirect(f'/recipe/{updated_recipe}')

@app.route('/delete_recipe')
def delete_recipe(id):
    user = User.get_by_id({ 'id' : session['user_id']})
    recipe = Recipe.get_ind({ 'id' : id })
    return redirect('/dashboard', user = user, recipe = recipe)
