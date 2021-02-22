import numpy as np
from flask import render_template
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy import inspect
from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///data/samples.db")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the tables
Counts = Base.classes.tweet_counts
StateAvg = Base.classes.state_avg
TimeAvg = Base.classes.time_avg
SentCount = Base.classes.sent_count
TimeTweets = Base.classes.time_tweets
StTweets = Base.classes.st_tweets

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def home():
    # Return template and data
    return render_template("index.html")

# Route for state sentiment bar chart data
@app.route("/statesent")

def statesent():

    session = Session(engine)
    results = session.query(StateAvg.state_code, StateAvg.BidenAvg, StateAvg.TrumpAvg).all()
    session.close()

    state_avg = []
    for state_code, BidenAvg, TrumpAvg in results:

        state_dict = {}
        state_dict["state_code"] = state_code
        state_dict["BidenAvg"] = BidenAvg
        state_dict["TrumpAvg"] = TrumpAvg
        state_avg.append(state_dict)
        
    return jsonify(state_avg)

# Route for time sentiment line chart data
@app.route("/timesent")

def timesent():

    session = Session(engine)
    results = session.query(TimeAvg.Date, TimeAvg.BidenAvg, TimeAvg.TrumpAvg).all()
    session.close()

    time_avg = []
    for Date, BidenAvg, TrumpAvg in results:

        time_dict = {}
        time_dict["date"] = Date
        time_dict["BidenAvg"] = BidenAvg
        time_dict["TrumpAvg"] = TrumpAvg
        time_avg.append(time_dict)

    return jsonify(time_avg)

# route for Sentiment count bar chart data
@app.route("/sentcounts")

def sentcounts():

    session = Session(engine)
    results = session.query(SentCount.analysis, SentCount.Biden_Count, SentCount.Trump_Count).all()
    session.close()

    sent_count = []
    for analysis, Biden_Count, Trump_Count in results:

        count_dict = {}
        count_dict["analysis"] = analysis
        count_dict["Biden_Count"] = Biden_Count
        count_dict["Trump_Count"] = Trump_Count

        sent_count.append(count_dict)
        
    return jsonify(sent_count)

# Buckley's time app.route
@app.route("/timetweets")
# change app name for mult routes
def timetweets():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query all sentiment data
    results = session.query(TimeTweets.created_at, TimeTweets.trump, TimeTweets.biden).all()

    session.close()

    # Create a dictionary from row of data and append to a list of dictionaries
    time_tweets = []
    for created_at, trump, biden in results:

        # if hashtag == "Biden":
        time_dict = {}
        time_dict["created_at"] = created_at
        time_dict["trump"] = trump
        time_dict["biden"] = biden
        

        time_tweets.append(time_dict)
        
    # turn the list of dicts into an array of objects
    return jsonify(time_tweets)

@app.route("/sttweets")
# change app name for mult routes
def sttweets():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query all sentiment data
    results = session.query(StTweets.state_code, StTweets.trump, StTweets.biden).all()

    session.close()

    # Create a dictionary from row of data and append to a list of dictionaries
    st_tweets = []
    for state_code, trump, biden in results:

        # state code
        st_dict = {}
        st_dict["state_code"] = state_code
        st_dict["trump"] = trump
        st_dict["biden"] = biden
        

        st_tweets.append(st_dict)
        
    # turn the list of dicts into an array of objects
    return jsonify(st_tweets)


if __name__ == '__main__':
    app.run(debug=True)