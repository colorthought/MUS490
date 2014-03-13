#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include </c/cs223/Hwk3/getLine.h>

int main(int argc, char *argv[]) {
 
  if (argc < 4) {
    printf("Invalid input. \n");
    exit(0);
   }
  int i = 1;
  int triplecounter = 0;
  
  //argument counter;
  while (argv[i][0] == '+') {
    i += 3;      
  }

  triplecounter = i % 3;
  printf("There are %d triples\n", triplecounter);
  
  //file counter
  int filecounter = 0; 
  while(i < argc) {
    i++, filecounter++;
  }
  printf("There are %d files\n", filecounter);

  //for each file
  for (int f = 0; f < filecounter; f++) {
    char *file;
    int cFile = (triplecounter*3) + f + 1;
    int flength = strlen(argv[cFile]);
    file = malloc(flength + 1);
    strcpy(file, argv[cFile]);
    //debug
    printf("%s\n ", file);
    for (int i = 0; i < triplecounter; i++)
    {
      char *FROMi;
      char *TOi;
      int flagi = i*3 + 1;
      int FROMii = i*3 + 2;
      FROMi = malloc(strlen(argv[FROMii]));
      TOi = malloc(strlen(argv[TOii]));
      strcpy(
      int TOii = i*3 + 3;
    }
    free(file);
  }
}
