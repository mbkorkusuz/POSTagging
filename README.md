# POS Tagging
## **Introduction**
This repository contains the implementation of well known part of speech (POS) tagging algorithm in NLP.

## **Installation**
* Make sure you had installed the requiring libraries in your system.

* Clone repository to your local machine.
 ````text
git clone https://github.com/mbkorkusuz/POSTagging.git
````
* Navigate to the project directory in the terminal.

Run the `train.py` script to train the classifier with the dataset.

 ````text
python3 train.py
````

When training is done run the `test.py` script for testing the classifier

For benchmark results, run:
````text
python3 test.py
````

Also if one wants to tag any sentence to its parts, can run `tag()` function.


## **Metrics**

- Accuracy: 0.9268431810619385

- F1-Score: 0.9268431810619385

- Precision: 0.9268431810619385

- Recall: 0.9268431810619385

## **Example Sentences**
<div class="header">
  <h1>
    S1
  </h1>
</div>

- Just a little bit, no, a lot of it, I really, really gotta quit.

````text
['RB' 'DT' 'JJ' 'NN' 'PUNCT' 'UH' 'PUNCT' 'DT' 'NN' 'IN' 'PUNCT' 'PUNCT' 'PUNCT' 'RB' 'PUNCT' 'RB' 'JJ' 'NN' 'PUNCT']
````


<div class="header">
  <h1>
    S2
  </h1>
</div>

- Something's wrong with me, my God, old habits die hard.

````text
['RB' 'JJ' 'IN' 'PUNCT' 'PUNCT' 'PRP$' 'PUNCT' 'PUNCT' 'JJ' 'NNS' 'PUNCT' 'RB' 'PUNCT']
````



<div class="header">
  <h1>
    S3
  </h1>
</div>

- I guess I had to go to that place to get to this one.

````text
['PUNCT' 'PUNCT' 'PUNCT' 'VBD' 'TO' 'VB' 'IN' 'DT' 'NN' 'TO' 'VB' 'IN' 'DT' 'NN' 'PUNCT']
````



