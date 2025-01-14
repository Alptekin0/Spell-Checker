# Spell-Checker
Detect spelling mistakes in Turkish texts and fixes them.
This project used Zemberek dataset and coded in python.
But the Zemberek dataset is java-based That's why we used Zemberek's gRPC service.
This allowed us to send efficient, fast and error-free requests over protocols.
At the same time, only the normalization module of the Zemberek dataset was used.
Because it is a sufficient module for spell checking and correction. (Normalization;	zemberek-normalization:	Basic spell checker, word suggestion. Noisy text normalization.)


To run the code, you need to execute and start the following command using Docker:

docker run -d --rm -p 6789:6789 -p 6790:6790 --name zemberek-grpc ryts/zemberek-grpc


All necessary explanations have been made in the code.
