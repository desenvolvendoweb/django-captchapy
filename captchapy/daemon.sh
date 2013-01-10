#!/bin/bash

while [ 1 ]
do
    echo 'esperando o tempo para deletar a imagem:' $1 'com o tempo:' $2
    sleep $2
    break
done

rm $1

echo 'deletou com sucesso'