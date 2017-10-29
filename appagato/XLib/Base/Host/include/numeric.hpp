/*------------------------------------------------------------------------------
Copyright © 2015 by Nicola Bombieri

H-BF is provided under the terms of The MIT License (MIT):

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
------------------------------------------------------------------------------*/
/**
 * @author Federico Busato
 * Univerity of Verona, Dept. of Computer Science
 * federico.busato@univr.it
 */
#pragma once

#define NO_CONSTEXPR 1

namespace numeric {

#if NO_CONSTEXPR
    #define CONST_EXPR
#else
    #define CONST_EXPR constexpr
#endif

// ==================== CONST EXPR TIME numeric methods ========================

template<typename T, typename R>
CONST_EXPR T    Min			(const T a, const R b);
template<typename T, typename R>
CONST_EXPR T    Max			(const T a, const R b);
template<typename T, typename R>
CONST_EXPR T  Div			(const T value, const R div);
template<typename T>
CONST_EXPR T  UpperApprox	(const T n, const T MUL);
template<typename T>
CONST_EXPR T  LowerApprox	(const T n, const T MUL);
template<typename T>
CONST_EXPR bool is_power2	(const T x);
template<typename T>
CONST_EXPR T  Factorial	(const T x);
template<typename T>
CONST_EXPR T  BinaryCoeff	(const T x, const T y);
//CONST_EXPR int  Mod2		(const int X, const int MOD);

// ======================= COMPILE TIME numeric methods ========================

template<int A, int B>      struct MIN;
template<int A, int B>      struct MAX;
template<int N>             struct LOG2;
template<int N>             struct MOD2;
template<int N>             struct IS_POWER2;
template<int N>             struct FACTORIAL;
template<int N, int K>      struct BINARY_COEFF;
template<int LOW, int HIGH> struct PRODUCTS_SEQUENCES;

// ========================== RUN TIME numeric methods =========================

inline unsigned NearestPower2_UP(unsigned v);
inline int Log2(const int v);

template<typename T>
float PerCent(const T part, const T max);

template<class iterator_t>
float Average(iterator_t start, iterator_t end);

template<class iterator_t>
float StdDeviation(iterator_t start, iterator_t end);

template<typename R>
struct compareFloatABS_Str {
    template<typename T>
    inline bool operator() (const T a, const T b);
};

template<typename R>
struct compareFloatRel_Str {
    template<typename T>
    inline bool operator() (const T a, const T b);
};

} //@Numeric

#include "impl/numeric.i.hpp"
