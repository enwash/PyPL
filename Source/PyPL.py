"""
PyPL 1.0

This is a program built to prove a set of
premises and a conclusion provided in PL
by the user.
Mostly to help with my homework.
But that's beside the point.

Currently supported rules:
    Modus Ponens
    Modus Tollens
"""

DONE_SOLVING = False

class PLExp():
    """
    PLExp: Class used for input premises.
    PLExpObject.infer(sentence) will return what can be inferred
    
    For instance, if the object is derived from "Ax>Bx", then
    running infer("Ax") will return a new PLExp derived from "Bx".
    """
    def __init__(self,sentence):
        """
        The sentence input is based on the following:
        - No spaces
        - No characters except A-Z, (), ~, &, and >
        - Actual PL sentence, duh
        """
        # Set the sentence
        self.sentence = sentence
        # Initialize the inference storage
        self.inferences = {}
        # Read the sentence and conver it to a set of inferences
        self.read_sentence()

    def addInference(self,s1,s2,rule):
        """
        Adds an inference with input s1 and
        output 2 to the inferences dictionary
        """
        # I mean it literally just adds an inference
        self.inferences[s1]=[s2,rule]
    
    def read_sentence(self):
        """
        Reads self.sentence and converts it to
        inferences for use with .infer()
        
        The inferencs are added to a dictionary,
        self.inferences, where the key is a
        possible input of .infer() and the value
        is the inference
        """
        s = self.sentence
        # Modus Ponens + Modus Tollens
        if '>' in s:
            if ')' in s:
                s1 = s[:s.index('>')]
                s2 = s[s.index('>')+1:]
                self.addInference('~'+s2,'~'+s1,'MT')
                if s1[0] == '(' and s1[-1] == ')':
                    s1 = s1[1:-1]
                if s2[0] == '(' and s2[-1] == ')':
                    s2 = s2[1:-1]
                self.addInference(s1,s2,'MP')
            else:
                s1 = s[:s.index('>')]
                s2 = s[s.index('>')+1:]
                self.addInference('~'+s2,'~'+s1,'MT')
                self.addInference(s1,s2,'MP')
                
    def infer(self,inp):
        """
        Returns and prints an inference from
        the input, inp (PLExp), and the sentence
        the object was initialized from.

        If inp is not provided, deaults to
        a "wild card" (for instance, A & B)
        """
        # Do the thing
        try:
            return self.inferences[inp]
        # Return false if there are no inferences for the given input
        except KeyError:
            return False

premises = []
num = 1
inp = False
while not inp:
    try:
        num = int(input('\nNumber of premises:\n> '))
        inp = True
    except:
        print('Invalid input! Integers only.')
for i in range(num):
    premises.append(input('Premise ' + str(i+1) +' (no spaces): \n> '))
conclusion = input('Conclusion:\n> ')

inferences = {}
for i in range(len(premises)):
    premises[i] = PLExp(premises[i])
    
def print_premises():
    """
    Print the premises
    """
    for i in range(len(premises)):
        print('\n' + str(i+1) + '. ' + premises[i].sentence, end='')
    print(' / ' + conclusion)

def check_done():
    """
    Check if an inference proves the
    original conclusion
    """
    for key in inferences:
        if key == conclusion:
            return True
    return False

def infer_from_premise(index):
    """
    Brute-force a given premise to see
    if any of the other premises
    can infer anything from it
    """
    for i in range(len(premises)):
        if i == index:
            pass
        inf = premises[index].infer(premises[i].sentence)
        if not inf == False:
            inferences[inf[0]] = inf[1]
            if check_done():
                return True
    for i in list(inferences):
        inf = premises[index].infer(i)
        if not inf == False:
            inferences[inf[0]] = inf[1]
            if check_done():
                return True
    return False

def infer_from_inference(inference):
    for i in range(len(premises)):
        inf = PLExp(inference).infer(premises[i].sentence)
        if not inf == False:
            inferences[inf[0]] = inf[1]
            if check_done():
                return True
    for i in range(len(inferences)):
        inf = PLExp(inference).infer(premises[i].sentence)
        if not inf == False:
            inferences[inf[0]] = inf[1]
            if check_done():
                return True
    return False

def print_all():
    """
    Print premises and inferences
    """
    print_premises()
    i = len(premises)
    for key, val in inferences.items():
        i += 1
        print(str(i) + '. ' + key + ' (' + val + ')')

def solve():
    """
    Infers everything possible
    """
    ret = False
    for i in range(len(premises)):
        if infer_from_premise(i):
            ret = True
    for i in list(inferences):
        if infer_from_inference(i):
            ret = True
    print_all()
    return ret

if not solve():
    print('\nUnsupported input')
