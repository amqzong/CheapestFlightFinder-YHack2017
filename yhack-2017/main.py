# main.py
# Description: Allows users to input information on their university or departing location, destination, and which day
# they are planning to leave. If the university is inputted, it finds the closest airports to that university.
# The webapp employs flexible flight planning by looking at the best flights/deals during the week of the input date 
# (on the CSV file provided by JetBlue) and outputting the available flights sorted by most money saved.

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

            # currently hardcodes airports closest to each university, could be improved by automatically
            # detecting nearest airports through Google Maps API
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

            # currently hardcodes airports closest to each university, could be improved by automatically
            # detecting nearest airports through Google Maps API
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

if __name__ == '__main__':
    app.run()
