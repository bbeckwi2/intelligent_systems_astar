#include<limits.h>
#include<iostream>
#include"Board.h"
#define getIndex(x,y) x + y * Y_DIM

    inline bool Board::validSpace(int x, int y){
      if (x > X_DIM || x < 0 || y > Y_DIM || y < 0) return false;
      return true;
    }

    Board::Board(int newBoard[9]){
      board = newBoard;
      h = (*hFunc)(board);
    }

    bool Board::swap(int x1, int y1, int x2, int y2){
      if (this->validSpace(x1, y1) && this->validSpace(x2, y2)){
        int i = getIndex(x1, y1);
        int j = getIndex(x2, y2);

        //swap
        int tmp = this->board[i];
        this->board[i] = this->board[j];
        this->board[j] = tmp;

      }
      return false;
    }

    int Board::get(int x, int y){
      if (this->validSpace(x, y)){
        return this->board[getIndex(x,y)];
      }
      return -1;
    }

    bool Board::operator <(const Board& other){
      return h < other.h;
    }
