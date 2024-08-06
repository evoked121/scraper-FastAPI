location_url = ""
#注意变量的格式
location1 = "Bellevue, Washington, United States of America"
location2 = "Los Angeles, California, United States of America"
people1 = "1,2,3"
room = "3"
start = "2024-04-17"
end = "2024-04-20"

url = 'https://www.expedia.com/Hotel-Search?adults={parent}&allowPreAppliedFilters=true&children=&d1={start}&d2={end}&destination={location}&endDate={end}&rooms={room}&semdtl=&sort=RECOMMENDED&startDate={start}&theme=&useRewards=true&userIntent='
destination = 'Bellevue%2C%20Washington%2C%20United%20States%20of%20America'
l1 = location1.split(",")
l11 = location2.split(",")
people = people1.split(",")



def getDesUrl(location_list):
    des_url = ""
    total_length = len(location_list)
    for i in range(total_length):
        lst = location_list[i].split(" ")
        lst = lst[1:] if lst[0]=="" else lst
        length = len(lst)
        des = ""
        for j in range(length):
            if j==length-1 and i==total_length-1:
                des += lst[j]
            elif j==length-1:
                des += lst[j]+"%2C%20"
            else:
                des += lst[j]+"%20"
        des_url += des
    return des_url

def getAdult(people):
    res = ""
    length = len(people)
    for i in range(length):
        if i==length-1:
            res += people[i]
        else:
            res += people[i]+"%2C"
    return res

location = getDesUrl(l11)
parent = getAdult(people)
print(url.format(location=location, parent=parent, start=start, end=end, room=room))
