import json
from collections import defaultdict
import math

# Load the JSON file
with open('TagsForBooks_Philip.json', 'r',encoding="utf-8") as f:
    data = json.load(f)

# Create a dictionary to store the inverted index
inverted_index = defaultdict(list)

# Loop through each document and its tags
for i, doc in enumerate(data):
    for tag in doc['tags']:
        # Add the document number to the inverted index for the current tag
        inverted_index[tag].append(i)

# Sort the inverted index by tag
inverted_index = dict(sorted(inverted_index.items()))

# Set the threshold for skip pointers
threshold = 10

# Create a dictionary to store the skip pointers
skip_pointers = {}

# Loop through each tag and its document list in the inverted index
for tag, docs in inverted_index.items():
    # If the document list is longer than the threshold, create skip pointers
    if len(docs) > threshold:
        # Calculate the skip interval
        skip_interval = int(math.sqrt(len(docs)))
        # Create a list of skip pointers
        skip_list = [docs[i:i+skip_interval][-1] for i in range(0, len(docs), skip_interval)]
        # Add the skip pointers to the dictionary
        skip_pointers[tag] = skip_list


# Print the inverted index and skip pointers
'''print("Inverted Index:")
print(inverted_index)
print('\n')
print("Skip Pointers:")
print(skip_pointers)
print('\n')'''

def infix_to_postfix(query):
    # Define operator precedence
    precedence = {'NOT': 3, 'AND': 2, 'OR': 1}

    # Split the query into individual terms and operators
    tokens = query.split()
    stack = []
    output = []

    for token in tokens:
        if token in ['AND', 'OR', 'NOT']:
            # Pop operators from the stack and add them to the output until
            # we find an operator with lower precedence or the stack is empty
            while stack and stack[-1] != '(' and precedence[token] <= precedence.get(stack[-1], 0):
                output.append(stack.pop())
            stack.append(token)
        elif token == '(':
            stack.append(token)
        elif token == ')':
            # Pop operators from the stack and add them to the output until
            # we find a left parenthesis or the stack is empty
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            if stack and stack[-1] == '(':
                stack.pop()
            else:
                raise ValueError("Mismatched parentheses")
        else:
            # Add terms to the output
            output.append(token)

    # Pop any remaining operators from the stack and add them to the output
    while stack:
        if stack[-1] == '(':
            raise ValueError("Mismatched parentheses")
        output.append(stack.pop())
        

    # Join the output listinto a single string and return it
    print(' '.join(output))
    return ' '.join(output)

def bool_search(query):
    # Split the query into individual terms
    terms = query.split()
    print(terms)

    if len(terms) == 1:
        results = set(inverted_index.get(terms[0], []))
        return sorted(results)
    else:
        cnt=0
        res1 = set(inverted_index.get(terms[cnt], []))
        if terms[cnt+1]=="NOT":
            results = set(range(1, 1001))-res1
            cnt+=2
        else:
            res2 = set(inverted_index.get(terms[cnt+1], []))
            if terms[cnt+2]=="AND":
                results = res1 & res2
            elif terms[cnt+2]=="OR":
                results = res1 | res2
            else :
                print("Invalid query")
                return []
            cnt+=3
        while cnt<len(terms):
            if terms[cnt]=="NOT":
                results = set(range(1, 1001))-results
                cnt+=1
            else:
                res = set(inverted_index.get(terms[cnt], []))
                if terms[cnt+1]=="AND":
                    results = results & res
                elif terms[cnt+1]=="OR":
                    results = results | res
                else :
                    print("Invalid query")
                    return []
                cnt+=2
    return sorted(results)

print(bool_search(infix_to_postfix(input())))