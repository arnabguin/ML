import argparse
import json
import math
import sys
from collections import defaultdict

from textblob import TextBlob

reload(sys)
sys.setdefaultencoding('utf8')

def rank(input, dishlist, topk, sample, output_file, maxreviews):

    path2reviews = args.input
    M = 0 # total number of reviews

    scores = {}     # map containing final scores per dish
    reviews = []    # list containing all reviews parsed from dataset (limited to 'maxreviews' in test mode)
    dishes = []     # list containing all dishes parsed from dish list (limited to 'sample' in test mode)
    reviews_map = defaultdict(list) # map containing list of review indices per dish
    reviews_sentiment = []          # list containing sentiment polarity of each review (we ignore the subjectivity score for this algorithm)


    ## Populate list of dishes
    with open(dishlist, 'r') as d:
        for i, dish in enumerate(d.readlines()):
            dish = dish.encode('utf-8').rstrip()
            dishes.append(dish)
            # Bail if max dishes is reached
            if sample != None and i == sample - 1: break

    print "Total number of dishes : {}".format(len(dishes))

    ## Populate list of reviews,construct review map per dish and compute sentiments of reviews
    with open(path2reviews, 'r') as f:
        for i, line in enumerate(f.readlines()):
            M = M + 1
            review_json = json.loads(line.encode('utf-8'))
            review = review_json['text']

            nmatch = 0
            ## Construct review map per dish
            for dish in dishes:
                if dish in review:
                    reviews_map[dish].append(i)
                    nmatch = nmatch + 1
            print "Number of matching dishes for review {}: {}".format(i, nmatch)

            ## Populate list of reviews
            reviews.append(review)

            ## Compute sentiment of reviews
            review_blob = TextBlob(review)
            reviews_sentiment.append(float(review_blob.sentiment[0]))

            # Bail if max reviews is reached
            if maxreviews != None and i == maxreviews - 1: break

    print "Cached {} reviews in memory".format(str(M))

    for i, dish in enumerate(dishes):
        print ("Analyzing dish \"{}\" in reviews".format(dish))
        dish_score = 0
        relevant_doc_count = 0

        for review_index in reviews_map[dish]:
            review = reviews[review_index]
            relevant_doc_count = relevant_doc_count + 1
            dish_score += reviews_sentiment[review_index]

            if relevant_doc_count % 500 == 0:
                print "Accumulated dish score for \"{}\" : {} per 100 relevant reviews".format(
                dish, dish_score)

        scores[dish] = {'idf': relevant_doc_count, 'tf': dish_score,
                        'score': 0 if relevant_doc_count == 0 else dish_score * math.log(
                            float(M + 1) / float(relevant_doc_count))}

        print "Dish score: {}".format(scores[dish])
        print "Total number of reviews parsed: {}".format(M)
        # Bail if number of max number of dishes reached
        if sample != None and i == sample - 1: break

    print ("Total reviews: {}. Top k = {} dishes based on scoring function.".format(M, int(topk)))

    ## Sort by score to get topk dishes
    scores_sorted = sorted(scores.items(), key=lambda t: t[1]['score'], reverse=True)[:topk]

    ## Create data frame of scores for visualization
    scores_df = defaultdict(list)
    for rec in scores_sorted:
        scores_df['dish'].append(rec[0].encode('utf-8'))     # Dish name
        scores_df['tf'].append(rec[1]['tf'])                 # Term frequency
        scores_df['ndocs'].append(rec[1]['idf'])             # Relevant docs
        scores_df['score'].append(rec[1]['score'])           # Final score = f(tf,idf,sentiment)

    with open(output_file, 'w') as of:
        of.write(str(dict(scores_df)))
    print "Scores written to {}".format(output_file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='This program ranks a given set of dishes based their occurence in Yelp reviews')

    parser.add_argument('--input', type=str, required=True,
                        help="list of reviews in json format")
    parser.add_argument('--rank',  type=str, required=True,
                        help='input file containing list of dishes to rank')
    parser.add_argument('--rank_k', default=5, type=int,
                        help='top k dishes')
    parser.add_argument('--rank_sample', default=None, type=int,
                        help='limit on number of dishes to consider (test only)')
    parser.add_argument('--rank_max_reviews', default=None, type=int,
                        help='limit on number of relevant reviews to consider (test only)')
    parser.add_argument('--rank_out', default='dish_ranking.json', type=str,
                        help='output data frame containing scores of top k ranked dishes')

    args = parser.parse_args()
    if args.rank:
        print "Ranking dishes."
        rank(args.input, args.rank, args.rank_k, args.rank_sample, args.rank_out, args.rank_max_reviews)
