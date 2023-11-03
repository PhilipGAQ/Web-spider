import json
from collections import defaultdict
import math
from Compress_For import compress,depress


def create_skip_pointers(threshold, docs,skip_list,skip_index):
    if len(docs) > threshold:
        skip_interval = int(math.sqrt(len(docs)))
        skip_list = [docs[i:i+skip_interval][-1] for i in range(0, len(docs), skip_interval)]
        skip_index = [i+skip_interval-1 for i in range(0, len(docs), skip_interval)]
        return skip_list, skip_index
    else:
        return [], []

# Load the JSON file
with open('TagsForMovies_Philip.json', 'r',encoding="utf-8") as f:
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
print(inverted_index)

# Set the threshold for skip pointers
threshold = 10

# Create a dictionary to store the skip pointers
skip_pointers_index={}
skip_pointers = {}
k=8

# Loop through each tag and its document list in the inverted index
for tag, docs in inverted_index.items():
    # If the document list is longer than the threshold, create skip pointers
    if len(docs) > threshold:
        # Calculate the skip interval
        skip_interval = int(math.sqrt(len(docs)))
        # Create a list of skip pointers
        skip_list = [docs[i:i+skip_interval][-1] for i in range(0, len(docs), skip_interval)]
        skip_index = [i+skip_interval-1 for i in range(0, len(docs), skip_interval)]
        # Add the skip pointers to the dictionary
        skip_pointers[tag] = skip_list
        skip_pointers_index[tag]=skip_index

'''Compressed_inverted_index={}
Compressed_inverted_index=compress(inverted_index,k)'''
# Print the inverted index and skip pointers
'''print("Inverted Index:")
print(inverted_index)
print('\n')
print("Skip Pointers:")
print(skip_pointers)
print('\n')
print("Skip_Index:")
print(skip_pointers_index)
print('\n')'''

def infix_to_postfix(query):
    # Define operator precedence
    precedence = {'(':4,')':4,'NOT': 3, 'AND': 2, 'OR': 1}

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
    #print(' '.join(output))
    return ' '.join(output)

def bool_and(res1,res2,index1,index2):
    results = []
    cnt1=cnt2=0
    #print("res1", res1)
    #print("res2",res2)
    #print("index1",index1)
    #print("index2",index2)
    if len(index1)==0 or len(index2)==0:
        while cnt1<len(res1) and cnt2<len(res2):
            if res1[cnt1]==res2[cnt2]:
                results.append(res1[cnt1])
                cnt1+=1
                cnt2+=1
            elif res1[cnt1]<res2[cnt2]: 
                cnt1+=1
            else:
                cnt2+=1
    else:
        gap1=int(index1[1])-int(index1[0])
        gap2=int(index2[1])-int(index2[0])
        while cnt1<len(res1) and cnt2<len(res2):
            if res1[cnt1]==res2[cnt2]:
                results.append(res1[cnt1])
                cnt1+=1
                cnt2+=1
            elif res1[cnt1]<res2[cnt2]:
                if cnt1 not in index1 or cnt1+gap1>=len(res1):
                    cnt1+=1
                else:
                    if res1[cnt1+gap1]<=res2[cnt2]:
                        cnt1+=gap1
                        continue
                    else :
                        cnt1+=1
                        continue
            else:
                if cnt2 not in index2 or cnt2+gap2>=len(res2):
                    cnt2+=1
                else:
                    if res2[cnt2+gap2]<=res1[cnt1]:
                        cnt2+=gap2
                        continue
                    else :
                        cnt2+=1
                        continue
    '''print("results:")
    print(results)
    print('\n')'''
    return results


#def bool_search(query):
    # Split the query into individual terms
    terms = query.split()
    print(terms)
    result_and=[]
    result_and_pointers=[]
    result_and_index=[]

    if len(terms) == 1:
        results = set(inverted_index.get(terms[0], []))
        #results = depress(Compressed_inverted_index,terms[0],k)
        return sorted(results)
    else:
        cnt=0
        res1 = set(inverted_index.get(terms[cnt], []))
        #print(res1)
        if terms[cnt+1]=="NOT":
            results = set(range(1, 1201))-res1
            result_and=list(results)
            result_and_pointers,result_and_index=create_skip_pointers(10,result_and,result_and_pointers,result_and_index)
            cnt+=2
        else:
            res2 = set(inverted_index.get(terms[cnt+1], []))
            #print(res2)
            if terms[cnt+2]=="AND":
                result_and = bool_and(inverted_index.get(terms[cnt],[]),inverted_index.get(terms[cnt+1],[]),skip_pointers_index.get(terms[cnt],[]),skip_pointers_index.get(terms[cnt+1],[]))
                #print(result_and)
                result_and_pointers,result_and_index=create_skip_pointers(10,result_and,result_and_pointers,result_and_index)
                results=set(result_and)
            elif terms[cnt+2]=="OR":
                results = res1 | res2
                result_and=list(results)
                result_and_pointers,result_and_index=create_skip_pointers(10,result_and,result_and_pointers,result_and_index)
            else :
                print("Invalid query")
                return []
            cnt+=3
        while cnt<len(terms):
            if terms[cnt]=="NOT":
                results = set(range(1, 1201))-results
                result_and=list(results)
                result_and_pointers,result_and_index=create_skip_pointers(10,result_and,result_and_pointers,result_and_index)
                cnt+=1
            else:
                res = set(inverted_index.get(terms[cnt], []))
                if terms[cnt+1]=="AND":
                    result_and = bool_and(inverted_index.get(terms[cnt],[]),result_and,skip_pointers_index.get(terms[cnt],[]),result_and_index)
                    result_and_pointers,result_and_index=create_skip_pointers(10,result_and,result_and_pointers,result_and_index)
                    results=set(result_and)
                    cnt+=2
                elif terms[cnt+1]=="OR":
                    results = results | res
                    result_and=list(results)
                    result_and_pointers,result_and_index=create_skip_pointers(10,result_and,result_and_pointers,result_and_index)
                    cnt+=2
                else :
                    res2=set(inverted_index.get(terms[cnt+1], []))
                    if terms[cnt+1]=="AND":
                        result_and = bool_and(inverted_index.get(terms[cnt],[]),result_and,skip_pointers_index.get(terms[cnt],[]),result_and_index)
                        result_and_pointers,result_and_index=create_skip_pointers(10,result_and,result_and_pointers,result_and_index)
                        results=set(result_and)
                        cnt+=2
                    elif terms[cnt+1]=="OR":
                        res = res1 | res2
                        result_and=list(results)
                        result_and_pointers,result_and_index=create_skip_pointers(10,result_and,result_and_pointers,result_and_index)
                        cnt+=2
                    print("Invalid query")
                    return []
                cnt+=2
    return sorted(results)


def bool_search(tokens):

    stack = []
    stack_index=[]
    tokens=tokens.split()
    print(tokens)
    result_and=[]
    result_and_pointers=[]
    result_and_index=[]

    for token in tokens:
        if token == 'AND':
            b=stack.pop()
            if type(b) is not set:
                b_pointers_index=skip_pointers_index.get(b,[])
                b = inverted_index.get(b,[])[:]
            else :
                b_pointers_index=stack_index.pop()
            a=stack.pop()
            if type(a) is not set:
                a_pointers_index=skip_pointers_index.get(a,[])
                a = inverted_index.get(a,[])[:]
            else :
                a_pointers_index=stack_index.pop()
            result_and = bool_and(sorted(list(a)),sorted(list(b)),a_pointers_index,b_pointers_index)
            stack.append(set(result_and))
            result_and_pointers,result_and_index=create_skip_pointers(10,sorted(list(result_and)),result_and_pointers,result_and_index)
            stack_index.append(result_and_index)
        elif token == 'OR':
            b=stack.pop()
            if type(b) is not set:
                b = set(inverted_index.get(b,[])[:])
            a=stack.pop()
            if type(a) is not set:
                a = set(inverted_index.get(a,[])[:])
            result = a | b
            result_and_pointers,result_and_index=create_skip_pointers(10,sorted(list(result)),result_and_pointers,result_and_index)
            stack.append(result)
            stack_index.append(result_and_index)
        elif token == 'NOT':
            a=stack.pop()
            if type(a) is not set:
                a = set(inverted_index.get(a,[])[:])
            result = set(range(1, 1201))-a
            result_and_pointers,result_and_index=create_skip_pointers(10,sorted(list(result)),result_and_pointers,result_and_index)
            stack.append(result)
            stack_index.append(result_and_index)
        else:
            stack.append(token)

    if len(stack) == 1:
        return stack[0]

final_result=sorted(bool_search(infix_to_postfix(input())))
print(final_result)
# Load data from JSON file
with open('Movies_Philip.json', 'r',encoding='utf-8') as f:
    data = json.load(f)

# Print corresponding data for each index in final_result
for index in final_result:
    print(data[index])
    print('\n')

