from urllib.request import urlretrieve

with open("C:\P\Hackathons\Junction\Server\posts_v2.csv", 'r') as file:
    line = file.readline()
    i, j = 0, 0
    while line:
        if i % 2 == 1:
            split = line.split(",")
            # print("URL: {}".format(split[1]))
            urlretrieve(split[1], "./images/{}.jpg".format(j))
            j += 1
        i += 1
        line = file.readline()
    print("Total count: {}".format(i))

