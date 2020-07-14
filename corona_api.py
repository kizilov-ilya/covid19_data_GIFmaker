import requests
import csv
import time
from tqdm import tqdm
from datetime import datetime, timedelta


def getListOfCountries():
    url = "https://covid-19-data.p.rapidapi.com/help/countries"

    querystring = {"format": "json"}

    headers = {
        'x-rapidapi-host': "covid-19-data.p.rapidapi.com",
        'x-rapidapi-key': "c4321c5facmshcf4333c19214808p1c12eajsn272a10f6802b"
    }
    time.sleep(0.5)
    response = requests.request("GET", url, headers=headers, params=querystring)
    print(f"Статус-код сети: {response.status_code}")
    data = response.json()
    all_countries = [data[i]['name'] for i in range(len(data))]
    return all_countries


print(getListOfCountries())


def getDailyReportByCountryName(country: str, date: str):
    url = "https://covid-19-data.p.rapidapi.com/report/country/name"

    querystring = {"date-format": "YYYY-MM-DD", "format": "json", "date": str(date), "name": str(country)}

    headers = {
        'x-rapidapi-host': "covid-19-data.p.rapidapi.com",
        'x-rapidapi-key': "c4321c5facmshcf4333c19214808p1c12eajsn272a10f6802b"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    return response.json()


def getConfirmed(country, date):
    time.sleep(1)
    data = getDailyReportByCountryName(country, date)
    data_dict = data[0]
    provinces = data_dict['provinces']
    provinces_dict: dict = provinces[0]

    if 'confirmed' in provinces_dict.keys():
        confirmed = provinces_dict['confirmed']
        return str(confirmed)
    return str(0)


# при отсутствии ключа возвращать на все позиции запроса нули 0


def getDeaths(country, date):
    time.sleep(1)
    data = getDailyReportByCountryName(country, date)
    data_dict = data[0]
    provinces = data_dict['provinces']
    provinces_dict = provinces[0]

    if 'deaths' in provinces_dict.keys():
        deaths = provinces_dict['deaths']
        return str(deaths)
    return str(0)


def getRecovered(country, date):
    time.sleep(1)
    data = getDailyReportByCountryName(country, date)
    data_dict = data[0]
    provinces = data_dict['provinces']
    provinces_dict = provinces[0]

    if 'recovered' in provinces_dict.keys():
        recovered = provinces_dict['recovered']
        return str(recovered)
    return str(0)


def createCsvDataFile(FILENAME: str, FILENAME_MOD: str, country: str):  # отсчет с 1 марта 2020 года
    headers = ['Date', 'Confirmed', 'Deaths', 'Recovered']
    days = []

    # date delta
    start_date = datetime(2020, 3, 1)
    date_delta = (datetime.now() - start_date).days
    print(f"Временная дельта: {date_delta} дн.")
    # НАПИСАТЬ ЦИКЛ сбора необходимых данных в списки то-есть 2 мерный массив
    for i in tqdm(range(date_delta)):
        query_date = start_date.date() + timedelta(days=int(i))

        days.append([f"{query_date}", f"{getConfirmed(country, query_date)}", f"{getDeaths(country, query_date)}",
                     f"{getRecovered(country, query_date)}"])

    with open(FILENAME, "w", newline="") as file:  # заполняем первою строку документа которая содержит заголовки
        writer = csv.writer(file)
        writer.writerow(headers)

    with open(FILENAME, "a", newline="") as file:  # заполняем первою строку документа которая содержит заголовки
        writer = csv.writer(file)
        writer.writerows(days)

    headers_mod = ['date', 'state', 'amount']
    days_mod = []

    for i in range(len(days)):
        if i <= 0:
            continue
        else:
            for j in range(3):
                days[i][j + 1] = int(days[i][j+1]) + int(days[i - 1][j + 1])

    for i in tqdm(range(date_delta)):

        if i <= 0:
            for j in tqdm(range(3)):  # 3 потому что для каждого поля
                days_mod.append([days[i][0], headers[j + 1], days[i][j + 1]])
                # необходимо для внесения первичного значения
        else:
            for j in tqdm(range(3)):
                days_mod.append([days[i][0], headers[j + 1], int(int(days[i][j + 1]))])
                # если не суммировать получим график сравнений относительно каждого дня

    with open(FILENAME_MOD, "w", newline='') as file:  # заполняем первою строку документа которая содержит заголовки
        writer = csv.writer(file)
        writer.writerow(headers_mod)

    with open(FILENAME_MOD, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(days_mod)


'''index_ukr =getListOfCountries().index("Ukraine")
print('index ukr =', index_ukr)'''


def enterCountry():
    try:
        search_country = int(input("Enter the number of country from the list: "))
        return search_country
    except ValueError as error:
        print(f"Type error, wrong type: {error}")
        enterCountry()


# config & test
FILENAME = ".\\users.csv"
FILENAME_MOD = ".\\users_mod.csv"
country_list = getListOfCountries()
country_dict = {i: country_list[i] for i in range(len(country_list))}
print(country_dict)

search_country = int(enterCountry())

createCsvDataFile(FILENAME, FILENAME_MOD, getListOfCountries()[search_country])

choosed_country = [country_list[search_country]]
file = ".\\choosed_country.csv"
with open(file, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(choosed_country)
'''
current_datetime = datetime.now()
print(type(current_datetime.date()))
'''
