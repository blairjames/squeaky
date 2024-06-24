![Squeaky](lizard_squeaky.jpg)

### Fast word list cleaner and de-duplicator. <br>
- Filters problem characters that play havoc with UTF-8 and removes duplicates to avoid inefficient use of resources. <br>
- Allows removal of words below a specified length. <br>
- Very handy when optimizing and combining multiple large wordlists.  <br><br>

### Usage:
git clone https://github.com/blairjames/squeaky.git <br> 
``` squeaky.py [-h] [-d] [-l LEN] [-u] input_file output_file ```

positional arguments: <br>
--input_file <br>
--output_file <br>

options: <br>
  -h, --help         - show this help message and exit. <br>
  -d, --dir          - Input a directory to process for word lists. (".txt" files) <br>
  -l LEN, --len LEN  - Minimum word length, words shorter than specified length will be 
                       removed. <br>
  -u, --unique       - Delete duplicate words in word list. <br>
