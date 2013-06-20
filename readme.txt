ITP 125 – Programming Project with Python - Hash table generation and Crack hash from rainbow table
Author: Chad Martin

Uses Python 3.3

This program can either generate hashes based on a password list or take an input file of some hashes and spit out the cracked version of the hashes based on the rainbow table that was created.

04/30/2012 Chi said the only input validation needed is to make sure -ops is either "generate" or "crack" and -t is either "md5" or "sha1" and check if -i is a local file or URL. If -i is a local file check if it exists

external URLs are assumed to be correct

Time to create the table and Time to crack the hashes include the time taken to fetch input files