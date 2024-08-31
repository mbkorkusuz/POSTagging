import pickle
import sklearn_crfsuite
from sklearn_crfsuite.metrics import flat_accuracy_score, flat_precision_score, flat_recall_score, flat_classification_report
from sklearn_crfsuite.metrics import flat_f1_score

def test(test_data):
	print("Testing...")

	y_true = test_data[1]  #labels
	y_pred = classifier.predict(test_data[0])
	
	precision = flat_precision_score(y_true, y_pred,average='micro')
	recall = flat_recall_score(y_true, y_pred,average='micro')
	f1 = flat_f1_score(y_true, y_pred, average = 'micro')
	accuracy = flat_accuracy_score(y_true, y_pred)

	print("Classsification Report: ", flat_classification_report(y_true, y_pred))

	print("Accuracy:",accuracy)
	print("F1-Score:",f1)
	print("Precision:",precision)
	print("Recall:",recall)

	flat_y_true = []
	flat_y_pred = []
	
	for x in y_true:
		for y in x:
			flat_y_true.append(y)
	
	for x in y_pred:
		for y in x:
			flat_y_pred.append(y)		
	
	end_p=["RP", "NFP", "VBP", "NNP", "PRP", "WP"]
	for i in range(0,len(flat_y_true)):
		if flat_y_true[i][-1] == "P" and flat_y_true[i][-1] not in end_p: 
			flat_y_true[i] = "PUNCT"
		if flat_y_pred[i][-1] == "P" and flat_y_pred[i][-1] not in end_p: 
			flat_y_pred[i] = "PUNCT"
			
def creatdict(sentence,index,pos):	#pos=="" <-> featuresofword  else, relative pos (str) is pos
	word = sentence[index]
	wordlow = word.lower()
	articleDeterminers = ['a', 'an', 'the']
	possesiveDeterminers = ['my', 'your', 'his', 'her', 'its', 'our', 'their']
	demDeterminers = ['this', 'that', 'those', 'these']
	dict={
		"wrd"+pos:wordlow,								# the token itself
		"cap"+pos:word[0].isupper(),					# starts with capital?
		"allcap"+pos:word.isupper(),					# is all capitals?
		"caps_inside"+pos:word==wordlow,				# has capitals inside?
		"nums?"+pos:any(i.isdigit() for i in word),		# has digits?

		"endss"+pos:word[len(word)-1] == 's',				# ends with s?
		"endsing"+pos:word[len(word)-3:] == 'ing',		# ends with ing
		"endsly"+pos:word[len(word)-2:] == 'ly',			# ends with ly

		"alldigit?"+pos:all(i.isdigit() for i in word),	# all digits?
		".?"+pos:any(i == '.' for i in word),				# includes .

		"isart"+pos:wordlow in articleDeterminers,
		"ispos"+pos:wordlow in possesiveDeterminers,
		"isdem"+pos:wordlow in demDeterminers,

		"isfirst"+pos:index == 0,
		"islast"+pos:index == len(sentence)-1,

		'prefix-1'+pos:word[0],
		'prefix-2'+pos:word[:2],
		'prefix-3'+pos:word[:3],

		'suffix-1'+pos:word[-1],
		'suffix-2'+pos:word[-2:],
		'suffix-3'+pos:word[-3:]
	}
	return dict

def feature_extractor(sentence, index):
	features = creatdict(sentence, index, "")
	return features

def load(filename):	
	print("Loading classifier...")
	with open(filename, "rb") as f:
		classifier = pickle.load(f)
		return classifier

def tag(sentence):
	#takes a single sentence as a list
	classifier = load("pos_crf.pickle")
	t_features = []
	for j in range(0,len(sentence)):	
		t_features.append(feature_extractor(sentence, j))
		
	ret = classifier.predict([t_features])[0]
	end_p = ["RP", "NFP", "VBP", "NNP", "PRP", "WP"]
	for i in range(0,len(ret)):
		if ret[i][-1] == "P" and ret[i][-1] not in end_p: 
			ret[i] = "PUNCT"

	return ret


if __name__ == "__main__":

	with open('pos_crf_test.data', 'rb') as file:
		test_data = pickle.load(file)
		
	file.close()
	
	classifier = load("pos_crf.pickle")
	test(test_data)
	
	sentence1 = ['Just', 'a', 'little', 'bit', ',', 'no', ',', 'a', 'lot', 'of', 'it', ',', 'I', 'really', ',', 'really', 'gotta', 'quit', '.']
	sentence2 = ["Something's", 'wrong', 'with', 'me', ',', 'my', 'God', ',', 'old', 'habits', 'die', 'hard', '.']
	sentence3 = ['I', 'guess', 'I', 'had', 'to', 'go', 'to', 'that', 'place', 'to', 'get', 'to', 'this', 'one', '.']
	
	print(tag(sentence1))
	print(tag(sentence2))
	print(tag(sentence3))
