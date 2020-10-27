#!/usr/bin/env python
# coding: utf-8

# In[3]:


#import dependencies
import numpy as np
import sqlalchemy
import os
import pandas as pd
import datetime as dt
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, desc

from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()
Base.prepare(engine, reflect=True)


# In[ ]:


#Flask setup
app = Flask(__name__)

Measurement = Base.classes.measurement
Station = Base.classes.station


# In[ ]:


#Flask routes
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations"
        f"/api/v1.0/tobs"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    
    session = Session(engine)
 
    
    precipitation = session.query(Measurement)
    
    precipitation_df = pd.read_sql(precipitation.statement, con=engine)
    precipitation_df.set_index('date', inplace = True)

    precipitation_df.index = precipitation_df.index.astype('str')
    precipitation_dict = precipitation_df.to_dict()
    return jsonify(precipitation_dict)
    
 


@app.route("/api/v1.0/tobs")
def tobs():

    session = Session(engine)    
    monthly_dates = dt.date.fromisoformat(session.query(Measurement).order_by(desc(Measurement.date)).first().date)
    last_year = monthly_dates-dt.timedelta(days=365)
    

    tobs = session.query(Measurement).filter(last_year<Measurement.date)
    tobs_df = pd.read_sql(tobs.statement, con=engine)
    tobs_df.set_index('date', inplace = True)

    tobs_df.index = tobs_df.index.astype('str')
    tobs_df = tobs_df.to_dict()

    return jsonify(tobs_df)

    
@app.route("/api/v1.0/stations")
def stations():

    session = Session(engine)
    station = session.query(Measurement.station).group_by(Measurement.station)
    station_df = pd.read_sql(station.statement, con=engine)
    
    return jsonify(station_df.to_dict())

if __name__ == '__main__':
    app.run(debug=True)

