#!/usr/bin/env python
# coding: utf-8
import spacy

nlp = spacy.load('en_core_web_sm')

#---------------------------1---------------------------

#recursive function that, given a token and the root of a sentence, returns the path of relations of a token.
def get_head(dep, token, root):
    if token.text != root.text:
        dep.append(token)
        get_head(dep, token.head, root)
    else:
        dep.append(token.head)
    return dep

#function that, given a sentence, extracts the paths of dependecy relations starting from the ROOT until it reaches each token.
def extract_path(sent):
    doc = nlp(sent)
    dep = []
    root = doc[:].root
    for token in doc:
        res = get_head([], token, root)
        res.reverse()
        dep.append([token.text, res])
    return dep

#---------------------------2---------------------------

#function that, given a sentence, returns a subtree of dependants for each token.
def extract_deptree(sent):
    doc = nlp(sent)
    res = []
    for token in doc:
        res.append([token, list(sub.text for sub in token.subtree)])
    return res

#---------------------------3---------------------------

#function that, given a sentence and a list of tokens, finds if that segment is a valid subtree of the sentence.
def check_valid_subtree(test, sent):
    subtrees = extract_deptree(sent)
    check = False
    for sub in subtrees:
        if len(test) == len(sub[1]):
            if all(t in sub[1] for t in test):
                check = True
    return check

#---------------------------4---------------------------

#function that, given a sentence and a starting and ending points, it returns the head of the span created from the sentence
#and the two points provided.
def spanhead(sent, start, end):
    doc = nlp(sent)
    span = doc[start:end]
    return span, span.root

#---------------------------5---------------------------

#function that, given a sentence, extracts the span of subject, direct and indirect object of that sentence.
def extract_sdi(sent):
    doc = nlp(sent)
    root = doc[:].root
    res = {
        'subject': [],
        'direct object': [],
        'indirect object': []
    }
    for token in doc:
        if token.dep_ == 'nsubj' or token.dep_ == 'nsubjpass' or token.dep_ == 'csubj' or token.dep_ == 'csubjpass' or token.dep_ == 'expl':
            subs = [sub for sub in token.subtree]
            res['subject'].append(doc[subs[0].i:subs[-1].i+1])
        elif token.dep_ == 'dobj':
            subs = [sub for sub in token.subtree]
            res['direct object'].append(doc[subs[0].i:subs[-1].i+1])
        elif token.dep_ == 'dative':
            subs = [sub for sub in token.subtree]
            res['indirect object'].append(doc[subs[0].i:subs[-1].i+1])
    return res



sent = "I saw the man on a hill with a telescope."
print('-----------------------ASSIGNMENT #1-----------------------')
print('1) Extract a path of dependency relations from the ROOT to a token\n')
deps = extract_path(sent)
for dep in deps:
    print('\t',dep[0],'', ' -> ', [d.dep_ for d in dep[1]])
print('\n2) Extract subtree of a dependents given a token\n')
subtrees = extract_deptree(sent)
for tree in subtrees:
    print('\t',tree[0],' -> ',tree[1])
print('\n3) Check if a given list of tokens (segment of a sentence) forms a subtree\n')
print('\tList: ["hill", "on"]',' -> ',check_valid_subtree(['hill', 'on'],sent))
print('\tList: ["a", "telescope", "with"]',' -> ',check_valid_subtree(['a', 'telescope', 'with'],sent))
print('\n4) Identify head of a span, given its tokens\n')
span, head = spanhead(sent, 2, 5)
print(f'\tThe head of the span "{span}" is "{head}"')
print('\n5) Extract sentence subject, direct object and indirect object spans\n')
res = extract_sdi(sent)
for key,item in res.items():
    print('\t',key,': ',item if item else None)
