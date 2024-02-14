# Pre-intervie_challenge
Setup:
1) please download the TechChallenge.py file and place it the same folder where "stock_price_data_files" folder is. 
2) Open the code and go to lines 77-78
3) For line 77, replace the number with the desired number of files that you would like to be processed.
4) If the folder has a different name than "stock_price_data_files", please change the string from the line 78 with the name of the folder(as a string)
5) If you have previously run the program, please be sure you have all the CSV files closed. 
6) Run the program.
7) In the same folder with your program, new CSV files will be created.


Assumptions:
1) the CSV files are not corupted or protected by password
2) The CSV files have 3 columns with the following order: Stock-id, Timestamp, Stock-price

Things that could be improved:
1) The prediction could have been made using fewer rows. The current code covers the predictions only when the file has 10 ore more rows. 
2) An upgrade to the "save_to_csv" function like: 
    - If the file is open, to retry maximum 3 times and than continue to the next file
    - To save the file with a different name
3) In the scenario were we have multiple CSV files in a stock exchange and the requested number of files is lower than the number of CSV files, to be able to pick only the needed stocks/Stock Exchange
4) To be able to access the path of the folder no matter where the program is located.
