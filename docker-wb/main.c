#include <stdio.h>

int fib(int n) {
    if (n <= 1) {
        return n;
    } else {
        return fib(n - 1) + fib(n - 2);
    }
}

int main() {
    int n;
    printf("Введите номер числа Фибоначчи: ");
    scanf("%d", &n);
    printf("Число Фибоначчи %d равно %d\n", n, fib(n));
    return 0;
}