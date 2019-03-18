
import requests, bs4, ast, re
from configobj import ConfigObj

config = ConfigObj('config.ini')

def downloadpage():
    print('Downloading page https://www.nasdaq.com/earnings/report/aapl')

    res = requests.get('https://www.nasdaq.com/earnings/report/aapl')
    res.raise_for_status()

    soup = bs4.BeautifulSoup(res.text, features="html.parser")

    #Find the div that contains earnings date
    showdata = soup.find("div", {"id": "showdata-div"})

    #there are two tables on nasdaq website, pick the fist one
    tables = showdata.findChildren("table")
    my_table = tables[0]

    # Confirm that headers are expected
    table_headers = my_table.findChildren(['th'])
    #print('table_headers: \n', table_headers)
    valid_headers(table_headers)

    table_data = my_table.findChildren(['td'])
    print('table data: ', table_data)
    #Validate that the data is in the expected format
    valid_row_format(table_data)

    for cell in table_data:
        #if valid_row_format(cells):
        value = cell.string
        #print("The value in this cell is %s" % value)

def valid_headers(data):

    from configobj import ConfigObj
    config = ConfigObj('config.ini')

    table_headers = config['NASDAQ.COM']['HEADERS_VALUES']
    table_headers = table_headers.split(",")

    for index, item in enumerate(data):
        #Remove space which sometimes throws unexpected errors and convert to string to compare headers
        if str(table_headers[index]).strip() != str(data[index]).strip():
            raise NameError('The headers are different from expected')
            return False

    print('match:')
    return True

def valid_row_format(data):

    data_formats = config['NASDAQ.COM']['TABLE_DATA_FORMATS']

    i = 0
    for key, value in data_formats.items():
        r = re.compile(value)
        tdstring = str(data[i])
        i = i + 1

        #Since it is a pain in the a$$ to do regex, going to remove all <td> tags and for simplier comparison
        clean_string = tdstring.replace('<td>', '').replace('</td>', '')

        if r.match(clean_string) is not None:
            print ('matches')
        else:
            raise NameError('The values are different from expected')
            return False

    return True


def lambda_handler(event, context):

    downloadpage()


downloadpage()