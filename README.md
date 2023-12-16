# StudyFlix-Downloader
A Proof of Concept to download videos from the german education site StudyFlix.de

# Usage
Run the Python script and pass in URLs in quotes seperated by spaces
```py
python downloader.py "example1" "example2"
```

Or just create a file that contains a link per line and parse it via `--file` or `-f` flag
```py
python downloader.py --file list.txt
```