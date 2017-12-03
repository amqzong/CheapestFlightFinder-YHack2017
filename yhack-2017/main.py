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
from operator import itemgetter, attrgetter
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

            if university == 'Yale':
                departure = 'BDL'
                departure2 = 'JFK'
            elif university == 'Brown':
                departure = 'PVD'
                departure2 = 'BOS'
            elif university == 'Columbia':
                departure = 'LGA'
                departure2 = 'JFK'
            if ((row[1] == departure or row[1] == departure2)
            and row[2] == destination and flightYear == year
                and flightMonth == month and (int(flightDay) <= int(day)+3 and int(flightDay) >= int(day)-3)):
                dealsAv.append(row[0:7])
        dealsAv = sorted(dealsAv, key= itemgetter(6))
        # dealsAv = dealsAv.sort(key = lambda row: row[6])

    with open('LowestFares.csv') as csvLowestFares:
        lowestFares = csv.reader(csvLowestFares, delimiter=',')
        lowestFaresAv = []
        array1 = []
        array2 = []
        for row in lowestFares:
            flightDate = row[2]
            flightYear = flightDate[6:10]
            flightMonth = flightDate[0:2]
            flightDay = flightDate[3:5]

            if university == 'Yale':
                departure = 'BDL'
                departure2 = 'JFK'
            elif university == 'Brown':
                departure = 'PVD'
                departure2 = 'BOS'
            elif university == 'Columbia':
                depature = 'LGA'
                departure2 = 'JFK'

            if ((row[0] == departure or row[0]==departure2)
            and row[1] == destination and flightYear == year
                and flightMonth == month and (int(flightDay) <= int(day)+3 and int(flightDay) >= int(day)-3)):
                array1.append(row[0:6])

        # lowestFaresAv = sorted(lowestFaresAv, key= itemgetter(5))
        for row in array1:
            price = float(row[5])
            array2.append(price)

        index = sorted(range(len(array2)), key=lambda k: array2[k])
        for i in range(0, len(index)):
            price = array1[index[i]]
            lowestFaresAv.append(price)


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
