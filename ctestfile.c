#include <stdio.h>

int main() {
    int num;
    printf("Enter an integer: ");
    scanf("%d", &num);

    // If remainder after dividing by 2 is 0, it is even
    if (num % 2 == 0) {
        printf("%d is even.\n", num);
    } 
    else {
        printf("%d is odd.\n", num);
    }

    return 0;
}

