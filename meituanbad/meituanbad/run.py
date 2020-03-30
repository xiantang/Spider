from scrapy import cmdline


name = 'meituan'
cmd = 'scrapy crawl {0}  -o ductdetail23.csv'.format(name)
cmdline.execute(cmd.split())