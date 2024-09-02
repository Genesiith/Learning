#include <stdio.h>

int putnbr(int nbr){
    if (nbr < 0){
        putchar('-');
        nbr = -nbr;
    }
    
    if (nbr > 9){
        putnbr(nbr / 10);
    }
    
    putchar(nbr % 10 + '0');
    return 0;
}