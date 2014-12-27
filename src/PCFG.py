from nltk import Tree
import numpy as np
from CodeWarrior.Standard_Suite import document
class PCFG():
    def __init__(self):
        self.document=set()
        self.build_grammar()
        self.build_lexicon()
    def build_grammar(self):
        self.grammar={
                      ('S','NP','VP'):0.8,
                      ('S','S','PP'):0.001,
                      ('S','Pronoun','VP'):0.2,
                      ('NP','Det','N'):0.30,
                      ('VP','VP','PP'):0.40,
                      ('VP','V','NP'):0.20,
                      ('VP','V','VP'):0.20,
                      ('PP','Preposition','NP'):1.0
                      }
    def build_lexicon(self):
        self.lexicon={
                      ('Det','the'):0.40,
                      ('Det', 'a'):0.40,
                      ('N','meal'):0.01,
                      ('N', 'car'):0.02,
                      ('N','book'):0.02,
                      ('N','robort'):0.01,
                      ('N', 'internet'):0.02,
                      ('V','buy'): 0.05,
                      ('V','want'):0.05,
                      ('V','read'):0.05,
                      ('V','book'):0.05,
                      ('V','say'): 0.05,
                      ('V','put'): 0.05,
                      ('V','includes'): 0.05,
                      ('Preposition','with'): 0.05,
                      ('Preposition','on'): 0.05,
                      ('Preposition','to'): 0.05,
                      ('Preposition','about'): 0.05,
                      ('Pronoun','I'):0.40
                      
                      }
    def read_documents(self,path):
        with open(path) as document_input:
            for line in document_input:
                self.document.add(tuple(line.split()))
                
    def pcfg(self,document):
        table={}
        back={}
        for j in range(1,len(document)+1):
            for lex_rule,probability in self.lexicon.items():
                if lex_rule[1]==document[j-1]:
                    table[(j-1,j,lex_rule[0])]=probability
                  
            for i in range(j-2,-1,-1):
                for k in range(i+1,j):
                    for grammer_rule,probability in self.grammar.items():
                        if (i,k,grammer_rule[1]) in table and (k,j,grammer_rule[2]) in table:
                            parse_prob=probability*table[i,k,grammer_rule[1]]*table[k,j,grammer_rule[2]]
                            if (i,j,grammer_rule[0]) not in table or parse_prob>table[(i,j,grammer_rule[0])]:
                                table[(i,j,grammer_rule[0])]=parse_prob
                                back[i,j,grammer_rule[0]]=(k,grammer_rule[1],grammer_rule[2])
        return table,back
    
    
    def build_tree(self,back,text,start,end,root):
        if (start,end,root) in back:
            compressed_subtree=back[(start,end,root)]
        else:
            word=text[start:end]
            return word
        split_spot=compressed_subtree[0]
        left_root=compressed_subtree[1]
        right_root=compressed_subtree[2]
        left_subtree=self.build_tree(back,text,start,split_spot,left_root)
        right_subtree=self.build_tree(back,text,split_spot,end,right_root) 
        return Tree(root,[left_subtree,right_subtree])
         
    
if __name__=='__main__':
    pcfg=PCFG()
    pcfg.read_documents('./document')
    for line in pcfg.document:
        table,back=pcfg.pcfg(line)
        print 'probability = '+str(table[(0,len(line),'S')])
        pcfg.build_tree(back,line,0,len(line),'S').draw()




