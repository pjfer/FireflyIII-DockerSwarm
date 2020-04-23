
number_of_clients=10
python_command="python3 client.py "
pw="?URz/cJqyL3ba=DQ"

for (( i=2; i<=$1; i++ ))
do
eval $python_command"user"$i"@mail.com "$pw >logs/client"$i".out 2>&1 &
    sleep 5
printf "Client "$i" started!\n"
done
