from flask import Flask, render_template, url_for, request, redirect, flash, get_flashed_messages
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
def restaurantList():
    restaurants = session.query(Restaurant).all()
    output = ''
    for r in restaurants:
        output += "<ul><a href='{}''>{}</a></ul>".format(url_for('restaurantMenu', restaurant_id=r.id), r.name)
        output += '<br>'
    return output


@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id)
    output = ''
    messages = get_flashed_messages()
    for m in messages:
        if m:
            output += m
            output += '<br><br>'
    for i in items:
        output += i.name
        output += '</br>'
        output += '<a href=\'/restaurants/{}/{}/edit\'>edit name of the course</a><br>'.format(restaurant_id, i.id)
        output += i.price
        output += '</br>'
        output += i.description
        output += '</br>'
        output += '</br>'

    return output


@app.route('/restaurants/<int:restaurant_id>/new', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):

    if request.method == 'POST':
        newItem = MenuItem(name=request.form['name'], description=request.form[
                           'description'], price=request.form['price'], course=request.form['course'], restaurant_id=restaurant_id)
        session.add(newItem)
        session.commit()
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template('newmenuitem.html', restaurant_id=restaurant_id)


@app.route('/restaurants/<int:restaurant_id>/<int:MenuID>/edit', methods=['GET', 'POST'])
def editMenuItem(restaurant_id, MenuID):
    editedItem = session.query(MenuItem).filter(MenuItem.id == MenuID).one()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        session.add(editedItem)
        session.commit()
        flash("Name edited!")
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template('editmenuitem.html', restaurant_id=restaurant_id, MenuID=MenuID, item=editedItem)


@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/delete/')
def deleteMenuItem(restaurant_id, menu_id):
    return "page to delete a new menu item."

if __name__ == '__main__':
    app.secret_key = "my key"
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
