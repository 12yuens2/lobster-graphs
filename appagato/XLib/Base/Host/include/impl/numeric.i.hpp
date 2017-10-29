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
#include <algorithm>
#include <ratio>
#include <numeric>
#include <cmath>

namespace numeric {

// ==================== CONST EXPR TIME numeric methods ========================

template<typename T, typename R>
CONST_EXPR T Min(const T a, const R b) { return a < b ? a : b; }

template<typename T, typename R>
CONST_EXPR T Max(const T a, const R b) { return a > b ? b : a; }

template<typename T, typename R>
CONST_EXPR T Div(const T value, const R div) { return (value + div - 1) / div; }

template<typename T>
CONST_EXPR T UpperApprox(const T n, const T MUL)	{
    return Div(n, MUL) * MUL;
}

template<typename T>
CONST_EXPR T LowerApprox(const T n, const T MUL)	{
    return (n / MUL) * MUL;
}

template<typename T>
CONST_EXPR bool CheckPow2(const T x) {
    return (x != 0) && !(x & (x - 1));
}

template<typename T>
CONST_EXPR T Factorial(const T x) {
    return x <= 1 ? 1 : x * Factorial(x - 1);
}
// ??????????
/*CONST_EXPR int BinaryCoeff(const int x, const int y) {
    return (x, x - y) / ( Factorial(y) );
}*/

//template<typename T>
//CONST_EXPR int Mod2(const T X, const int MOD) { return X & (MOD - 1);	}

// ======================= COMPILE TIME numeric methods ========================

template<int A, int B> struct MAX {	static const int value = A > B ? A : B; };
template<int A, int B> struct MIN {	static const int value = A < B ? A : B;	};

//lower bound
template<int N>
struct LOG2 {
    static_assert(N > 0, "LOG2 : N <= 0");
    static_assert(IS_POWER2<N>::value, "LOG2 : N is not power of two");

	static const int value = 1 + LOG2<N / 2>::value;
};
template<>	struct LOG2<1> { static const int value = 0;	};

template<int N>
struct MOD2 {
	static_assert(N > 0, "MOD2 : N <= 0");
    static_assert(IS_POWER2<N>::value, "MOD2 : N is not power of two");

	static const int value = N - 1;
};

template<int N>
struct IS_POWER2 {
	static const bool value = (N != 0) && !(N & (N - 1));
};

template<int N>
struct FACTORIAL {
	static_assert(N >= 0, "FACTORIAL");
	static const int value = N * FACTORIAL<N - 1>::value;
};
template<> struct FACTORIAL<0> { static const int value = 1; };

template<int LOW, int HIGH>
struct PRODUCTS_SEQUENCES {
    static const int value = LOW * PRODUCTS_SEQUENCES<LOW + 1, HIGH>::value;
};
template<int LOW>
struct PRODUCTS_SEQUENCES<LOW, LOW> {
    static const int value = LOW;
};

template<int N, int K>
struct BINARY_COEFF {
    private:
        static const int min = MIN<N, N - K>::value;
        static const int max = MAX<N, N - K>::value;
    public:
        static const int value = PRODUCTS_SEQUENCES<min + 1, N>::value /
                                 FACTORIAL<max>::value;
};

// ========================== RUN TIME numeric methods =========================

inline int NnearestPower2_UP(int v) {
    v--;
    v |= v >> 1;
    v |= v >> 2;
    v |= v >> 4;
    v |= v >> 8;
    v |= v >> 16;
    v++;
    return v;
}

inline int Log2(const int v) {
    return 31 - __builtin_clz(v);
}

template<class iterator_t>
float Average(iterator_t start, iterator_t end) {
    using T = typename std::iterator_traits<iterator_t>::value_type;
    const T sum = std::accumulate(start, end, 0);
    return static_cast<float>(sum) / std::distance(start, end);
}

template<class iterator_t>
float StdDeviation(iterator_t start, iterator_t end) {
    using T = typename std::iterator_traits<iterator_t>::value_type;
    T sum = 0, sum2 = 0;
    for (auto it : start) {
        sum += *it;
        sum2 += std::pow(*it, 2);
    }
    const int N = std::distance(start, end);
    return std::sqrt(static_cast<float>(N * sum2 - std::pow(sum, 2))) / N;
}

template<typename T>
float PerCent(const T part, const T max) {
	return (static_cast<float>(part) / max) * 100;
}

template<std::intmax_t Num, std::intmax_t Den>
struct compareFloatABS_Str<std::ratio<Num, Den>> {
    template<typename T>
    inline bool operator() (const T a, const T b) {
        const T epsilon = static_cast<T>(Num) / static_cast<T>(Den);
        return std::abs(a - b) < epsilon;
    }
};

template<std::intmax_t Num, std::intmax_t Den>
struct compareFloatRel_Str<std::ratio<Num, Den>> {
    template<typename T>
    inline bool operator() (const T a, const T b) {
        const T epsilon = static_cast<T>(Num) / static_cast<T>(Den);
        const T diff = std::abs(a - b);
        //return (diff < epsilon) || (diff / std::max(std::abs(a), std::abs(b)) < epsilon);
        return (diff < epsilon) ||
        (diff / std::min(std::abs(a) + std::abs(b), std::numeric_limits<float>::max()) < epsilon);
    }
};

} //@numeric
