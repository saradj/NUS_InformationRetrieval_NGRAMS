This is the README file for A0207386Y's submission

== Python Version ==

I'm using Python Version <3.7.6> for
this assignment.

== General Notes about this assignment ==

I have chosen not to use padding for this assignment since after printing the probabilities I saw that the certainty decreased slightly with padding, the probabilities of the language detected were not as strong.
To keep all the counts of the respective 4 grams, I used a map (dictionary) from each language to a list of tuples or 4 characters - the 4 grams extracted from sentences written in that language. I created another map as well, from the language to a total count of 4-grams (including the smoothing count). This was used to keep track of all the total occurrences of 4-grams for the different language.
For building the model, I started by reading in the sentences from the file, and for each sentence extract the label and generate all the possible character 4-grams from the sentence, by using the build in function ngrams in nltk.
For each labeled language I added all the 4-grams corresponding to it and their respective counts, and also added add-one smoothing by adding the non already present 4-gram with a count of 1, every time that it is encountered in a different language.
To calculate the probability I used the log sum probability. Initially, when calculating a normal probability (by multiplying the probabilities of all the grams in the test sentence for each language separately) the highest accuracy I could achieve was around 70% with some preprocessing. After some online research I decided to use the log probability since the probability values tend to be very close to 0, so taking the log allows take into consideration the values more precisely, since since it transforms them into a range [-2000 to 0]. Since the log of a multiplication is just a sum of the individual logarithms, I just calculated the individual probabilities for each ngram, took the log base 10 of it and summed them up for each sentence.
This gave me the best score 100%, so there was no need for preprocessing the text before.
To be able to detect if the language is not one of the 3 target languages, I kept track of the out of vocabulary words I would encounter in the test sentence, and if their frequency was higher than a certain threshold(which I chose by trial and error) this sentence would be labeled as other.

== Files included with this submission ==

build_test_LM.py
ESSAY.txt
README.txt

== Statement of individual work ==

Please put a "x" (without the double quotes) into the bracket of the appropriate statement.

[x] I, A0207386Y, certify that I have followed the CS 3245 Information
Retrieval class guidelines for homework assignments.  In particular, I
expressly vow that I have followed the Facebook rule in discussing
with others in doing the assignment and did not take notes (digital or
printed) from the discussions.  

[ ] I, A0207386Y, did not follow the class rules regarding homework
assignment, because of the following reason:

<Please fill in>

I suggest that I should be graded as follows:

<Please fill in>

== References ==

I used StackOverflow for Python functions references, since I am quite new with Python. 
http://alexbarter.com/statistics/n-gram-log-probability/
The above website guided me into considering taking the logarithm of the probability.

email: e0445488@u.nus.edu
