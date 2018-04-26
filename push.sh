git add *
#GIT_AUTHOR_DATE='your date' GIT_COMMITTER_DATE='your date' git commit -m 'new (old) files'
#git commit -m "fernando"
#git commit -m printf '%(%Y-%m-%d)T\n'
#git commit --date="`stat -c %y myfile`" *
git commit -m "date +%F"
#git commit -m printf '%(%Y-%m-%d)T\n'
git push origin master
