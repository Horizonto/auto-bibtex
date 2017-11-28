import urllib.request
from bs4 import BeautifulSoup

fBibRaw = open("ref.bibraw", "r");
fBibOut = open("ref.bib", "w");

def Process(s: str) -> str:
    if s.startswith("MR"):
        fPage = urllib.request.urlopen("https://mathscinet.ams.org/mathscinet/search/publications.html?fmt=bibtex&pg1=MR&s1="+s[2:]);
        bsPage = BeautifulSoup(fPage, 'html.parser');
        fPage.close();
        fBibOut.write(bsPage.pre.string);
    elif s.startswith("arXiv:"):
        fBibQuery = urllib.request.urlopen("http://adsabs.harvard.edu/cgi-bin/bib_query?"+s);
        bsBibQuery = BeautifulSoup(fBibQuery, 'html.parser');
        fBibQuery.close();
        ltagColumns = bsBibQuery.find_all("td");
        lsColumns = [tag.string for tag in ltagColumns if tag.string]
        sBibCode=lsColumns[lsColumns.index("Bibliographic Code:") + 1];
        fBibEntry = urllib.request.urlopen("http://adsabs.harvard.edu/cgi-bin/nph-bib_query?bibcode="+sBibCode+"&data_type=BIBTEX");
        lsBibEntryLines = list(map(lambda b:b.decode('utf-8'), fBibEntry));
        fBibEntry.close();
        fBibOut.write("".join(lsBibEntryLines[4:]));
    else:
        fBibOut.write(s);

for sLine in fBibRaw:
    Process(sLine);

fBibRaw.close();
fBibOut.close();
