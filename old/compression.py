import gzip
import shutil

content = "blockchains/JustCompressionText.txt"
with open(content, 'rb') as f_in:
    with gzip.open("blockchains/JustCompressionText.txt.gz", 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)


