# Import packages
import requests
import json
import pandas as pd
from datetime import datetime, timedelta
import numpy as np
import time

def flattenDict(dd, separator ='_', prefix =''):
    return {prefix + separator + k if prefix else k : v
            for kk, vv in dd.items()
            for k, v in flattenDict(vv, separator, kk).items()
            } if isinstance(dd, dict) else { prefix : dd }
			
class singaporeAirTemperature:
    
    def __init__(self, startDate, numDays):
        presentDate = datetime.today()
        presentDateString = presentDate.strftime("%Y-%m-%d")
        try:
            startDateType = datetime.strptime(startDate, "%Y-%m-%d")
        except ValueError:
            return print("Invalid date format. Please follow format YYYY-MM-DD.")
        numDaysMax = (presentDate - startDateType).days
        self.startDate = startDate
        self.startDateType = startDateType
        if numDaysMax > 1:
            dateList = [numDays, numDaysMax]
            numDaysIndex = np.argmin(dateList, axis = 0) 
            numDays = dateList[numDaysIndex]
            self.numDays = numDays
            self.dates = [self.startDateType + timedelta(days = i) for i in range(0, (self.numDays))]
        else:
            raise Exception(f"Number of days between {self.startDate} and {presentDateString} is less than 1 day")
            
    def getData(self):
        url = "https://api.data.gov.sg/v1/environment/air-temperature"
        headers = {"accept": "application/json"}
        dataJsonList = []
        counter = 0
        print("Begin data loading...")
        for i in [j.strftime("%Y-%m-%d") for j in self.dates]:
            params = {"date": i}
            response = requests.request("GET", url, headers = headers, params = params)
            time.sleep(3)
            data = response.text
            dataJson = json.loads(data)
            dataJsonList.append(dataJson)
            counter += 1
            numDaysRemaining = self.numDays - counter
            print(f"Data loaded for date {i} with {numDaysRemaining} days remaining...")
            if counter == self.numDays:
                print("Data loading completed.")  
        return dataJsonList
    
    def loadData(self):
        dataJsonList = self.getData()
        dfReadings = pd.DataFrame()
        for i in dataJsonList[0]["items"]:
            timestamp = i["timestamp"]
            dfR = pd.DataFrame(i["readings"])
            dfR["timestamp"] = i["timestamp"]
            dfReadings = pd.concat([dfReadings, dfR], axis = 0)
            dfReadings = dfReadings.reset_index(drop = True)
        dfStations = pd.DataFrame()
        for j in dataJsonList:
            for k in j["metadata"]["stations"]:
                dfS = pd.DataFrame([flattenDict(k)])
                dfStations = pd.concat([dfStations, dfS], axis = 0)
                dfStations = dfStations.reset_index(drop = True)
        print(f"Size of dfReadings: {dfReadings.shape}\nSize of dfStations: {dfStations.shape}")
        return dfReadings, dfStations
		