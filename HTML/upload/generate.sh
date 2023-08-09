# ./generate.sh 运行执行脚本
# ./generate.sh -clear 删除执行结果
if [ $1 == "-clear" ]; then
    rm -r ./output
    rm attack_cost.dot
    rm attack_cost.eps
    rm attack_cost.pdf
    rm block_cost.dot
    rm block_cost.eps
    rm block_cost.pdf
    rm cvss.csv
else
    mkdir ./output
    python3 makeinput.py
    cd ./output
    graph_gen.sh input.P -p -v
    cd ..
    python3 rebuild.py
    dot -Tps attack_cost.dot > attack_cost.eps
    dot -Tps block_cost.dot > block_cost.eps
    epstopdf attack_cost.eps
    epstopdf block_cost.eps
fi

