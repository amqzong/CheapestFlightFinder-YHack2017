#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from flask import Flask, render_template, request
app = Flask(__name__)

import csv

@app.route('/form')
def form():
    return render_template('form.html')

@app.route('/submitted', methods=['POST'])
def submitted_form():
    university = request.form['university']
    departure = request.form['departure']
    destination = request.form['destination']
    year = request.form['year']
    month = request.form['month']
    day = request.form['day']


    with open('Deals.csv') as csvDeals:
        deals = csv.reader(csvDeals, delimiter=',')
        dealsAv = []
        for row in deals:
            flightDate = row[3]
            flightYear = flightDate[0:4]
            flightMonth = flightDate[5:7]
            flightDay = flightDate[8:10]


            if (row[1] == departure and row[2] == destination and flightYear == year
                and flightMonth == month and flightDay == day):
                dealsAv.append(row[0:7])

    with open('LowestFares.csv') as csvLowestFares:
        lowestFares = csv.reader(csvLowestFares, delimiter=',')
        lowestFaresAv = []
        for row in lowestFares:
            flightDate = row[2]
            flightYear = flightDate[6:10]
            flightMonth = flightDate[0:2]
            flightDay = flightDate[3:5]

            if (row[0] == departure and row[1] == destination and flightYear == year
                and flightMonth == month and flightDay == day):
                lowestFaresAv.append(row[0:6])
    
    
    return render_template(
    'submitted_form.html',
    university=university,
    departure=departure,
    destination=destination,
    year=year,
    month=month,
    day=day,
    dealsAv=dealsAv,
    lowestFaresAv=lowestFaresAv)
