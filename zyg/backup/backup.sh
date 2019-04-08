#!/bin/bash
#备份neo4j数据库

file=$(date +%Y-%m-%d)

#备份文件路径
#bak_path = /home/python/Desktop/new/beifen

#数据库目录
#db_path = /home/python/Desktop/new/neo4j-community-3.4.5/bin

echo $file

cd /home/yangxl/neo4j-community-3.4.10/bin

#cd /home/python/Desktop/new/neo4j-community-3.4.5/bin

#关闭数据库
./neo4j stop

echo ‘开始备份…’

#./neo4j-admin  dump --database=graph_bak.db --to=/mnt/backup/$file.db_bak.zip

./neo4j-admin  dump --database=jibin.db --to=/mnt/backup/$file.db

echo ‘备份完成’
./neo4j start

find /mnt/backup -mtime +30 -type f -name '*.db' -exec rm {} \;


