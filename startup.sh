#!/bin/bash
chmod +x tweet.py

# Save current cron jobs, append our cronjob
crontab -l > tempcron
echo "*/1 * * * * source $HOME/Coding\ Projects/Python/dsa-tw/.env; (cd $HOME/Coding\ Projects/Python/dsa-tw/utility; sh ./run.sh create) && python $HOME/Coding\ Projects/Python/dsa-tw/tweet.py >> ./log.txt 2>&1 && rm $HOME/Coding\ Projects/Python/dsa-tw/utility/post_*.txt" >> tempcron
crontab tempcron
rm tempcron
#(cd $HOME/Coding\ Projects/Python/dsa-tw/utility; sh ./run.sh create)
#python $HOME/Coding\ Projects/Python/dsa-tw/tweet.py >> ./log.txt 2>&1
#rm $HOME/Coding\ Projects/Python/dsa-tw/utility/post_*.txt
