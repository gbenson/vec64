#define PY_SSIZE_T_CLEAN
#include <Python.h>

PyDoc_STRVAR(indexify_base64__doc__,
"Transform Base64 alphabet symbols into their RFC 4648 integer values.\n"
"\n"
"The result is returned as a bytes object, with each byte containing the\n"
"value of one symbol in the input; `'hello'`, for example, indexifies as\n"
"`bytes((33, 30, 37, 37, 40))`.  Processing stops if a non-Base64 symbol\n"
"is encountered, so indexifying `'hello world'` returns the same 5-byte\n"
"sequence as indexifying `'hello'` did, since ASCII space is not a symbol\n"
"in the Base64 alphabet.");

static const char b64_symbol_indexes[] = {
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
indexify_base64(PyObject *self, PyObject *args)
{
    const char *encoding = NULL;
    char *str = NULL;
    Py_ssize_t size;

    if (!PyArg_ParseTuple(args, "es#", encoding, &str, &size)) {
        return NULL;
    }

    unsigned char *buf = (unsigned char *) str;
    unsigned char *limit = buf + size;
    for (unsigned char *p = buf; p < limit; p++) {
        unsigned char c = *p;
        unsigned char i = b64_symbol_indexes[c];

        if ((i & ~63) != 0) {
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
    {"indexify_base64", indexify_base64, METH_VARARGS, indexify_base64__doc__},
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
