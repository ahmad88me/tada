import sys, os
cur = os.path.dirname (__file__)
parent_dir = '/'.join(cur.split('/')[:-1])
#print 'parent'
#print parent_dir
sys.path.append(parent_dir)


