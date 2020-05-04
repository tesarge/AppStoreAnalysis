#!/usr/bin/env python
# coding: utf-8

# # App Profile Recommendations

# The following will be used as a basis to make recommendations for developing applications to be listed on Google Play and the App Store. 
# 
# # Introduction
# 
# As we begin the process, it is worth noting that our in-app revenue comes from advertisement. Therefore, our applications should be made to attract a high number of users. A high number of users means a higher chance that advertisements are engaged.
# 
# That being said, our analysis will focus on free apps in the app stores that follow a similar revenue format. Our goal for this analysis is to help give our developers an idea for apps that garner a high user count.

# ## Data Sources
# 
# The Google Play store has over 2.1 million apps while the Apple App Store carries over 2 million itself. The collection and analysis of this amount of data would prove to be costly and time consuming. Therefore, analysis will be performed and readily available data sets. Sets of data from Google Play and the App Store, on 10,000 and 7,000 apps respectively, will be used to serve as a slice of the pie for our analysis. Documentation for the data sets is provided below.
# 
# Google Play Store: https://www.kaggle.com/lava18/google-play-store-apps
# 
# Apple App Store: https://www.kaggle.com/ramamet4/app-store-apple-data-set-10k-apps

# In[1]:


def explore_data(dataset, start, end, rows_and_columns=False):
    dataset_slice = dataset[start:end]    
    for row in dataset_slice:
        print(row)
        print('\n') # adds a new (empty) line after each row

    if rows_and_columns:
        print('Number of rows:', len(dataset))
        print('Number of columns:', len(dataset[0]))


# In[2]:


file_1 = open('Data/AppleStore.csv', encoding="utf8")
from csv import reader
read_1 = reader(file_1)
apple = list(read_1)

file_2 = open('Data/googleplaystore.csv', encoding="utf8")
from csv import reader
read_2 = reader(file_2)
android = list(read_2)


# After extracting the data we want to see using the code above, we can now browse some of the data that is available to us. Below is a sample from the App Store data.

# In[3]:


explore_data(apple, 1,5)


# And a sample from Google Play

# In[4]:


explore_data(android,1,5)


# Great. So it looks like we have a bevy of information for each individual app at our disposal. The first order of business is to categorize this data that we have and this has already been given to us in the data sets within the column row. Below I have displayed the column headers from both lists.

# In[5]:


print(apple[0])


# In[6]:


print(android[0])


# 
# 

# ## Cleaning the Data
# 
# ### Removing Duplicate Data
# One of the first steps we have is that some of this data will need to be removed from our lists. We will need to find if any rows have data that does not match the other rows data in each respective column. To do that, we can run this:

# In[7]:


for row in android:
    header_length = len(android[0])
    row_length = len(row)
    if row_length != header_length:
        print(row)
        print(android.index(row))


# Here we can see that row 10473 has data inconsitencies and will need to be removed.

# In[8]:


del android[10473]


# In[9]:


print(android[10473])


# So just to double check that the row was deleted from our data, I printed the same row again to make sure that the row below had shifted up to replace our old one. Looks good.

# Now that inconsistent data is cleared, we will need to look for duplicate data.

# In[10]:


duplicate = []
unique = []
for app in android[1:]: #using [1:] to select data after the header
    name = app[0]
    if name in unique:
        duplicate.append(name)
    else:
        unique.append(name)
        
print('Unique apps in android: ', len(unique))
print('Duplicate apps in android: ', len(duplicate))


# We find that roughly 10% of the data in our list is duplicate data. We will want to remove this but we need to decide how to remove the data. To do that, we should look at some duplicates and see what kind of data we want in our final list. Lets find an app that has duplicates. A popular and well-known app like Instagram might be a good place to look.

# In[11]:


for app in android:
    name = app[0]
    if name == 'Instagram':
        print(app)


# The data differentiates at the 4th column. To save you time from scrolling back up, the 4th column is the 'Reviews' column. The differentiation is likely from data being taken at different times. We will want the most recent data and that will likely be the row with the most reviews.
# 
# To do this I'll write a code that will make a new list that stores the apps each only once, cycles through each row in the original list and checks the number of reviews stored in the new list and updates to the highest value if necessary.

# In[12]:


reviews_max = {}
for app in android[1:]:
    name = app[0]
    n_reviews = float(app[3])
    if name in reviews_max and reviews_max[name] < n_reviews:
        reviews_max[name] = n_reviews
    elif name not in reviews_max:
        reviews_max[name] = n_reviews
        


# To ensure that we have the same number of apps as the unique apps list from above:

# In[13]:


print(len(reviews_max))


# Right now this data is just stored in a dictionary that attributes an app name to the number of reviews. Now we need to make a list that contains all the app data using only the apps we just singled out above.

# In[14]:


android_clean = []
already_added = []
for app in android[1:]:
    name = app[0]
    n_reviews = float(app[3])
    if n_reviews == reviews_max[name] and name not in already_added:
        android_clean.append(app)
        already_added.append(name)
        


# In[15]:


explore_data(android_clean, 1,4)


# In[16]:


print(len(android_clean))


# ### Filtering Out Non English Apps
# Alright, so the data in the list is looking like how we want it and has been cleaned of duplicate entries. But we still need to clean up some more. Being a company that makes apps in English, it would be best if we also narrowed our focus to look at only the apps in English. We do this because apps that our popular in one country might not be as popular or even nonexistent in another country, like Facebook in China or Ali Pay in the US. Sorry, iQiyi, we'll have to take you out of our data.
# 
# To do this we need to write some code that will look at the name of the app, determine if it is English or another language, and remove the non-English apps. We can use ASCII to recognize characters that are English or other languages based on their associated number. Characters we use in English fall between 0-127 in the ASCII. We can check each character in the app name to see if its ASCII number is 127 or less. We should also consider other characters such as emojis or trademark logos that sometimes appear in app names. We can give apps a threshold for the number of non-English characters they cinlude before we consider it a non_english app. Below I've set it to three.

# In[17]:


def eng_check(string):
    non_eng = 0
    for char in string:
        if ord(char) > 127:
            non_eng += 1
            
    if non_eng > 3:
        return False
    else:
        return True


# In[18]:


eng_check('爱奇艺PPS -《欢乐颂2》电视剧热播')


# In[19]:


eng_check('Instagram')


# In[20]:


eng_check('Instachat 😜')


# Looks like this has worked and we can start making a list that includes only English apps. 

# In[21]:


android_en_clean = []
def lang_filter(data):
    for app in data:
        name = app[0]
        if eng_check(name) :
            android_en_clean.append(app)


# In[22]:


lang_filter(android_clean)


# In[23]:


len(android_en_clean)


# ### Cleaning The Apple App Store Data
# 
# Now I'll run the Apple App Store data through the same process, making minor changes to the code for relevancy.

# In[24]:


for row in apple:
    header_length = len(apple[0])
    row_length = len(row)
    if row_length != header_length:
        print(row)
        print(apple.index(row))


# In[25]:


duplicate_apple = []
unique_apple = []
for app in apple[1:]: #using [1:] to select data after the header
    name = app[1]
    if name in unique_apple:
        duplicate_apple.append(name)
    else:
        unique_apple.append(name)
        
print('Unique apps in apple: ', len(unique_apple))
print('Duplicate apps in apple: ', len(duplicate_apple))


# In[26]:


reviews_max_apple = {}
for app in apple[1:]:
    name = app[1]
    n_reviews_apple = float(app[5])
    if name in reviews_max_apple and reviews_max_apple[name] < n_reviews_apple:
        reviews_max_apple[name] = n_reviews_apple
    elif name not in reviews_max_apple:
        reviews_max_apple[name] = n_reviews_apple


# In[27]:


print(len(reviews_max_apple))


# In[28]:


apple_clean = []
apple_already_added = []
for app in apple[1:]:
    name = app[1]
    n_reviews = float(app[5])
    if n_reviews == reviews_max_apple[name] and name not in apple_already_added:
        apple_clean.append(app)
        apple_already_added.append(name)


# In[29]:


print(len(apple_clean))


# In[30]:


apple_en_clean = []
def lang_filter_apple(data):
    for app in data:
        name = app[1]
        if eng_check(name) :
            apple_en_clean.append(app)


# In[31]:


lang_filter_apple(apple_clean)


# In[32]:


print(len(apple_en_clean))


# The App Store raw data looks like it's a bit cleaner than the Google Play store data and we didn't have to do much. However, I went ahead and did it for the sake of consistency.

# ### Filtering Out Paid Apps
# 
# Since we plan on app revenue coming solely from in-app advertisement, we should only look at data regarding similar apps. Therefore, we want to filter out data on paid apps, as the revenue schemes are different that what we plan to implement. 
# 
# The App Store data displays price in a numbers-only string, such as '3.99', making it easy to convert to a float. However, the Google Play Store data shows price using a dollar sign and that doesn't allow us to convert it to a float. The good news is that the data contains a column titled "Type" which says whether the app is free or paid. To filter out the paid apps, we only need to search this "type" column

# In[33]:


apple_free = []
for app in apple_en_clean[1:]:
    price = float(app[4])
    if price == 0.0:
        apple_free.append(app)


# In[34]:


print(len(apple_free))


# In[35]:


android_free = []
for app in android_en_clean[1:]:
    price = app[6]
    if price == "Free":
        android_free.append(app)


# In[36]:


print(len(android_free))


# # Analysis

# Since we are making an app with an in-app advertisement based revenue scheme, our app revenue will be highly influenced by the number of users. This is one of the reasons we needed to filter out the paid apps. Paid apps, while also benefitting from a high volume of users, can rely on user payments in a variety of ways such as upfront app cost, a monthly subscription fee, or in-app upgrades, to name a few. In this way, paid apps can make decent revenue with fewer users than a free app. Our goal of having a high user count means that we should plan on launching the app on both the Google Play store and The App Store.
# 
# To ensure that our strategy can be profitable, we will roll out the app in three steps:
# 
# 1. First, we will build a basic Android version of the app and launch on the Google Play Store.
# 
# 2. If our initial response from users is positive, we will further develop the app based on user reviews.
# 
# 3. Pending a profitible first six months on Google Play, we will build an iOS version of the app to release on the Apple App Store.
# 
# 

# To find a starting point for our app development, we will analyze the apps in the data sets by genre. In the App Store this is under the 'prime_genre' column, and in the Google Play store under 'Genres' and 'Category'. TO do this we will make some functions to 
#     1. Generate a frequency table that shows percentage, and
#     2. Display the percentages in descending order

# In[37]:


def freq_table(dataset, index):
    table = {}
    total = 0
    
    for row in dataset:
        total += 1
        value = row[index]
        if value in table:
            table[value] += 1
        else:
            table[value] = 1
            
    table_percent = {}
    for key in table:
        percentage = (table[key]/total) * 100
        table_percent[key] = percentage
        
    return table_percent

def display_table(dataset, index):
    table = freq_table(dataset, index)
    table_display = []
    for key in table:
        key_val_as_tuple = (table[key], key)
        table_display.append(key_val_as_tuple)

    table_sorted = sorted(table_display, reverse = True)
    for entry in table_sorted:
        print(entry[1], ':', entry[0])


# ### Most Popular Google Play Apps by Genre

# In[38]:


display_table(android_free, 9)


# In[39]:


display_table(android_free, 1)


# ### Most Popular App Store Apps by Genre

# In[40]:


display_table(apple_free, 11)


# As we can see in the frequency table of the App Store data, the 'Games' genre dominates the free apps market with a 58% share. The next closet is 'Entertainment' with almost 8% share. Looking further down we notice that of the top ten genres by percentage, over 80% of apps are for entertainment purposes such as music, games, and sports. Making an app in an entertainment genre might be a good start to our app.
# 
# 'Games' has over 58% of the market for free aps but that doesn't necessarily mean that it is the best genre for us to make an app. 'Social Networking' only has just over 3% but we know that Facebook, Instagram, and other free social media apps have billions of users. 

# The Google Play data does not have a stand out genre like 'Games' in the App Store. In both the 'Category' and 'Genres', the top apps are a mix of entertainment and productivity apps. Unfortunately, when considering both the App Store and Google Play, analyzing the most popular genres is insufficient by itself to make a recommendation. We will need to go deeper and find out which genre has the most users per app.

# To analyze genres by number of users, we will have to use two different metrics for the App Store and Google Play. In Google Play, we can use the 'Installs' column to determine how many people have installed the app. Unfortunately, the App Store data does not have such a column, so we will have to look at the number of ratings with the 'rating_count_tot' column.
# 
# For 'ratings_count_tot', we can isolate the apps in each genre, sum up their ratings numbers, then divide the sum by the number of apps in the genre.

# ### The App Store Genre Frequency

# In[41]:


apple_genre = freq_table(apple_free, -5)

for genre in apple_genre:
    total = 0
    len_genre = 0
    for app in apple_free:
        genre_app = app[-5]
        if genre_app == genre:
            num_ratings = float(app[5])
            total += num_ratings
            len_genre += 1
    avg_num_ratings = total / len_genre
    print (genre, ':', avg_num_ratings)



# Based off the results the top three most used app genres in descending order are Navigation, Reference, and Music. Let's take a closer clook at what kinds of apps we would be competing with if we were to make an app in one of these genres.

# In[42]:


for app in apple_free:
    if app[-5] == 'Navigation':
        print(app[1], ':', app[5])


# Clearly the Navigation app market is anchored down by two apps comprising over half a million ratings together, Waze and Google Maps. Having two apps such as these makes it difficult for a new app to enter the market and as such, we would be better to look elsewhere.

# In[43]:


for app in apple_free:
    if app[-5] == 'Reference':
        print(app[1], ':', app[5])


# The 'Reference' genre seems much more open than 'Navigation'. Here there are no single apps that clearly control the market. Yes, the Bible app has nearly 1 million ratings however if we look at the other apps within the genre, it's hard to see that these apps would necessarily be in competition with each other. In other words, 'Bible' and 'City Maps for Minecraft' likely have no competition with each other.

# In[44]:


for app in apple_free:
    if app[-5] == 'Music':
        print(app[1], ':', app[5])


# Much like 'Reference', the 'Music' genre has a few apps at the top with around a million ratings and then a wide open field of apps covering various aspets of music. Looking at some of the names we can determine that there are a handful of music streaming services outside the top three including 'Tidal', 'Amazon Music' and 'iHeartRadio'. We also see some device specific apps like 'Bose Connect' which connects mobile devices to Bose speaker devices. Additionally, there are a few apps for learning instruments such as piano and guitar basics.
# 
# Ok, so let's do the same for the Google Play store.

# ### Google Play Genre Frequency

# Google and Apple store app data differently so where as the App Store has a unique count for the 'ratings_count_tot' column, the Google Play store has data stored for number of downloads. However, this data is a little vague.

# In[45]:


display_table(android_free, 5)


# Here the Google Play store documents app installs in brackets but these brackets are very defined. Fortunately, this shouldn't be too much of an issue for the purposes of our initial analysis on free apps. Before we can look at the numbers, we will need to remove the strings, or the '+' and ',' from our list.

# In[57]:


android_category = freq_table(android_free, 1)

for category in android_category:
    total = 0
    len_category = 0
    for app in android_free:
        category_app = app[1]
        if category_app == category:
            n_installs = app[5]
            n_installs = n_installs.replace('+','')
            n_installs = n_installs.replace(',','')
            total += float(n_installs)
            len_category += 1
    android_avg_installs = total / len_category
    print(category, ' : ', android_avg_installs)


# So what we can do with this data is take our analysis of the App Store data and try to determine how these two data sets overlap. To do that, I will open up some of these categories to figure out what types of apps are in them, as the category names are a bit different from the App Store.
# 
# Since the Reference genre in the App Store seemed promising, I will look in the 'BOOKS_AND_REFERENCE' category first.

# In[58]:


for app in android_free:
    if app[1] == 'BOOKS_AND_REFERENCE':
        print(app[0], ':', app[5])


# This category is similar to the App STore version in that it seems like a pretty open field for apps. There appear to be quite a number of book based apps including reference apps to books as well as e-book readers and game guides. This category also includes a few dictionaries between and English and other languages but we can discount these as our app will only be in English. 
# 
# This data is good, but let's take a look at some of the others before making a final recommendation

# In[60]:


for app in android_free:
    if app[1] == 'EDUCATION':
        print(app[0], ':', app[5])


# 'EDUCATION' is an interesting category because there are so many apps with over 1 million installs. This could be promising since we will rely on user count for revenue. More interestingly is that there is a high number of apps related to learning English, all likely with some competitive overlap, yet many of these apps have over 1 million installs. This has me thinking that we should look at the App Store data in the 'Education' genre.

# In[61]:


for app in apple_free:
    if app[-5] == 'Education':
        print(app[1], ':', app[5])


# Initially when I looked through the App Store data, I looked through the categories that had higher average ratings. AFter seeing the Google Play 'EDUCATION' category, it seemed like this might be a good genre for us to explore and despite having a lower average review count, the App Store data I feel supports this as well. If we comb through the App Store 'Education' genre we can see at the bottom that there are a handful of apps with less than 1000 reviews, but nearly all of them are aimed at babies and small children. At the top we have apps geared more for adult learners, and they have some outstanding review counts. 
# 
# Take into consideration how long a baby or small child will use an app. Eventually they will grow out of it and the app will no longer be used. Some of these apps, specifically those aimed for babies, have a very short shelf life on a users phone. When the child grows up, the app will be deleted. 
# 
# Yet, when we look at the adult learning apps, we have to consider what users are doing with these apps. It is likely that they will use it for quite some time. Duolingo, for instance, is a popular language learning app that encourages users to maintain daily streaks for app use. Some users have logged thousands of days using that app. This kind of app is being downloaded onto phones to be kept for a very long time. 

# ## Analytical Outcome
# 
# After going over the data in these app stores, I think our company should be looking to make an application that falls somewhere in between Education and Books/Reference. These genres are very wide and seem to be supported by a high number of loyal users. Even with similar apps in the same category, many apps in education enjoy a high user base. 
# 
# We want an app that will be used by many and for an extended period of time. The more often our app is on screens, the more likely users will follow up on an advertisement.
# 
# My application recommendation for our company:
# 
#     1. I suggest that we build an app that has a goal of helping users 
#     improve their English skills.
#     2. To achieve this goal, we can offer an e-reader type application  
#     where users can read stories at their English level
#         -The text will have clickable words with a definition
#         should the user not know the word.
#         -The app will have the ability to save a word into a flashcard bank
#         for further study
#     3. Stories can be categorized based on English exams that users are
#     studying for (e.g. contains words  and grammar found on the 
#     IELTS, TOEFL, SAT, etc)

# # Conclusion
# 
# In this project we analyzed data in Google Play and The App Store to make a recommendation to our company for an application design.
# 
# The recommendation is an e-reader style application that is aimed at adult learners of English. The Book and Education genres are popular on both app stores and support a high number of users while also maintaing a level of parity that would allow success for new entrants into the genres. 

# In[ ]:




