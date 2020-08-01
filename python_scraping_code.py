
from urllib.request import urlopen
import csv
from bs4 import BeautifulSoup 
import re
import pandas as pd
import time


def datascrapping(links):
    clgids = []
    clgnames = []
    clgaddress = []
    clgemails = []
    clgdistricts = []
    registersnames = []

    for str in links:
        print(str)
        con = urlopen(str)
        data = con.read()
        con.close()
        soup = BeautifulSoup(data, "html.parser")
        id = soup.find('span', attrs={"id": 'ctl00_ContentPlaceHolder1_lblInstituteCode'})
        # print("college id is :" + id.text)
        clgids.append(id.text)
        name = soup.find('span', attrs={"id": 'ctl00_ContentPlaceHolder1_lblInstituteNameEnglish'})
        # print("college name is:" + name.text)
        clgnames.append(name.text)
        infotable = soup.find('table', attrs={"class", 'AppFormTable'})
        td = infotable.find_all('td')  # find all elments between <td> element
        address = td[15].text  # 15th <td> element contains address
        # print("Address is: " + address)
        clgaddress.append(address)
        email = soup.find('span', attrs={"id": 'ctl00_ContentPlaceHolder1_lblEMailAddress'})
        # print("Mail id is:" + email.text)
        clgemails.append(email.text)
        dist = soup.find('span', attrs={"id": 'ctl00_ContentPlaceHolder1_lblDistrict'})
        # print("District is : " + dist.text)
        rname = td[61].text  # 61 <td> element contains register name
        # print("Register name is :" + rname)
        registersnames.append(rname)
    return clgids,clgnames,clgaddress,clgemails,clgdistricts,registersnames

def urlscrapping(url):
    ids = []
    names = []
    addresses = []
    emails = []
    districts = []
    rnames = []
    html = urlopen(url)
    soup = BeautifulSoup(html.read(), 'html.parser')
    href = soup.find('table',attrs={"class": 'DataGrid'})
    links = []
    for link in href. find_all('a'):
        if link. get('href') is None:
            continue
        else:
            href ='http://dtemaharashtra.gov.in/'+link. get('href')
            links. append(href)
    print(links)
    ids, names, addresses, emails, districts, rnames = datascrapping(links)
    return ids,names,addresses,emails,districts,rnames
    # print(ids)
    # print(names)
    # print(addresses)
    # print(emails)
    # print(districts)
    # print(rnames)


def main():
    ids = []
    names = []
    addresses = []
    emails = []
    districts = []
    rnames = []
    url="http://dtemaharashtra.gov.in/frmInstituteList.aspx?RegionID=3&RegionName=Mumbai"
    ids,names,addresses,emails,districts,rnames=urlscrapping(url)
    dataFrame = {'College Id': ids, 'College Names': names, 'College Address': addresses, 'Email': emails, 'Districts': districts, 'Register Name': rnames}
    df = pd.DataFrame(dataFrame, columns=['College Id', 'College Names', 'College Address', 'Email', 'Districts', 'Register Name'])
    outpath = r'C:\New folder'
    filename = 'Collegelists' + (time.strftime("%Y-%m-%d-%H-%M-%S") + '.xls')
    export_csv = df.to_csv(outpath + "\\" + filename, encoding='utf-8-sig', index=None, header=True)
    print(time.strftime("%H%M%S"))

if __name__ == '__main__':
    main()
