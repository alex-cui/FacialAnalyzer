import wget
import requests

def getLinesById(id, fname):
	"""Returns the lines split by '\t' where the first element is the given id"""
	lines = (l.strip().split('\t') for l in open(fname) if not l.startswith('#'))
	ret = [l for l in lines if int(l[0]) == int(id)]
	return ret

for id in range(10000, 15000):
    attrs = getLinesById(id, 'facelabels.txt')
    for fid, attr, label in attrs:
        try:
            if attr == 'age':
                print(fid, attr, label)
                urls = getLinesById(fid, 'faceindex.txt')[0]
                imgurl, pageurl = urls[1:]
                print('Image URL:', imgurl)
                wget.download(imgurl, 'data/'+ label + '/' + fid + '.jpg')
        except Exception as e:
            print('Something went wrong:', e)
