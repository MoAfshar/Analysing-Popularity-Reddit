import pandas as pd 
import csv
from tqdm import tqdm

def createEdgePath():
	sub = pd.read_csv("submissions.csv")

	edge_list = []
	for i in range(1, len(sub)):
    	if(sub.loc[i, 'imageNum'] == sub.loc[i-1, 'imageNum']): 
    		edge_list.append(tuple((sub.loc[i-1, 'id'], sub.loc[i, 'id'])))

	print(len(edge_list))
	with open('edge_list.csv','w', newline='') as out:
    	csv_out = csv.writer(out)
    	csv_out.writerow(['source','destination'])
    	for row in edge_list:
        	csv_out.writerow(row)

#Use if needed
def filterNodes(): 
	sub = pd.read_csv("filteredSub.csv")
	newFile = sub[sub["Count_of_reddit_id"] > 3]
	ids = list(newFile['id'])
	newSub = pd.read_csv("submissions.csv")
	j = []
	for i in tqdm(range(0, len(newSub))): 
 		if(newSub.get_value(i, 'id') not in ids): 
 			print(newSub.get_value(i, 'id'))
 			j.append(newSub[newSub.id == newSub.get_value(i, 'id')].index)
 			#newSub = newSub.drop(newSub[newSub.id == newSub.loc[i, 'id']].index.tolist())

	print(j)
	for i in tqdm(range(len(j))):
		newSub = newSub.drop(j[i])

	header = ["id", "unixtime", "rawtime", "title,", "total_votes" ,"reddit_id", "number_of_upvotes", "Subreddit", "number_of_downvotes", "localtime", "score", "number_of_comments", "imageNum"]
	newSub.to_csv('outputFinal.csv', columns = header, index = False)