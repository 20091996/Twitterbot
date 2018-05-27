import tweepy, re, operator
from paralleldots import set_api_key
from paralleldots import sentiment

# Authentication Consumer Key
CONSUMER_KEY = "PBAlehVfXAWJDY2VkJaGvYCUz"
CONSUMER_SECRET = "6CkkHEd9TGYyBmirhXqMw3Neu4gulZFSzFoiU3Dzw73NQpiJTQ"

# Authentication Access Tokens
ACCESS_TOKEN = "4089293293-lFJOzGUvvFiRe6OZXyFsY71dgKmqkSw56XXvbXq"
ACCESS_TOKEN_SECRET = "hZJEtvImZSt4uTepnJMZkbQmIMISghTFpAeBEVeH33GTF"


oauth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
oauth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

api = tweepy.API(oauth)

def GetSearch():
    hash = input("Type the word u want to search without #")
    hash = "#" + hash
    print(hash)
    tweets = api.search(hash)
    return tweets


def SentAnalysis():
    lists = []
    tweets = GetSearch()
    set_api_key("5Ilq8t88HXC0EYjVzpCDqqnQSlPJm5mJ9faJTnigwG4")
    for tweet in tweets:
        lists.append(sentiment(tweet.text))
    return lists


def tweet_match():
    trump = 0
    tweets = api.user_timeline(screen_name="@realdonaldtrump", count=200, tweet_mode="extended")
    for tweet in tweets:
        tweet_text = re.sub(r"http\S+", "", tweet.full_text)   # Removing the URL texts
        if "India" in tweet_text or "INDIA" in tweet_text or "india" in tweet_text:
            trump += 1

    modi = 0
    listx = []
    tweets = api.user_timeline(screen_name="@narendramodi", count=200, tweet_mode="extended")
    for tweet in tweets:
        listx.append(tweet.full_text)
    for x in listx:
        if "US" in x or "USA" in x or "America" in x  or "america" in x:
            modi += 1
    # showing the comparison
    print("MOdi-"+ str(modi))
    print("Trump-"+ str(trump))



def top_usage():
    import nltk
    from nltk.corpus import stopwords
    nltk.download('stopwords')
    stop_words = set(stopwords.words('english'))

    dictt = {}
    tweet_words = []
    tweet = api.user_timeline(screen_name="narendramodi", count=200, tweet_mode="extended")
    for x in tweet:
        y = x.full_text.split(" ")
        for z in y:
            tweet_words.append(z)
    for word in tweet_words:
        if word not in stop_words and "http" not in word:
            if word in dictt.keys():
                dictt[word] += 1
            else:
                dictt[word] = 1

    sorted_dict = sorted(dictt.items(), key=operator.itemgetter(1))
    print("The Top Ten Words Are: ")
    for i in range(-1, -11, -1):
        print(sorted_dict[i][0], " - ", sorted_dict[i][1])


def determine_location():
    language = {}
    location = {}
    time = {}
    tag_hash = input("Enter the word without #: ")
    tag_hash='#'+ tag_hash
    print(tag_hash)
    tweets = api.search(q=tag_hash, count=200)
    for tweet in tweets:
        if tweet.user.lang in language.keys():
            language[tweet.user.lang] += 1
        else:
            language[tweet.user.lang] = 1
        #for location
        if tweet.user.location in location.keys():
            location[tweet.user.location] += 1
        elif tweet.user.location != '':
            location[tweet.user.location] = 1
        #for time zones
        if tweet.user.time_zone in time.keys():
            time[str(tweet.user.time_zone)] += 1
        else:
            time[str(tweet.user.time_zone)] = 1

    Location = sorted(location, key=location.get, reverse=True)
    Time = sorted(time, key=time.get, reverse=True)
    Language = sorted(language, key=language.get, reverse=True)

    print("Locations for this keyword are:")
    i = 0
    for j in Location[0:5]:
        i += 1
        print(i, j, location[j])

    print("Timezones for this keyword:")
    i = 0
    for j in Time[0:5]:
        i += 1
        print(i, j, time[j])
    i = 0
    print("Top 5 languages used:")
    for j in Language[0:5]:
        i += 1
        print(i, j, language[j])

def menu():
    show_menu = True
    menu_choices = "\nEnter From The Corrosponding options:   \n1.Extraction of tweets on a topic:\n2.Count the no. of followers on a tweet\n3.Do a sentiment analysis on tweets  \n4.Determine Time Language, And Location \n5.Comparison Of Tweets\n6.Top Words in Usage\n7.Tweet A Message\n8.Exit"
    while show_menu:
        choice = input(menu_choices)  # getting the user choice

        # For tweets Retrieval
        if choice == "1":
            tweets = GetSearch()   # getting the tweets from the other function
            print("Following tweets have been made by the people \n")
            for tweet in tweets:
                print(tweet.text)

        # Count Followers
        elif choice == "2":
            tweets = GetSearch()
            for tweet in tweets:
                print("User : %s \t Followers:%s " % (tweet.user.name, tweet.user.followers_count))
            print("\n")

        # Determine The Sentiments
        elif choice == "3":
            lists = SentAnalysis()
            p = 0
            n = 0
            nu = 0
            for x in lists:
                if x["sentiment"] == "neutral":
                    nu += 1
                elif x["sentiment"] == "negative":
                    n += 1
                elif x["sentiment"] == "positive":
                    p += 1
            print("Sentiment Result:\nWait for a minute(max 2 min xD)")
            print("Positive:%d \t Negative:%d \t Neutral:%d" % (p, n, nu))

        # Determine the location
        elif choice == "4":
            determine_location()

        # Comparison of tweets
        elif choice == "5":
            tweet_match()

        # Top Usage
        elif choice == "6":
            top_usage()

        # Tweet A Message
        elif choice == "7":
            status = input("Enter The Status update:")
            api.update_status(status)

        # Exit
        elif choice == "8":
            show_menu = False
menu()
