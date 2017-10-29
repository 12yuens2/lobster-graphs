#include <iomanip>
#include <string>
#include <cuda_runtime.h>
#include "../../../../Host/BaseHost.hpp"

inline std::ostream& operator<<(std::ostream& out, const int2& value) {
    out << "( " << value.x << "," << value.y << " )";
    return out;
}

inline bool operator== (const int2& A, const int2& B) {
	return A.x == B.x && A.y == B.y;
}

inline bool operator!= (const int2& A, const int2& B) {
	return A.x != B.x || A.y != B.y;
}

inline bool operator< (const int2& A, const int2& B) {
	return A.x < B.x || (A.x == B.x && A.y < B.y);
}

inline bool operator<= (const int2& A, const int2& B) {
	return A.x <= B.x && A.y <= B.y;
}

inline bool operator>= (const int2& A, const int2& B) {
	return A.x >= B.x && A.y >= B.y;
}

inline bool operator> (const int2& A, const int2& B) {
	return A.x > B.x || (A.x == B.x && A.y > B.y);
}

namespace cuda_util {

inline void __getLastCudaError(const char *errorMessage, const char *file, const int line) {
	cudaError_t err = cudaGetLastError();
	if (cudaSuccess != err) {
		std::cerr << std::endl << " CUDA error   "
                  << StreamModifier::Emph::SET_UNDERLINE << file
                  << "(" << line << ")"
				  << StreamModifier::Emph::SET_RESET << " : " << errorMessage
                  << " -> " << cudaGetErrorString(err) << "(" << (int) err
                  << ") "<< std::endl << std::endl;
		cudaDeviceReset();
		std::exit(EXIT_FAILURE);
	}
}

template<bool FAULT, typename T, typename R>
bool Compare(T* hostArray, R* devArray, const int size, std::string str) {
	R* ArrayCMP = new R[size];
	cudaMemcpy(ArrayCMP, devArray, size * sizeof(R), cudaMemcpyDeviceToHost);
	__CUDA_ERROR("Copy To Host");

	bool flag = fUtil::Compare<FAULT>(hostArray, ArrayCMP, size, str);
	delete[] ArrayCMP;
    return flag;
}

template<bool FAULT, typename T, typename R>
bool Compare(T* hostArray, R* devArray, const int size) {
    R* ArrayCMP = new R[size];
    cudaMemcpy(ArrayCMP, devArray, size * sizeof(R), cudaMemcpyDeviceToHost);
    __CUDA_ERROR("Copy To Host");

    bool flag = fUtil::Compare<FAULT>(hostArray, ArrayCMP, size);
    delete[] ArrayCMP;
    return flag;
}

template<bool FAULT, typename T, typename R>
bool Compare(T* hostArray, R* devArray, const int size, bool (*cmpFunction)(T, R)) {
    R* ArrayCMP = new R[size];
    cudaMemcpy(ArrayCMP, devArray, size * sizeof(R), cudaMemcpyDeviceToHost);
    __CUDA_ERROR("Copy To Host");

    bool flag = fUtil::Compare<FAULT>(hostArray, ArrayCMP, size, cmpFunction);
    delete[] ArrayCMP;
    return flag;
}

template<bool FAULT, typename T, typename R>
bool CompareAndSort(T* hostArray, R* devArray, const int size) {
	R* ArrayCMP = new R[size];
	cudaMemcpy(ArrayCMP, devArray, size * sizeof(R), cudaMemcpyDeviceToHost);
	__CUDA_ERROR("Copy To Host");

    bool flag = fUtil::CompareAndSort<FAULT>(hostArray, ArrayCMP, size);

    delete[] ArrayCMP;
    return flag;
}

#if defined(__NVCC__)

template<typename T>
__global__ void scatter(const int* __restrict__ toScatter,
                        const int scatter_size,
                        T*__restrict__ Dest,
                        const T value) {

    const int ID = blockIdx.x * blockDim.x + threadIdx.x;

	for (int i = ID; i < scatter_size; i += blockDim.x * gridDim.x)
		Dest[ toScatter[i] ] = value;
}

template<typename T>
__global__ void fill(T* devArray, const int fill_size, const T value) {

    const int ID = blockIdx.x * blockDim.x + threadIdx.x;
	for (int i = ID; i < fill_size; i += blockDim.x * gridDim.x)
        devArray[ i ] = value;
}


template<typename T>
__global__ void fill2(T* devArray, const int fill_size, const T value) {
    const int stride = blockDim.x * gridDim.x;
    T* devArrayEnd = devArray + fill_size;
    devArray += blockIdx.x * blockDim.x + threadIdx.x;

    for (; devArray < devArrayEnd; devArray += stride)
        *devArray = value;
}

template <typename T>
__global__ void fill(T* devMatrix, const int n_of_rows, const int n_of_columns,
                     const T value, int integer_pitch) {

	const int X = blockDim.x * blockIdx.x + threadIdx.x;
	const int Y = blockDim.y * blockIdx.y + threadIdx.y;
    if (integer_pitch == 0)
        integer_pitch = n_of_columns;

    for (int i = Y; i < n_of_rows; i += blockDim.y * gridDim.y) {
        for (int j = X; j < n_of_columns; j += blockDim.x * gridDim.x)
		    devMatrix[i * integer_pitch + j] = value;
    }
}
#endif

} //@cuda_util
