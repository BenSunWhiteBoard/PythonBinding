#include <stdio.h>
// pointer usage
void add_one(int *x) {
    printf("C: before add_one x is:%i\n", *x);
    *x += 1;
    printf("C: after add_one x is:%d\n", *x);
}

// struture
struct MyStruct 
{
    double *data;
    int size;
};

void print_my_struct(struct MyStruct *my_st){

    printf("C: my_st has data array start from:%p\n", my_st->data);
    printf("C: my_st has array size:%d\n", my_st->size);

    for (size_t i = 0; i < my_st->size; i++)
    {
        printf("C: %li th data is %f\n", i, my_st->data[i]);
    }
}


