from datetime import datetime

import requests
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from flask import Flask, render_template, request

app = Flask(__name__)
Base = declarative_base()
# this is a horrible practice to hard-code credentials, but it's a PoC app only
engine = create_engine("postgresql://docker:docker@dv1562_lab2_db_1/dv1562_lab2_db_1",
                       pool_size=10, max_overflow=20)
Session = sessionmaker(bind=engine)


# Class representing the column in the database
class Request(Base):
    __tablename__ = 'requests'
    id = Column(Integer, primary_key=True)
    city = Column(String(100))
    timestamp = Column(DateTime())


# save the city request in the database
def save_city(city):
    session = Session()
    new_request = Request(city=city, timestamp=datetime.utcnow())
    session.add(new_request)
    session.commit()
    session.close()


# get all the previous city queries
def get_cities():
    session = Session()
    cities = [r.city for r in session.query(Request.city).distinct()]
    session.close()
    return cities


# main page, returned when one nagivates to 127.0.0.1
@app.route("/", methods=['GET'])
def hello():
    cities = get_cities()
    return render_template("main.html", cities=(cities if cities else ""))


# called when user requests weather in a city
@app.route("/", methods=['POST'])
def weather():
    city = request.form.get("city")
    if not city:
        return render_template("main.html")
    url = "https://wttr.in/" + city + ".png"
    filename = city + ".png"

    r = requests.get(url, allow_redirects=True)
    print("Here I am again")
    # save the images in a volume
    open("static/images/"+filename, 'wb').write(r.content)
    # save the request in the database
    save_city(city)

    # get the list of cities requested so far.
    cities = get_cities()
    return render_template("main.html", city=city, filename=filename, cities=(cities if cities else ""))


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
