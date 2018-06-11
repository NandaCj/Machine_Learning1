import collections
import math
import operator
import re
from Helpers.Logging import *
from sqlite3 import dbapi2 as sqlite


def getwords(doc):
  Info("Getting Words..")
  splitter = re.compile(r'\W*')
  words = [s.lower() for s in splitter.split(doc) if 2 < len(s) < 20]
  Info("Words in the Doc... \n {}".format(set(words)))
  return set(words)


class classifier(object):

  def __init__(self, getfeatures, filename=None):
    Info("Classifier .. Getfeature {}".format(getfeatures))
    # Counts of ofeature/category combinations
    self.fc = collections.defaultdict(lambda: collections.defaultdict(int))

    # Counts of documents in each category
    self.cc = collections.defaultdict(int)
    self.getfeatures = getfeatures

  def setdb(self, dbfile):
    self.con = sqlite.connect(dbfile)
    self.con.execute('create table if not exists fc(feature, category, count)')
    self.con.execute('create table if not exists cc(category, count)')

  # Dict-based methods
  # (XXX: The methods should delegate to a Store object, which could then be
  # a dict- or db-based class. But this is for fun only, so...)

  #def incf(self, f, cat):
    #self.fc[f][cat] += 1

  #def incc(self, cat):
    #self.cc[cat] += 1

  #def fcount(self, f, cat):
    #if f in self.fc and cat in self.fc[f]:
      #return float(self.fc[f][cat])
    #return 0.0

  #def catcount(self, cat):
    #if cat in self.cc:
      #return float(self.cc[cat])
    #return 0.0

  #def totalcount(self):
    #return sum(self.cc.values())

  #def categories(self):
    #return self.cc.keys()

    # Increase the count of a feature/category pair
  def incf(self, f, cat):
    # Info("Increasing the count of the feature...")
    self.fc.setdefault(f, {})
    self.fc[f].setdefault(cat, 0)
    self.fc[f][cat] += 1
    # Info("Count of Feature per category: {}".format(self.fc))

  # Increase the count of a category
  def incc(self, cat):
    # Info("Increasing the Count of Category...")
    self.cc.setdefault(cat, 0)
    self.cc[cat] += 1
    # Info("Count of total number of time category called {}".format(self.cc))

  # The number of times a feature has appeared in a category
  def fcount(self, f, cat):
    if f in self.fc and cat in self.fc[f]:
      return float(self.fc[f][cat])
    return 0.0


  # The number of items in a category
  def catcount(self, cat):
    if cat in self.cc:
      return float(self.cc[cat])
    return 0

  def totalcount(self):
    res = self.con.execute('select sum(count) from cc').fetchone()
    if not res: return 0.0
    return float(res[0])

  def categories(self):
    cur = self.con.execute('select category from cc')
    return [d[0] for d in cur]

  def train(self, item, cat):
    Info("\n Item :{} \n Categtory :{}".format(item, cat))
    features = self.getfeatures(item)
    for f in features:
      self.incf(f, cat)
    self.incc(cat)

  def cprob(self, cat):
    """Returns P(cat)."""
    if self.totalcount() == 0: return 0.0
    return self.catcount(cat) / self.totalcount()

  def fprob(self, f, cat):
    """Returns P(f | cat), i.e. chance that a document in category cat contains
    the given feature."""
    if self.catcount(cat) == 0: return 0.0

    return self.fcount(f, cat)/self.catcount(cat)

  def weightedprob(self, f, cat, prf, weight=1.0, ap=0.5):
    """Returns guess for P(f | cat). The guess starts near `ap` if only few
    data is known."""
    basicprob = prf(f, cat)

    # Count how often this feature has occurred in any category
    totals = sum([self.fcount(f, c) for c in self.categories()])

    weightedp = ((weight*ap) + (totals*basicprob))/(weight + totals)
    return weightedp


class naivebayes(classifier):

  def __init__(self, getfeatures):
    classifier.__init__(self, getfeatures)  # XXX: use super()?
    self.thresholds = collections.defaultdict(lambda: 1.0)

  def setthreshold(self, cat, t):
    self.thresholds[cat] = t

  def getthreshold(self, cat):
    return self.thresholds[cat]


  def classify(self, doc, default=None):
    probs = {}

    # Find category with highest "probability"
    max = 0.0
    for cat in self.categories():
      probs[cat] = self.prob(cat, doc)
      if probs[cat] > max:
        max = probs[cat]
        best = cat

    # make sure the classifier is sure about what it's saying
    for cat in probs:
      if cat == best: continue
      if probs[cat]*self.getthreshold(best) > probs[best]: return default
    return best

  def docprob(self, doc, cat):
    """Returns P(doc | cat), assuming all words in doc are independent (which
    is not true, hence this does not really return a probability. The result is
    still useful, though)."""
    features = self.getfeatures(doc)
    probs = [self.weightedprob(f, cat, self.fprob) for f in features]
    return reduce(operator.mul, probs, 1.0)

  def prob(self, cat, doc):
    """Returns P(cat | doc), with the same caveats as listed for docprob().
    Also omits the division by P(doc), which would be required by Bayes's
    Theorem -- we don't care about that term."""
    # XXX: work out (on paper) what this does in terms of catcount etc
    return self.docprob(doc, cat) * self.cprob(cat)


class fisherclassifier(classifier):

  def __init__(self, getfeatures):
    classifier.__init__(self, getfeatures)  # XXX: use super()?
    self.minimums = collections.defaultdict(int)

  def setminimum(self, cat, min):
    self.minimums[cat] = min

  def getminimum(self, cat):
    return self.minimums[cat]

  def cprob(self, f, cat):
    """As far as I understand, this returns P(cat | f), but with a fancy method
    to avoid normalization issues?"""
    clf = self.fprob(f, cat)
    if clf == 0: return 0.0  # else testOneCategory() fails
    freqsum = sum([self.fprob(f, c) for c in self.categories()])
    p = clf/freqsum
    return p

  def fisherprob(self, doc, cat):
    features = self.getfeatures(doc)
    # XXX: If cprob returns P(cat | f), why can I use it with weightedprob?
    probs = [self.weightedprob(f, cat, self.cprob) for f in features]
    p = reduce(operator.mul, probs, 1.0)

    fscore = -2*math.log(p)
    return self.invchi2(fscore, len(features)*2)

  def invchi2(self, chi, df):
    m = chi / 2.0
    sum = term = math.exp(-m)
    for i in range(1, df // 2):
      term *= m / i
      sum += term
    return min(sum, 1.0)

  def classify(self, item, default=None):
    best = default
    max = 0.0
    for c in self.categories():
      p = self.fisherprob(item, c)
      if p > self.getminimum(c) and p > max:
        best = c;
        max = p
    return best


def sampletrain(cl):
  Info("Training Sample ...")
  cl.train('Nobody owns the water.', 'good')
  cl.train('the quick rabbit jumps fences', 'good')
  cl.train('buy pharmaceuticals now', 'bad')
  cl.train('make quick money at the online casino', 'bad')
  cl.train('the quick brown fox jumps', 'good')


if __name__ == '__main__':
  cl = classifier(getwords)
  sampletrain(cl)
  print("Classification \t Count \t \n")
  for Classification, ClassificationCount in cl.cc.items():
    print(" {} \t {}".format(Classification, ClassificationCount))


  print ("Word \t Count ")
  for Word, Count in cl.fc.items():
    print("{} \t {}".format(Word, Count))

  word = 'quick'
  classification =  'good'
  print("Probablity of \"{}\" in the \"{}\" classification ".format(word, classification))
  print ("Count of \"{}\" in \"{}\" --> \"{}\"".format(word, classification, cl.fcount(word, classification)))
  print ("Total Count of classification \"{}\" -->  {}".format(classification, cl.catcount(classification)))
  print(cl.fprob(word, classification))
  # print cl.fcount('quick', 'good')
  # print cl.fcount('quick', 'bad')
