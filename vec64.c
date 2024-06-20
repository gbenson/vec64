#define PY_SSIZE_T_CLEAN
#include <Python.h>

PyDoc_STRVAR(base64_symbol_indexes__doc__,
"Transform Base64 alphabet symbols into their RFC 4648 integer values.\n"
"\n"
"Given a string or bytes-like object, return a bytes object in which\n"
"each byte contains the value of the corresponding symbol from in the\n"
"input.  Processing stops at the first non-Base64 symbol or when the\n"
"end of the input is reached, whichever is sooner.   Up to two padding\n"
"characters (`'='`) will be transformed into zero values (`b'\\0'`) at\n"
"the end of the input.\n"
"\n"
"Usage examples:\n"
"\n"
"```python\n"
">>> list(base64_symbol_indexes('hello'))\n"
"[33, 30, 37, 37, 40]\n"
">>> list(base64_symbol_indexes('hello world'))\n"
"[33, 30, 37, 37, 40]        # processing stopped at the ' '\n"
">>> list(base64_symbol_indexes('hello='))\n"
"[33, 30, 37, 37, 40, 0]     # the '=' transforms to '\\0'\n"
">>> list(base64_symbol_indexes('hello==='))\n"
"[33, 30, 37, 37, 40, 0, 0]  # processing stopped after the second '='\n"
"```\n");

static const char symbol_index_table[] = {
    -1, -1, -1, -1,   -1, -1, -1, -1,   -1, -1, -1, -1,   -1, -1, -1, -1,
    -1, -1, -1, -1,   -1, -1, -1, -1,   -1, -1, -1, -1,   -1, -1, -1, -1,
    -1, -1, -1, -1,   -1, -1, -1, -1,   -1, -1, -1, 62,   -1, -1, -1, 63,
    52, 53, 54, 55,   56, 57, 58, 59,   60, 61, -1, -1,   -1, -1, -1, -1,
    -1,  0,  1,  2,    3,  4,  5,  6,    7,  8,  9, 10,   11, 12, 13, 14,
    15, 16, 17, 18,   19, 20, 21, 22,   23, 24, 25, -1,   -1, -1, -1, -1,
    -1, 26, 27, 28,   29, 30, 31, 32,   33, 34, 35, 36,   37, 38, 39, 40,
    41, 42, 43, 44,   45, 46, 47, 48,   49, 50, 51, -1,   -1, -1, -1, -1,

    -1, -1, -1, -1,   -1, -1, -1, -1,   -1, -1, -1, -1,   -1, -1, -1, -1,
    -1, -1, -1, -1,   -1, -1, -1, -1,   -1, -1, -1, -1,   -1, -1, -1, -1,
    -1, -1, -1, -1,   -1, -1, -1, -1,   -1, -1, -1, -1,   -1, -1, -1, -1,
    -1, -1, -1, -1,   -1, -1, -1, -1,   -1, -1, -1, -1,   -1, -1, -1, -1,
    -1, -1, -1, -1,   -1, -1, -1, -1,   -1, -1, -1, -1,   -1, -1, -1, -1,
    -1, -1, -1, -1,   -1, -1, -1, -1,   -1, -1, -1, -1,   -1, -1, -1, -1,
    -1, -1, -1, -1,   -1, -1, -1, -1,   -1, -1, -1, -1,   -1, -1, -1, -1,
    -1, -1, -1, -1,   -1, -1, -1, -1,   -1, -1, -1, -1,   -1, -1, -1, -1,
};

static PyObject *
base64_symbol_indexes(PyObject *self, PyObject *args)
{
    const char *encoding = NULL;
    char *str = NULL;
    Py_ssize_t size;

    if (!PyArg_ParseTuple(args, "et#", encoding, &str, &size)) {
        return NULL;
    }

    unsigned char *buf = (unsigned char *) str;
    unsigned char *limit = buf + size;
    for (unsigned char *p = buf; p < limit; p++) {
        unsigned char c = *p;
        unsigned char i = symbol_index_table[c];

        if ((i & ~63) != 0) {
            // Process up to two padding characters
            if (c == '=') {
                *(p++) = 0;

                if (p < limit && *p == '=')
                    *(p++) = 0;
            }

            size = p - buf;
            break;
        }

        *p = i;
    }

    PyObject *result = PyBytes_FromStringAndSize(str, size);
    PyMem_Free(str);

    return result;
}

static PyMethodDef vec64_methods[] = {
    {"base64_symbol_indexes",
     base64_symbol_indexes,
     METH_VARARGS,
     base64_symbol_indexes__doc__},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef vec64_module = {
    PyModuleDef_HEAD_INIT,
    "_vec64",
    .m_doc = "word2vec-style embeddings for base64",
    .m_size = 0,
    .m_methods = vec64_methods,
};

PyMODINIT_FUNC
PyInit_vec64(void)
{
    return PyModule_Create(&vec64_module);
}
