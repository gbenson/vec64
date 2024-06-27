#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <stdbool.h>

#if __GNUC__ >= 3
# define unlikely(cond)   __builtin_expect(!!(cond), 0)
# define likely(cond)     __builtin_expect(!!(cond), 1)
#else
# define unlikely(cond)   (cond)
# define likely(cond)     (cond)
#endif

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
    52, 53, 54, 55,   56, 57, 58, 59,   60, 61, -1, -1,   -1, 64, -1, -1,
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

        if (unlikely((i & ~63) != 0)) {
            // Process up to two padding characters
            if (c == '=') {
                *(p++) = 64;

                if (p < limit && *p == '=')
                    *(p++) = 64;
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

// Symbol and range types.  A bitmask of symbol characteristics, with
// individual symbol type values chosen such that the overall type of
// a group of symbols can be calculated by combining their individual
// symbol symbol types using bitwise AND to knock out unshared bits.
//
// e.g. RT_UPPER_ALPHAHEX  // [A-F]
//           & RT_DECIMAL  // [0-9]
//         => RT_UPPERHEX  // [A-F0-9]
//  or  RT_UPPER_ALPHAHEX  // [A-F]
//             & RT_LOWER  // [a-z]
//            => RT_ALPHA  // [A-Za-z]
//
// XXX would changing symbol_type_t to uintptr_t make things faster?
// Speed test, but also and maybe disassemble and see if using bytes
// means we're wasting cycles masking and shifting.
typedef unsigned char symbol_type_t;

// Symbol characteristics
#define SBIT_UPPER  (1<<0)
#define SBIT_LOWER  (1<<1)
#define SBIT_ALPHA  (1<<2)
#define SBIT_DIGIT  (1<<3)
#define SBIT_HEX    (1<<4)
#define SBIT_ALNUM  (1<<5)
#define SBIT_PUNCT  (1<<6)
#define SBIT_MASK  ((1<<7)-1)

// Range types
#define RT_NONE           ((symbol_type_t) -1)  // No symbols have seen
#define RT_BASE64         0           // Every type of symbol was seen
#define RT_PUNCT          SBIT_PUNCT  // Only '+' and '/' were seen

#define RT_ALNUM          SBIT_ALNUM               // A-Za-z0-9
#define RT_UPPER_ALNUM    (SBIT_UPPER | RT_ALNUM)  // A-Z0-9
#define RT_LOWER_ALNUM    (SBIT_LOWER | RT_ALNUM)  // a-z0-9

#define RT_HEX            (SBIT_HEX | RT_ALNUM)  // A-Fa-f0-9
#define RT_UPPERHEX       (SBIT_HEX | RT_UPPER_ALNUM)  // A-F0-9
#define RT_LOWERHEX       (SBIT_HEX | RT_LOWER_ALNUM)  // a-f0-9

#define RT_ALPHAHEX       (SBIT_ALPHA | RT_HEX)      // A-Fa-f
#define RT_UPPER_ALPHAHEX (SBIT_ALPHA | RT_UPPERHEX) // A-F
#define RT_LOWER_ALPHAHEX (SBIT_ALPHA | RT_LOWERHEX) // a-f

#define RT_DECIMAL        (SBIT_DIGIT | RT_HEX | SBIT_UPPER | SBIT_LOWER)  // 0-9

#define RT_ALPHA          (SBIT_ALPHA | RT_ALNUM)  // A-Za-z
#define RT_UPPER          (SBIT_ALPHA | RT_UPPER_ALNUM)  // A-Z
#define RT_LOWER          (SBIT_ALPHA | RT_LOWER_ALNUM)  // a-z

// Individual symbol types
#define ST_UAHEX  RT_UPPER_ALPHAHEX
#define ST_UPPER  RT_UPPER
#define ST_LAHEX  RT_LOWER_ALPHAHEX
#define ST_LOWER  RT_LOWER
#define ST_DIGIT  RT_DECIMAL
#define ST_PUNCT  RT_PUNCT

static const symbol_type_t symbol_type_table[] = {
     ST_UAHEX, ST_UAHEX, ST_UAHEX, ST_UAHEX,  // ABCD
     ST_UAHEX, ST_UAHEX, ST_UPPER, ST_UPPER,  // EFGH
     ST_UPPER, ST_UPPER, ST_UPPER, ST_UPPER,  // IJKL
     ST_UPPER, ST_UPPER, ST_UPPER, ST_UPPER,  // MNOP
     ST_UPPER, ST_UPPER, ST_UPPER, ST_UPPER,  // QRST
     ST_UPPER, ST_UPPER, ST_UPPER, ST_UPPER,  // UVWX
     ST_UPPER, ST_UPPER, ST_LAHEX, ST_LAHEX,  // YZab
     ST_LAHEX, ST_LAHEX, ST_LAHEX, ST_LAHEX,  // cdef
     ST_LOWER, ST_LOWER, ST_LOWER, ST_LOWER,  // ghij
     ST_LOWER, ST_LOWER, ST_LOWER, ST_LOWER,  // klmn
     ST_LOWER, ST_LOWER, ST_LOWER, ST_LOWER,  // opqr
     ST_LOWER, ST_LOWER, ST_LOWER, ST_LOWER,  // stuv
     ST_LOWER, ST_LOWER, ST_LOWER, ST_LOWER,  // wxyz
     ST_DIGIT, ST_DIGIT, ST_DIGIT, ST_DIGIT,  // 0123
     ST_DIGIT, ST_DIGIT, ST_DIGIT, ST_DIGIT,  // 4567
     ST_DIGIT, ST_DIGIT, ST_PUNCT, ST_PUNCT,  // 89+/
     ST_PUNCT,                                // =
};

PyDoc_STRVAR(vec64_split__doc__,
"Split a sequence of Base64 symbol indexes by character type.\n"
"\n"
"Given a bytes-like object of Base64 alphabet symbol indexes as\n"
"returned by `base64_symbol_indexes`, return a list of 3-tuples\n"
"describing the ranges of character types found.  Each returned\n"
"tuple comprises start and limit indexes into the input sequence\n"
"describing the characteristics all symbols in the range share.\n");

static PyObject *
vec64_split(PyObject *self, PyObject *args)
{
    const char *sequence;
    Py_ssize_t len, maxsplit = 0;
    symbol_type_t split_on_type = RT_NONE;

    if (!PyArg_ParseTuple(
            args, "y#|nB",
            &sequence, &len, &maxsplit, &split_on_type)) {
        return NULL;
    }

    if (maxsplit < 0) {
        maxsplit = 0;
    }

    unsigned char *buf = (unsigned char *) sequence;
    unsigned char *start = buf;
    unsigned char *limit = buf + len;
    symbol_type_t state = RT_NONE;
    bool in_split = false;

    PyObject *result = PyList_New(0);
    if (result == NULL) {
        return NULL;
    }

#define RECORD_RANGE(range_start, range_limit, range_kind) do { \
    PyObject *range = Py_BuildValue(                            \
        "(nnk)",                                                \
        (range_start) - buf,                                    \
        (range_limit) - buf,                                    \
        (range_kind));                                          \
                                                                \
    if (unlikely(range == NULL))                                \
        goto error;                                             \
                                                                \
    if (unlikely(PyList_Append(result, range) != 0))            \
        goto error;                                             \
} while (0)

#define DO_SPLIT(split_start, split_state, is_enter_split) do { \
    start = (split_start);                                      \
    new_state = (split_state);                                  \
    in_split = (is_enter_split);                                \
} while (0)

#define ENTER_SPLIT(_start, _state) DO_SPLIT((_start), (_state), true)
#define LEAVE_SPLIT(_start, _state) DO_SPLIT((_start), (_state), false)

    for (unsigned char *p = start; p < limit; p++) {
        unsigned char symbol_index = *p;

        if (unlikely(symbol_index > 64)) {
            PyErr_SetNone(PyExc_ValueError);
            goto error;
        }

        symbol_type_t symbol_type = symbol_type_table[symbol_index];
        symbol_type_t new_state = state & symbol_type;

        if (likely(new_state == state)) {
            continue;  // no change
        }

        unsigned char *pp = start;
        if (unlikely(symbol_type == split_on_type)) {
            ENTER_SPLIT(p, symbol_type);

            // Enforce maxsplit as necessary.
            if (maxsplit) {
                maxsplit -= 1;
                if (unlikely(!maxsplit)) {
                    split_on_type = RT_NONE;
                }
            }
        }
        else if (unlikely(in_split)) {
            LEAVE_SPLIT(p, symbol_type);
        }

        if (unlikely(state == RT_NONE)) {
            state = new_state;
            continue;  // don't record transitions from RT_NONE
        }

        RECORD_RANGE(pp, p, state);

        state = new_state;

        // Reaching RT_BASE64 means we've seen every symbol type: all
        // bits are knocked out, nothing we could encounter can cause
        // a state change, so we can stop processing early and return
        // our result if we reach it.
        if (unlikely(state == RT_BASE64)) {
            break;
        }
    }

    if (start < limit) {
        RECORD_RANGE(start, limit, state);
    }

#undef DO_SPLIT
#undef ENTER_SPLIT
#undef LEAVE_SPLIT
#undef RECORD_RANGE
    return result;

error:
    Py_CLEAR(result);
    return NULL;
}

static int
vec64_exec(PyObject *module)
{
#define ADD_INT_CONSTANT(v) do {                                \
    if (PyModule_AddIntConstant(module, "_" #v, v) < 0) {       \
        goto error;                                             \
    }                                                           \
} while (0)

    ADD_INT_CONSTANT(RT_BASE64);
    ADD_INT_CONSTANT(RT_PUNCT);
    ADD_INT_CONSTANT(RT_ALNUM);
    ADD_INT_CONSTANT(RT_UPPER_ALNUM);
    ADD_INT_CONSTANT(RT_LOWER_ALNUM);
    ADD_INT_CONSTANT(RT_HEX);
    ADD_INT_CONSTANT(RT_UPPERHEX);
    ADD_INT_CONSTANT(RT_LOWERHEX);
    ADD_INT_CONSTANT(RT_ALPHAHEX);
    ADD_INT_CONSTANT(RT_UPPER_ALPHAHEX);
    ADD_INT_CONSTANT(RT_LOWER_ALPHAHEX);
    ADD_INT_CONSTANT(RT_DECIMAL);
    ADD_INT_CONSTANT(RT_ALPHA);
    ADD_INT_CONSTANT(RT_UPPER);
    ADD_INT_CONSTANT(RT_LOWER);

#undef ADD_INT_CONSTANT
    return 0;

error:
    return -1;
}

static PyMethodDef vec64_methods[] = {
    {"base64_symbol_indexes",
     base64_symbol_indexes,
     METH_VARARGS,
     base64_symbol_indexes__doc__},
    {"_split",
     vec64_split,
     METH_VARARGS,
     vec64_split__doc__},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef_Slot vec64_slots[] = {
    {Py_mod_exec, vec64_exec},
    {0, NULL},
};

static struct PyModuleDef vec64_module = {
    PyModuleDef_HEAD_INIT,
    "_vec64",
    .m_doc = "word2vec-style embeddings for base64",
    .m_size = 0,
    .m_methods = vec64_methods,
    .m_slots = vec64_slots,
};

PyMODINIT_FUNC
PyInit__vec64(void)
{
    return PyModuleDef_Init(&vec64_module);
}
