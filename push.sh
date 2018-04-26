#git add *
#GIT_AUTHOR_DATE='your date' GIT_COMMITTER_DATE='your date' git commit -m 'new (old) files'
#git commit -m "rakiduam"
#git commit -m printf '%(%Y-%m-%d)T\n'
#git commit --date="`stat -c %y myfile`" *
#git commit -m date +%F
#git commit -m printf '%(%Y-%m-%d)T\n'
#git push origin master
git add -u;
git commit -m "rakiduam generated files on `date +'%Y-%m-%d %H:%M:%S'`";
git push origin master