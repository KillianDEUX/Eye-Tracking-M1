#!/bin/bash
video="$1"
echo "============$video=========="
video_tag="$video-tag"
echo "$video_tag"
$(ffmpeg -i "$video".mp4 -i ../Images/tag1.png -i ../Images/tag2.png -i ../Images/tag3.png -i ../Images/tag4.png -filter_complex "[0] pad=iw+300:ih+300:iw+300:ih+300:color=white [pad],[1:v] scale=150:150 [ovr1], [2:v] scale=150:150 [ovr2], [3:v] scale=150:150 [ovr3], [4:v] scale=150:150 [ovr4], [pad][ovr1]overlay=0:0[v1], [v1][ovr2] overlay=W-w:0[v2], [v2][ovr3] overlay=0:H-h[v3], [v3][ovr4] overlay=W-w:H-h[v4]" -map "[v4]" "$video_tag".mp4)
echo "Ajout des tags terminé"

#Utilisation :
#./addTag.sh nomFichierVideo

#ffmpeg : sudo apt install ffmpeg
