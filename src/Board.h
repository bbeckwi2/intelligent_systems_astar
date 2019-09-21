    class Board
    {
        private: 
            int *board;

            static const int X_DIM = 3;
            static const int Y_DIM = 3;
            
            inline bool validSpace(int x, int y);
            
            int h = INT_MAX;
        public:
            static int (*hFunc)(int *);
            Board(int newBoard[9]);
            bool swap(int x1, int y1, int x2, int y2);
            int get(int x, int y);
            bool operator <(const Board& other);
    };