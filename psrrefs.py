#!/opt/local/bin/python

import sys

import ads

def create_psrrefs_bibcode(paper):

    """Use the year and author list to generate a psrrefs bibcode"""

    # one author - use first three letters of authors name
    # two authors - use 2 first inits  and 2-digit year
    #three authors - use three first inits plus 2-digit year
    # 4+, use first three inits, "+" and 2-digit year

    n_author = len(paper.author)
    # generate the year string
    year_string = paper.year[2:4]

    if n_author == 1:
        inits_string = paper.author[0][:3].lower()
    
    elif n_author == 2 or n_author == 3:
        inits_string = ""

        for author in paper.author:
            inits_string = "".join([inits_string, author[0].lower()])

    else:
        inits_string = ""
        for author in paper.author[:3]:
            inits_string = "".join([inits_string, author[0].lower()])

        inits_string = "".join([inits_string, "+"])

    
    return "".join([inits_string, year_string])

if __name__ == "__main__":

    #generate a list of years
    #years = range(1950,2015)
    years=[2015]

    f = open("psrrefs.bib.tmp", "w")

    for yr in years:
        # run query
        papers = list(ads.query("pulsar", 
                                database="astronomy", 
                                rows="all", 
                                dates=yr))

        # loop over retrieved papers
        for paper in papers:

            # skip "nonarticles" (bibtex not implemented)
            if "NONARTICLE" in paper.property:
                continue

            # change the bibcode to psrrefs format

            bibcode = create_psrrefs_bibcode(paper)

            paper.bibcode = bibcode

            try:
                f.write(paper.bibtex.encode('utf-8'))
            except TypeError:
                pass
            except UnicodeEncodeError:
                # should figure this out
                pass

        sys.exit()


    f.close()
