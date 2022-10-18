#!/usr/bin/env python3

import json

data = {}
year_sales = 0
with open("./car_sales.json") as json_file:
  data = json.load(json_file)
for item in data:
  if item["car"]["car_year"] == 2007:
    year_sales = year_sales + item["total_sales"]
print(year_sales)
