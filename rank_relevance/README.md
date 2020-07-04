
Ranking of dishes/restaurants
-----------------------------

The repo contains a short, relatively simple program to 
* get top K dishes from a set of Yelp reviews based on popularity
* get top K restaurants for an user preference of dishes ( we call the preference a "diner's list" that may contain 1 single dish name or a collection of dishes preferably from a single cuisine (italian,indian etc)) 

Usage
-----

usage: ranker.py [-h] [--rank RANK]
                      [--rank_kd RANK_KD] 
                      [--rank_kr RANK_KR]
                      [--rank_sample_dish_count RANK_SAMPLE_DISH_COUNT]              (( test mode ))
                      [--rank_sample_restaurant_count RANK_SAMPLE_RESTAURANT_COUNT]  (( test mode ))
                      [--rank_max_reviews RANK_MAX_REVIEWS]                          (( test mode ))
                      [--rank_restaurants_input RANK_RESTAURANTS_INPUT]
                      [--rank_reviews_input RANK_REVIEWS_INPUT]
                      [--rank_dishes_output RANK_DISHES_OUTPUT]
                      [--rank_restaurants_output RANK_RESTAURANTS_OUTPUT]
  --rank RANK           file containing list of dishes
  --rank_kd RANK_KD     top k ranked dishes
  --rank_kr RANK_KR     top k ranked restaurants
  --rank_sample_dish_count RANK_SAMPLE_DISH_COUNT
                        max number of dishes to consider in dish list
  --rank_sample_restaurant_count RANK_SAMPLE_RESTAURANT_COUNT
                        max number of restaurants to scan
  --rank_max_reviews RANK_MAX_REVIEWS
                        max reviews to scan
  --rank_restaurants_input RANK_RESTAURANTS_INPUT
                        input json file containing info about businesses
  --rank_reviews_input RANK_REVIEWS_INPUT
                        input json file containing restaurant reviews
  --rank_dishes_output RANK_DISHES_OUTPUT
                        output file containing scores of top k ranked dishes
  --rank_restaurants_output RANK_RESTAURANTS_OUTPUT
                        output file containing scores of top k ranked
                        restaurants
Top K dishes
------------

(1) Create a new dataset containing text reviews in JSON format or Download an existing data set (eg. YELP review data set) [let's call it reviews.json]

(2) Create a file (ex: dishes.txt) with list of dishes to be ranked

(3) Run the ranker program (assuming K=50)

eg. python ranker.py --rank_reviews_input reviews.json --rank dishes.txt --rank_kd 50 --rank_dishes_output dishes_ranked.json

(4) Data frame for top K dishes will be output to dish_ranked.json

Top K restaurants
-----------------

(1) Create a new dataset containing text reviews in JSON format or Download an existing data set (eg. YELP review data set) [let's call it reviews.json]
(2) Create a new dataset containing information about restaurants mentioned in the reviews or Download an existing data set (eg. YELP business data set) [let's call it business.json]

(2) Create a file (ex: diner.txt) containing 1 or more dishes [diner's preference]

(3) Run the ranker program (assuming K=30)

eg. python ranker.py --rank diner.txt --rank_kr 30 --rank_restaurants_input business.json --rank_reviews_input reviews.json

(4) Data frame for top K restaurants will be output to restaurant_ranked.json

