# ! /bin/sh

basepath=$(cd `dirname $0`; pwd)

while true
do
    procnum=`ps -ef|grep "blog.py"|grep -v grep|wc -l`
    if [ $procnum -eq 0 ]
    then
        python blog.py > /dev/null 2>&1 &
        echo `date +%Y-%m-%d` `date +%H:%M:%S`  "restart blog 服务">>$basepath/blogShell.log
    fi
    sleep 5
done

