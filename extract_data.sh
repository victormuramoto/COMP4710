#!/bin/bash

out='data.txt'
aux=$(date -v-3d "+%Y %m %d")
_yyyy=$(echo $aux | cut -d' ' -f1)
_mm=$(echo $aux | cut -d' ' -f2)
_dd=$(echo $aux | cut -d' ' -f3)

rm $out

echo Any Druid Hunter Mage Paladin Priest Rogue Shaman Warlock Warrior >> $out

for i in {1..9};
do
	home_path="http://hearthstats.net/decks/public?utf8=%E2%9C%93&q[klass_id_eq]=$i&q[unique_deck_created_at_gteq]=$_yyyy-$_mm-$_dd+00%3A00%3A00+UTC&q[unique_deck_num_matches_gteq]=35&q[name_cont]=&items=100&sort=winrate&order=desc"
	
	count=$(wget -q $home_path -O - | grep '<td class="name">' | wc -l)
	echo $count
	echo $count >> $out
	
	url_list=$(wget -q $home_path -O - | grep '<td class="name">' | cut -d\" -f4)

	for url in $url_list;	
	do
		url_path="http://hearthstats.net$url"
		deck_name=$(wget -q $url_path -O - | grep 'col-md-12' | cut -d\> -f5 | cut -d\< -f1)
		#deck_cost=$(wget -q $url_path -O - | grep 'class="deck-details row"' | cut -d\> -f36 | cut -d\< -f1)
		echo $deck_name
		echo $deck_name >> $out
		deck_cards=$(wget -q $url_path -O - | grep 'blizz_id' | cut -d\" -f6) 
		echo $deck_cards >> $out
	done
done
