#pragma once
#include <stdio.h>
// f4helen.h --- f4 Helper Extension

typedef struct
{
    void* array;
    int size;
    int elem_size;
} f4_array;

f4_array* f4_new(unsigned int elem_size, unsigned int size)
{
    f4_array* a = malloc(sizeof(f4_array));
    a->array = malloc(elem_size * size);
    a->elem_size = elem_size;
    a->size = size;
    return a;
}

void f4_resize(f4_array* a, unsigned int new_size)
{
    a->array = realloc(a->array, a->elem_size * new_size);
    a->size = a->array ? new_size : 0;
}

void f4_free(f4_array *a)
{
    a->size = 0;
    free(a->array);
    free(a);
}

void f4_in(const char* format, ...)
{
    va_list a_list;
    va_start(a_list, x);
    va_end(a_list);
}

void f4_out(const char* format, ...)
{
    va_list a_list;
    va_start(a_list, x);
    va_end(a_list);
}