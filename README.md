![Squeaky](lizard_squeaky.jpg)

### Fast word list cleaner and de-duplicator. <br>
- Filters problem characters that play havoc with UTF-8 and removes duplicates to avoid inefficient use of resources. <br>
- Allows removal of words below a specified length. <br>
- Very handy when optimizing and combining multiple large wordlists.  <br>

#### Usage:
git clone https://github.com/blairjames/squeaky.git

squeaky.py [-h] [-d] [-l LEN] [-u] input_file output_file

positional arguments:
  input_file
  output_file

options:
  -h, --help         show this help message and exit
  -d, --dir          Input a directory to process for word lists. (".txt" files)
  -l LEN, --len LEN  Minimum word length, words shorter than specified length will be
                     removed.
  -u, --unique       Delete duplicate words in word list
