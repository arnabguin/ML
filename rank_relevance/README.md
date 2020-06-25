
Ranking of dishes in Yelp data set 
----------------------------------

The repo contains a short, relatively simple program to rank a list of dishes from a set of Yelp reviews. 

Steps:

(1) Create a new dataset containing text reviews in JSON format or Download an existing data set (eg. YELP review data set) [let's call it reviews.json]

(2) Populate a file (ex: dishes.txt) with list of dishes that you want to rank that are present in the reviews.

(3) Run the ranker program

eg. python dish_ranking.py --input reviews.json --rank dishes.txt --rank_k 50 --rank_out dishes_ranked.json

usage: yelp_dish_ranking.py [-h] --input INPUT --rank RANK [--rank_k RANK_K]
                            [--rank_sample RANK_SAMPLE]
                            [--rank_max_reviews RANK_MAX_REVIEWS]
                            [--rank_out RANK_OUT]

This program ranks a given set of dishes based their occurence in Yelp reviews

optional arguments:
  -h, --help            show this help message and exit
  --input INPUT         list of reviews in json format
  --rank RANK           input file containing list of dishes to rank
  --rank_k RANK_K       top k dishes
  --rank_sample RANK_SAMPLE
                        limit on number of dishes to consider (test only)
  --rank_max_reviews RANK_MAX_REVIEWS
                        limit on number of relevant reviews to consider (test
                        only)
  --rank_out RANK_OUT   output data frame containing scores of top k ranked
                        dishes

