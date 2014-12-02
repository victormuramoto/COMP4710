#!/bin/bash

home_path='http://hearthstats.net/decks/public?utf8=%E2%9C%93&q[klass_id_eq]=&q[unique_deck_created_at_gteq]=2014-11-19+07%3A10%3A03+UTC&q[unique_deck_num_matches_gteq]=30&q[name_cont]=&items=100&sort=winrate&order=desc'

url_list=$(wget -q $home_path -O - | grep '<td class="name">' | cut -d\" -f4)

for url in $url_list;
do
	echo url: $url
	url_path="http://hearthstats.net$url"
	echo $url_path >> data.txt
	deck_name=$(wget -q $url_path -O - | grep 'col-md-12' | cut -d\> -f5 | cut -d\< -f1) >> data.txt
	echo $deck_name
	#for line in $deck_name;
	#do
	#	echo $line
	#done
	wget -q $url_path -O - | grep 'blizz_id' | cut -d\" -f6 >> data.txt
done
