'''
Created on Aug 19, 2014

@author: j19li
'''
import wco_lex
from ply.lex import lex, LexToken
import io
class WCOParser:
    def __init__(self):
        self._lex=lex(wco_lex)
    def parse(self,cfg_file):
        cfg=io.open(cfg_file)
        cfg_str=cfg.read()
        cfg.close()
        self._lex.input(cfg_str)
        tokens=list(self._lex)
        stack=[]
        for t in tokens:
            if(t.type in ['NAME','LPAREN','STRING']):
                stack.append(t)
            elif(t.type=='RPAREN'):
                l2=[]
                while(len(stack)>0 and ((not isinstance(stack[-1], LexToken)) or stack[-1].type!='LPAREN')):
                    pt=stack.pop()
                    l2.append(pt)
                if(stack[-1].type!='LPAREN'):
                    raise Exception('unmatched PAREN lineno:%s'%t.lineno)
                stack.pop()
                if(len(l2)==2):
                    if((not isinstance(l2[1], LexToken)) or l2[1].type!='NAME'):
                        raise Exception('expect not %s but NAME,lineno:%s,l2:%s'%(l2[1],t.lineno,l2))
                    if(isinstance(l2[0],LexToken) and l2[0].type!='STRING'):
                        raise Exception('syntax error,lineno:%s,l2:%s'%(l2[0].lineno,l2))
                    stack.append((l2[1].value,l2[0].value if isinstance(l2[0], LexToken) else l2[0]))
                else:
                    raise Exception('syntax error,lineno:'%t.lineno)
        return dict(stack)
                    
                    