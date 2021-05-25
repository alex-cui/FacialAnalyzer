import wget
import requests
import os

def getLinesById(fname):
	"""Returns the lines split by '\t' where the first element is the given id"""
	lines = (l.strip().split('\t') for l in open(fname) if not l.startswith('#'))
	ret = [l for l in lines]
	return ret

def main():
	attrs = getLinesById('celeb.txt')
	names = ['Shakira']
	path = '/home/andrew/Desktop/cs179_AlexAndrew/backend/new_celeb/'
	folders = os.scandir(path)
	# for folder in folders:
	# 	names.append(folder.name)
	# print(names)
	for name, id, url, rect, checksum in attrs:
		try:
			if name in names and int(id) > 100:
				print('new_celeb/' + name + '/' + id + '.jpg')
				wget.download(url, 'new_celeb/' + name + '/' + id + '.jpg')
		except:
			print('Error')
			continue

	print(names)
	#
	# for name in names:
	# 	os.mkdir(os.path.join(path, name))

if __name__ == '__main__':
	main()
