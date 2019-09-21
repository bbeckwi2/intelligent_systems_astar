#include<iostream>
#include"Board.h"

using namespace std;

int aStar(int * );
int (*Board::hFunc)(int *);
int main(int argc, char *argv[]){

  if(argc<2){
    cout << "Enter board when executing."<< endl;
    exit(1);
  }
  char **input = &argv[1];
  int board[9];

  for(int i = 0; i < 9; i++){
    board[i] = *(*input+i);
  }

  Board::hFunc = &aStar;
  Board myBoard (board);

  return 0;
}

int aStar(int *){
  cout << "I'm A Star" << endl;
  return 0;
}
