#include <iostream>
#include <fstream>
#include <string>

using namespace std;

void xorEncryptDecrypt(const string &inputFile, const string &outputFile, const string &key) {
    ifstream inFile(inputFile, ios::binary);
    ofstream outFile(outputFile, ios::binary);

    char ch;
    int keyIndex = 0;

    while (inFile.get(ch)) {
        // Effectuer l'opération XOR avec le caractère de la clé
        char encryptedChar = ch ^ key[keyIndex];

        // Écrire le caractère chiffré dans le fichier de sortie
        outFile.put(encryptedChar);

        // Avancer l'index de la clé, répéter si nécessaire
        keyIndex = (keyIndex + 1) % key.length();
    }

    inFile.close();
    outFile.close();
}

int main(int argc, char* argv[]) {
    if (argc < 3) {
        cout << "Utilisation : " << argv[0] << " <fichier d'entrée> <fichier de sortie> [clé de chiffrement]" << endl;
        return 1;
    }

    string inputFile = argv[1];
    string outputFile = argv[2];
    string key;

    if (argc >= 4) {
        key = argv[3];
    } else {
        // Lire la clé depuis un fichier
        ifstream keyFile("key.txt");
        if (!keyFile) {
            cerr << "Erreur : Impossible de lire la clé depuis le fichier 'key.txt'." << endl;
            return 1;
        }
        getline(keyFile, key);
        keyFile.close();
    }

    xorEncryptDecrypt(inputFile, outputFile, key);
    cout << "Opération réussie." << endl;

    return 0;
}

