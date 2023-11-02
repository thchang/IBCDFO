#include <iostream>
#include <stdlib.h>

int main()
{
  std::cout << "There are lots of ways executables might print to screen\n";
  printf("Are they all easy to catch?\n");
  system("echo What about this?\n");
  return 0;
}
