#!/bin/bash


echo "Executing dcfinder-1.2-SNAPSHOT.jar"
java -cp metanome-cli-1.2-SNAPSHOT.jar:dcfinder-1.2-SNAPSHOT.jar de.metanome.cli.App \
    -a de.metanome.algorithms.dcfinder.DCFinderMetanome \
    --file-key INPUT --files ./datasets/ncvoter_1001r_19c.csv --header --separator , \
    --algorithm-config APPROXIMATION_DEGREE:0


# java -cp metanome-cli-1.2-SNAPSHOT.jar:dcfinder-1.2-SNAPSHOT.jar de.metanome.cli.App \
#     -a de.metanome.algorithms.dcfinder.DCFinderMetanome


# java -cp metanome-cli-1.2-SNAPSHOT.jar:TANE-1.2-SNAPSHOT.jar de.metanome.cli.App \
#     -a de.metanome.algorithms.tane.TaneAlgorithm \
#     --file-key INPUT_GENERATOR \
#     --files nursery.csv \
#     --separator , \
#     --ignore-leading-spaces \
#     --header


# java -cp metanome-cli-1.2-SNAPSHOT.jar:hydra-1.2-SNAPSHOT.jar de.metanome.cli.App \
#     -a de.hpi.naumann.dc.algorithms.hybrid.HydraMetanome --file-key INPUT_FILES --files ./datasets/iris.csv --header --separator ,


# echo "Script de testes!"

# echo "Executando hydra-1.2-SNAPSHOT.jar"
# java -cp metanome-cli-1.2-SNAPSHOT.jar:hydra-1.2-SNAPSHOT.jar de.metanome.cli.App -a de.hpi.naumann.dc.algorithms.hybrid.HydraMetanome --file-key INPUT --files iris.csv --header --separator ,


# echo "Executando HyUCC-1.2-SNAPSHOT.jar"
# java -cp metanome-cli-1.2-SNAPSHOT.jar:HyUCC-1.2-SNAPSHOT.jar de.metanome.cli.App -a de.metanome.algorithms.hyucc.HyUCC --file-key INPUT_GENERATOR --files iris.csv --header --separator ,

# echo "FALTA HYFD"

# echo "Executando ORDER-1.2-SNAPSHOT.jar"
# java -cp metanome-cli-1.2-SNAPSHOT.jar:ORDER-1.2-SNAPSHOT.jar de.metanome.cli.App -a de.metanome.algorithms.order.ORDERLhsRhs --file-key RELATIONAL_INPUT --files iris.csv --header --separator ,

# echo "Executando BINDER-1.2-SNAPSHOT.jar"
# java -cp metanome-cli-1.2-SNAPSHOT.jar:BINDER-1.2-SNAPSHOT.jar de.metanome.cli.App -a de.metanome.algorithms.binder.BINDERFile --file-key INPUT_FILES --files iris.csv --header --separator ,

echo "Script de testes concluído!"
