import osa
import math


def read_temps_from_file(filename):
    temps = []
    with open(filename) as f:
        for line in f:
            temps.append(int(line.split()[0]))
    return temps


def read_currencies_from_file(filename):
    currencies = []
    with open(filename) as f:
        for line in f:
            currencies.append((int(line.split()[1]), line.split()[2]))
    return currencies


def read_miles_from_file(filename):
    miles = []
    with open(filename) as f:
        for line in f:
            modified_line = line.replace(',', '')
            miles.append(float(modified_line.split()[1]))
    return miles


def get_average_temp(filename):
    client = osa.Client('http://www.webservicex.net/ConvertTemperature.asmx?WSDL')
    temps = read_temps_from_file(filename)
    average_temps = sum(temps)/len(temps)
    response = client.service.ConvertTemp(average_temps, 'degreeFahrenheit', 'degreeCelsius')
    return round(response, 2)


def get_rubles_sum(filename):
    client = osa.Client('http://fx.currencysystem.com/webservices/CurrencyServer4.asmx?WSDL')
    currencies = read_currencies_from_file(filename)
    rubles = []
    for currency in currencies:
        rate = client.service.RateNum(baseCurrency=currency[1], toCurrency='RUB', rounding=True)
        rubles.append(math.ceil(currency[0]*rate))
    return sum(rubles)


def convert_miles_to_km(filename):
    client = osa.Client('http://www.webservicex.net/length.asmx?WSDL')
    miles = read_miles_from_file(filename)
    kilometers = []
    for mile in miles:
        kilometer = client.service.ChangeLengthUnit(mile, 'Miles', 'Kilometers')
        kilometers.append(round(kilometer, 2))
    return sum(kilometers)


if __name__ == '__main__':
    print(get_average_temp('temps.txt'))
    print(get_rubles_sum('currencies.txt'))
    print(convert_miles_to_km('travel.txt'))
