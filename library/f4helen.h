#pragma once
#include <stdio.h>
#include <stdarg.h>
#include <stdlib.h>
// f4helen.h --- f4 Helper Extension

typedef struct
{
    void* array;
    int size, elem_size;
    char type;
} f4_array;

f4_array* f4_new(char type, unsigned int size)
{
    f4_array* a = malloc(sizeof(f4_array));
    int elem_size = sizeof(void*);
    switch(type)
    {
    case 'c':
        elem_size = sizeof(char);
    case 'd':
        elem_size = sizeof(int);
    case 'f':
        elem_size = sizeof(double);
    case 's':
        elem_size = sizeof(char *);
    }
    a->elem_size = elem_size;
    a->array = malloc(elem_size * size);
    a->type = type;
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

}

void f4_out(const char* format, ...)
{
    const char *p;
    va_list argp;
    int i;
    double d;
    char *s;
    f4_array *arr;
    char fmtbuf[256];

    va_start(argp, format);

    for(p = format; *p != '\0'; p++)
        {
        if(*p != '%')
            {
            putchar(*p);
            continue;
            }

        switch(*++p)
            {
            case 'c':
                i = va_arg(argp, int);
                putchar(i);
                break;

            case 'd':
                i = va_arg(argp, int);
                sprintf(fmtbuf, "%d", i);
                fputs(fmtbuf, stdout);
                break;

            case 'f':
                d = va_arg(argp, double);
                sprintf(fmtbuf, "%f", d);
                fputs(fmtbuf, stdout);
                break;

            case 's':
                s = va_arg(argp, char *);
                fputs(s, stdout);
                break;

            case 'a':
                fmtbuf[0] = '[';
                char* f = fmtbuf+1;
                arr = va_arg(argp, f4_array *);
                switch(arr->type)
                {
                case 'c':
                    break;
                case 'd':
                    break;
                case 'f':
                    break;
                case 's':
                    break;
                }
                break;

            case '%':
                putchar('%');
                break;
            }
        }
    va_end(argp);
}