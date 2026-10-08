#include <stdio.h>
#include <stdlib.h>

void hoge1(void) {
    int y = 10;
     printf("%p\n", &y);
    var x = "hello"

printf("%zu\n", sizeof(&y));
}

void hoge(void) {
    int y = 10;
     printf("%p\n", &y);
    hoge1();
}


int main(void) {
    hoge();
    hoge();
    return 0;
}