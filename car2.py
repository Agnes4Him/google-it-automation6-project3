#!/usr/bin/env python3

import json
import locale
import sys
import os
import emails
import reports


def load_data(filename):
  """Loads the contents of filename as a JSON file."""
  with open(filename) as json_file:
    data = json.load(json_file)
  return data


def format_car(car):
  """Given a car dictionary, returns a nicely formatted name."""
  return "{} {} ({})".format(
      car["car_make"], car["car_model"], car["car_year"])

def process_data(data):
  """Analyzes the data, looking for maximums.

  Returns a list of lines that summarize the information.
  """
  max_revenue = {"revenue": 0}
  max_dict = {}
  year_dict = {}
  car = {}
  model_sales = ""
  popular_year = 0
  total = 0
  for item in data:
    # Calculate the revenue generated by this model (price * total_sales)
    # We need to convert the price from "$1234.56" to 1234.56
    item_price = locale.atof(item["price"].strip("$"))
    item_revenue = item["total_sales"] * item_price
    if item_revenue > max_revenue["revenue"]:
      item["revenue"] = item_revenue
      max_revenue = item
    # TODO: also handle max sales
    max_dict[item["id"]] = item["total_sales"]
    max_sales = max(max_dict, key=max_dict.get)
    if item["id"] == max_sales:
      car = item["car"]
      model_sales = item["total_sales"]
    # TODO: also handle most popular car_year
    if item["car"]["car_year"] not in year_dict:
      year_dict[item["car"]["car_year"]] = 0
      year_dict[item["car"]["car_year"]] += item["total_sales"]
    else:
      year_dict[item["car"]["car_year"]] +=  item["total_sales"]
    popular_year = max(year_dict, key=year_dict.get)
  for k, v in year_dict.items():
      if k == popular_year:
        total = v

    summary = [
    "The {} generated the most revenue: ${}".format(
      format_car(max_revenue["car"]), max_revenue["revenue"]),
    "The {} had the most sales: {}".format(format_car(car), model_sales),
    "The most popular year was {} with {} sales.".format(popular_year, total)
  ]

  return summary


def cars_dict_to_table(car_data):
  """Turns the data in car_data into a list of lists."""
  table_data = [["ID", "Car", "Price", "Total Sales"]]
  for item in car_data:
    table_data.append([item["id"], format_car(item["car"]), item["price"], item["total_sales"]])
  return table_data

def main(argv):
  """Process the JSON data and generate a full report out of it."""
  data = load_data("/home/student-01-646faa095248/car_sales.json")
  summary = process_data(data)
  car_data = cars_dict_to_table(data)
  title = "Sales summary for last month"
  paragraph = summary[0] + "<br />" + summary[1] + "<br />" + summary[2]
  # TODO: turn this into a PDF report
  reports.generate("/tmp/cars.pdf", title, paragraph, car_data)

  # TODO: send the PDF report as an email attachment

  message = emails.generate("automation@example.com",  "{}@example.com".format(os.environ.get('USER')), "Sales summary for last month",  summary[0] + "\n" + summary[1]$
  emails.send(message)


if __name__ == "__main__":
  main(sys.argv)


