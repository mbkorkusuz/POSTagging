# -*- coding: utf-8 -*-
import pickle
import sklearn_crfsuite

def formatdata(formatted_sentences,formatted_labels,file_name):
	file=open(file_name, 'r', encoding='ascii', errors='backslashreplace')
	print("Reading data...")
	text=file.read().splitlines()
	tokens=[]
	labels=[]
	for line in text:
		line=line.split('\t')
		if len(line)==3:
			tokens.append(line[0])
			if line[1]=="PUNCT":
				labels.append(line[0]+"P")
			else:
				labels.append(line[2])	
		else:
			formatted_sentences.append(tokens)
			formatted_labels.append(labels)
			tokens=[]
			labels=[]


def creatdict(sentence,index,pos):	#pos=="" <-> featuresofword  else, relative pos (str) is pos
	word=sentence[index]
	wordlow=word.lower()
	articleDeterminers = ['a', 'an', 'the']
	possesiveDeterminers = ['my', 'your', 'his', 'her', 'its', 'our', 'their']
	demDeterminers = ['this', 'that', 'those', 'these']
	dict={
		"wrd"+pos:wordlow,								# the token itself
		"cap"+pos:word[0].isupper(),					# starts with capital?
		"allcap"+pos:word.isupper(),					# is all capitals?
		"caps_inside"+pos:word==wordlow,				# has capitals inside?
		"nums?"+pos:any(i.isdigit() for i in word),		# has digits?

		"endss"+pos:word[len(word)-1]=='s',				# ends with s?
		"endsing"+pos:word[len(word)-3:]=='ing',		# ends with ing
		"endsly"+pos:word[len(word)-2:]=='ly',			# ends with ly

		"alldigit?"+pos:all(i.isdigit() for i in word),	# all digits?
		".?"+pos:any(i=='.' for i in word),				# includes .

		"isart"+pos:wordlow in articleDeterminers,
		"ispos"+pos:wordlow in possesiveDeterminers,
		"isdem"+pos:wordlow in demDeterminers,

		"isfirst"+pos:index==0,
		"islast"+pos:index==len(sentence)-1,

		'prefix-1'+pos:word[0],
		'prefix-2'+pos:word[:2],
		'prefix-3'+pos:word[:3],

		'suffix-1'+pos:word[-1],
		'suffix-2'+pos:word[-2:],
		'suffix-3'+pos:word[-3:]
	}
	return dict
	

def feature_extractor(sentence,index):
	features=creatdict(sentence,index,"")

	return features

def creatsets(file_name):	
	sentences=[]
	labels=[] 	
	formatdata(sentences,labels,file_name)	
	limit=int(len(sentences))
	sentences=sentences[:limit]
	labels=labels[:limit]

	print("Feature extraction...")
	features=[]		#X_train
	for i in range(0,len(sentences)):
		features.append([])
		for j in range(0,len(sentences[i])):
			features[-1].append(feature_extractor(sentences[i],j))
			
	del sentences[:]
	del sentences

	delimit=int((len(labels)*8)/10)
	test_data=[features[delimit:],labels[delimit:]]
	features=features[:delimit]
	labels=labels[:delimit]
	
	training_data=[features,labels]

	with open('pos_crf_train.data', 'wb') as file:
		pickle.dump(training_data, file)
	file.close()

	with open('pos_crf_test.data', 'wb') as file:
		pickle.dump(test_data, file)
	file.close()
		
	return training_data, test_data	
		
def train(training_data):		
	print("Training...")
	features=training_data[0]
	labels=training_data[1]	
	classifier.fit(features,labels)	

def save(filename):	
	print("Saving classifier.")
	with open(filename, "wb") as f:
		pickle.dump(classifier, f)
	return

if __name__ == "__main__":

	classifier=sklearn_crfsuite.CRF(c1=0.2, c2=0.2, max_iterations=1000)
	training_data, test_data=creatsets("en-ud-train.conllu")
	
	with open('pos_crf_train.data', 'rb') as file:
		training_data=pickle.load(file)
	file.close()
	
	train(training_data)
	save("pos_crf.pickle")
	