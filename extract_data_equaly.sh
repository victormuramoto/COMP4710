#!/bin/bash

out='data.txt'
aux=$(date -v-30d "+%Y %m %d")
_yyyy=$(echo $aux | cut -d' ' -f1)
_mm=$(echo $aux | cut -d' ' -f2)
_dd=$(echo $aux | cut -d' ' -f3)

rm $out
num_deck=240
num_match=25

echo Any Druid Hunter Mage Paladin Priest Rogue Shaman Warlock Warrior >> $out

for i in {1..9}:
do
	home_path="http://hearthstats.net/decks/public?utf8=%E2%9C%93&q[klass_id_eq]=$i&q[unique_deck_created_at_gteq]=$_yyyy-$_mm-$_dd+00%3A00%3A00+UTC&q[unique_deck_num_matches_gteq]=$num_match&q[name_cont]=&items=100&sort=winrate&order=asc"
	
	count=$(wget -q $home_path -O - | grep 'found matching' | cut -d' ' -f1 | cut -d\> -f2)
	
	if [[ "$count" -lt "$num_deck" ]]; then
        num_deck="$count"
    fi
done

for i in {1..9}:
do
	home_path="http://hearthstats.net/decks/public?utf8=%E2%9C%93&q[klass_id_eq]=$i&q[unique_deck_created_at_gteq]=$_yyyy-$_mm-$_dd+00%3A00%3A00+UTC&q[unique_deck_num_matches_gteq]=$num_match&q[name_cont]=&items=$num_deck&sort=winrate&order=asc"
	
	echo $num_deck
	echo $num_deck >> $out
	
	url_list=$(wget -q $home_path -O - | grep '<td class="name">' | cut -d\" -f4 | tail -n $num_deck)
	winrate_list=$(wget -q $home_path -O - | grep 'class="winrate"' | cut -d\> -f2 | cut -d\< -f1 | tr -d % | tail -n $num_deck)
	
	echo $winrate_list
	echo $winrate_list >> $out
	
	for url in $url_list:	
	do
		url_path="http://hearthstats.net$url"
		deck_name=$(wget -q $url_path -O - | grep 'col-md-12' | cut -d\> -f5 | cut -d\< -f1)
		#deck_cost=$(wget -q $url_path -O - | grep 'class="deck-details row"' | cut -d\> -f36 | cut -d\< -f1)
		echo $deck_name
		echo $deck_name >> $out
		deck_cards=$(wget -q $url_path -O - | grep 'blizz_id' | cut -d\" -f6) 
		echo $deck_cards >> $out
		#card_imgs=$(wget -q $url_path -O - | grep 'blizz_id' | cut -d\" -f38 | cut -d\/ -f6)
		#echo $card_imgs >> $out 
	done
done


