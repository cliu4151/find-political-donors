# InsightDataScience Challenge Submission: find-politcal-donors

### Author of Challenge Submission: Connie Liu

This is a submission for the InsightDataScience challenge
https://github.com/InsightDataScience/find-political-donors

Identify possible donors for a variety of upcoming election campaigns from Federal Election Commission campaign contributions data. Example output files would be:
1. `medianvals_by_zip.txt`: contains a calculated running median, total dollar amount and total number of contributions by recipient and zip code
2. `medianvals_by_date.txt`: has the calculated median, total dollar amount and total number of contributions by recipient and date.


## Approach

To generate the two output files medianvals_by_zip.txt and medianvals_by_date.txt:
1. For each line read from the input file, I extracted the relevant 5 data pieces (cmte_id, zipcode, transaction_dt, transaction_amt, other_id)
2. After extraction, data is IGNORED if these conditions are NOT met:

    For both outputs
    * `other_id` is empty
    * `cmte_id` is NOT empty
    * `transaction_amt` is NOT empty

    For only `medianvals_by_zip.txt`
    * `zipcode` is NOT empty and length of first 5 characters of zipcode is equal to five

    For only `medianvals_by_date.txt`
    * `transaction_dt` is valid date

3. For the first output file medianvals_by_zip.txt, the data is processed and appended into corresponding map to 3 dictionaries using `guid` of `cmte_id` and `zipcode`
    * A rolling median is calculated for each line of input
    * The cmte_id, zipcode, resulting rolling median, number of transactions, total of transaction amounts are written to specificed first output file name (e.g. medianvals_by_zip.txt) delimited by `|`
4. For the second output file medianvals_by_date.txt, the data is mapped into 3 dictionaries using `guid_date` of `cmte_id` and `transaction_dt`
    * Similar to step three, each line of input is processed and appended to dictionaries using guid_date as the key
    * Calculations and writing to the second output file are made after the entire input file is processed
    * The guid_date keys are sorted alphabetically and then chronologically by date
    * For each key in the sorted list of guid_date, the corresponding cmte_id, transaction_dt, median, number of transactions, and total transaction amount are written to second output file name (e.g. medianvals_by_date.txt)


## Running the code

Enter `./run.sh` in the find-political-donors directory to run script that contains the following command
to run the program `find_political_donors.py` on the file in the input folder

```
python ./src/find_political_donors.py ./input/itcont.txt ./output/medianvals_by_zip.txt ./output/medianvals_by_date.txt`
```

Currently in the input directory, there is the input file from the original challenge README.  Testing of other inputs were done via `insight_testsuite/tests`


## Running the tests

The tests are stored as text files under the `insight_testsuite/tests` folder. Each test has a separate folder with an `input` folder for `itcont.txt` and an `output` folder for output corresponding to that test.

Run the tests with the following command from within the `insight_testsuite` folder:

    insight_testsuite~$ ./run_tests.sh

In addition to the provided test_1, these tests have been added:
* test_no_or_invalid_zipcode: No zipcodes or invalid zipcodes
* test_invalid_dates: Invalid dates

### Unit Tests

Run unit tests for checkDate function (`test_find_political_donors.py`) from within the `insight_testsuite` folder
    
    insight_testsuite~$ python test_find_political_donors.py


## Solution Utilizes

* Python
* Python libraries & modules: numpy, heapq, sys, math, datetime


## Acknowledgments

The Rolling median class (streamMedian) is by Arden Dertat
(http://www.ardendertat.com/2011/11/03/programming-interview-questions-13-median-of-integer-stream/)
