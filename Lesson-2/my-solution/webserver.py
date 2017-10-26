from http.server import HTTPServer, BaseHTTPRequestHandler
import cgi
import os.path
from urllib.parse import parse_qs, urlparse
from database_setup import Base, Restaurant, MenuItem
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Create session and connect to DB
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


class webServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            if self.path.endswith("/restaurants"):
                restaurants = session.query(Restaurant).all()
                output = ""
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output += "<html><body><a href='/restaurants/new'><h1>Make a restaurant here!</h1></a>"
                for restaurant in restaurants:
                    output += restaurant.name
                    id =restaurant.id
                    output += "<br><a href='/restaurants/{}/edit'>Edit</a><br>".format(id)
                    output += "<a href='/restaurants/{}/delete'>Delete</a><br><br>".format(id)
                    output += "</body></html>"
                self.wfile.write(output.encode())
                return
            elif self.path.endswith("/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body><h1>Enter the name of the new restaurant:</h1>"
                output += "<form method='POST'><input type='text' name='restaurant'><br><input type='submit' value='Make a new restaurant!'></form>"
                output += "</body></html>"
                self.wfile.write(output.encode())
                return
            elif self.path.endswith("/edit"):
                output = ""
                restaurant_id = os.path.split(os.path.split(urlparse(self.path).path)[0])[1]
                restaurant_name = session.query(Restaurant).filter(Restaurant.id == restaurant_id).first().name
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output += "<html><body><h1>{}</h1><br>"
                output += "<form method='POST'><input type='text' name='new-name'><input type='submit' value='Give it a new name!'></form></body></html>"
                output = output.format(restaurant_name)
                self.wfile.write(output.encode())
                return
            elif self.path.endswith("/delete"):
                output = ""
                restaurant_id = os.path.split(os.path.split(urlparse(self.path).path)[0])[1]
                restaurant_name = session.query(Restaurant).filter(Restaurant.id == restaurant_id).first().name
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output += "<html><body><h1>Are you sure you want to delete {}?</h1><br>"
                output += "<form method='POST'><input type='submit' value='Delete'></form></body></html>"
                output = output.format(restaurant_name)
                self.wfile.write(output.encode())
                return
            else:
            	self.send_error(404, 'File Not Found: %s' % self.path)
        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)

    def do_POST(self):
        try:
            if self.path.endswith("/restaurants/new"):
                length = int(self.headers.get('Content-length', 0))
                data = self.rfile.read(length).decode()
                restaurant_name = parse_qs(data)["restaurant"][0]
                restaurant1 = Restaurant(name=restaurant_name)
                session.add(restaurant1)
                session.commit()
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()
                return
            elif self.path.endswith("/edit"):
                length = int(self.headers.get('Content-length', 0))
                data = self.rfile.read(length).decode()
                new_name = parse_qs(data)["new-name"][0]
                restaurant_id = os.path.split(os.path.split(urlparse(self.path).path)[0])[1]
                restaurant_to_edit = session.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
                restaurant_to_edit.name = new_name
                session.add(restaurant_to_edit)
                session.commit()
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()
            elif self.path.endswith("/delete"):
                restaurant_id = os.path.split(os.path.split(urlparse(self.path).path)[0])[1]
                restaurant_to_delete = session.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
                session.delete(restaurant_to_delete)
                session.commit()
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()
            else:
                self.send_error(404, 'File Not Found: %s' % self.path)
        except IOError:
        	self.send_error(404, 'File Not Found: %s' % self.path)

def main():
    try:
        server = HTTPServer(('', 8080), webServerHandler)
        print('Web server running...open localhost:8080/restaurants in your browser')
        server.serve_forever()
    except KeyboardInterrupt:
        print('^C received, shutting down server')
        server.socket.close()

if __name__ == '__main__':
    main()
