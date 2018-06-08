import feedparser
import collections
import re
from Helpers.Logging import *
PrintedOnce = False
def getwords(html):
  text = re.compile(r'<[^>]+>').sub('', html)
  words = re.compile(r'[^A-z^a-z]+').split(text)
  words_list = [word.lower() for word in words if word]
  global PrintedOnce
  if not PrintedOnce:
    Info("Length of Total words in the HTML :{}".format(len(words_list)))
    Info(words_list[:5])
    PrintedOnce = True
  return words_list


def getwordcounts(url):
  Info("Parsing Url: {}".format(url))
  d = feedparser.parse(url)

  #print d
  wc = collections.defaultdict(int)

  Info("Number of Entries in Parsed URL : {}".format(len(d)))
  for e in d.entries:
    if 'summary' in e:
      summary = e.summary
    else:
      summary = e.description

    words = getwords('%s %s' % (e.title, summary))
    for word in words:
      wc[word] += 1



  if 'title' not in d.feed:
    print 'Invalid url', url
    return 'bogus data', wc
  try:
    Info("Title of the Feed :{}".format(d.feed.title))
  except:
    pass
  return d.feed.title, wc


def main():

  # XXX: break this up into smaller funtions, write tests for them
  Info("Generating feed Vector..")
  apcount = collections.defaultdict(int)
  wordcounts = {}
  feedlist = open('feedlist.txt').readlines()

  for url in feedlist[:25]:
    Info("Url :{}".format(url))
    title, wc = getwordcounts(url)
    wordcounts[title] = wc
    for word, count in wc.iteritems():
      if count > 1:
        apcount[word] += 1

  Info("Appropriate Words Count : {}".format(len(apcount)))

  wordlist = []
  for w, bc in apcount.iteritems():
    frac = float(bc)/len(feedlist)
    if 0.1 < frac < 0.5:
      wordlist.append(w)
  Info("Length of Words to be written in BlogData {}".format(len(wordlist)))
  out = file('blogdata.txt', 'w')
  out.write('Blog')
  try:
    for w in wordlist:
      out.write('\t' + w)
    out.write('\n')
    for blogname, counts in wordcounts.iteritems():
      out.write(blogname)
      for w in wordlist:
        if w in counts: out.write('\t%d' % counts[w])
        else: out.write('\t0')
      out.write('\n')
  except:
    Error("SOme While writing to BlogData")

if __name__ == '__main__':
  main()
