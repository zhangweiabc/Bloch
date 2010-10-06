from sys import stderr
from optparse import OptionParser

from Bloch import load, save

parser = OptionParser(usage="""%prog <input file> <tolerance> <output file> [<tolerance> <output file>]+

Example:

  %prog counties.shp 500 counties-simple.shp 5000 counties-simpler.shp

That is all.""")

if __name__ == '__main__':
    opts, args = parser.parse_args()
    
    infile, outargs = args[0], args[1:]
    outfiles = [(int(outargs[i]), outargs[i + 1]) for i in range(0, len(outargs), 2)]
    
    print >> stderr, 'Loading data...'
    datasource = load(infile)
    
    print >> stderr, len(datasource._indexes()), 'shapes,',
    print >> stderr, datasource.db.execute('SELECT COUNT(DISTINCT line_id) FROM segments').fetchone()[0], 'lines,',
    print >> stderr, datasource.db.execute('SELECT COUNT(DISTINCT guid) FROM segments').fetchone()[0], 'segments.'
    
    for (tolerance, outfile) in sorted(outfiles):
    
        print >> stderr, 'Simplifying linework to %d...' % tolerance
        datasource.simplify(tolerance)
        
        print >> stderr, 'Building %s...' % outfile
        save(datasource, outfile)
