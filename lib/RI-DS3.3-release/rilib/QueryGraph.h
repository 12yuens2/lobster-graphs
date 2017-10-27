/*
 * QueryGraph.h
 *
 *  Created on: Nov 11, 2012
 *      Author: vbonnici
 */
/*
Copyright (c) 2013 by Rosalba Giugno

This library contains portions of other open source products covered by separate
licenses. Please see the corresponding source files for specific terms.

RI is provided under the terms of The MIT License (MIT):

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 */

#ifndef QUERYGRAPH_H_
#define QUERYGRAPH_H_


namespace rilib{


class QueryGraph{
public:
	int nof_nodes;

	void** nodes_attrs;

	int* adj_sizes;
	int* out_adj_sizes;
	int* in_adj_sizes;

	int** adj_list;//out...in
	void*** adj_attrs;//out...in
	int** edge_ids;//out...in

	QueryGraph(){
		nof_nodes = 0;
		nodes_attrs = NULL;
		adj_sizes = NULL;
		out_adj_sizes = NULL;
		in_adj_sizes = NULL;
		adj_list = NULL;
		adj_attrs = NULL;
		edge_ids = NULL;
	}









	void print(){
		std::cout<<"| QueryGraph:  nof nodes "<<nof_nodes<<"\n";
		for(int i=0; i<nof_nodes; i++){
			std::cout<<"| node["<<i<<"]\n";
			std::cout<<"| \tattribute_pointer["<<nodes_attrs[i]<<"]\n";
			std::cout<<"| \tattribute["<<*((std::string*)(nodes_attrs[i]))<<"]\n";
			std::cout<<"| \tadj_size["<<adj_sizes[i]<<"] out_adj_size["<<out_adj_sizes[i]<<"] in_adj_size["<<in_adj_sizes[i]<<"] \n";
			std::cout<<"| \tadjs[";
//			std::cout<<" o ";
			for(int j=0; j<adj_sizes[i]; j++){
//				if(j == out_adj_sizes[i])
//					std::cout<<" i ";
				std::cout<<adj_list[i][j]<<"\t";
			}
			std::cout<<"]\n";
			std::cout<<"| \teids[";
			for(int j=0; j<adj_sizes[i]; j++){
//				if(j == out_adj_sizes[i])
//					std::cout<<" i ";
				std::cout<<edge_ids[i][j]<<"\t";
			}
			std::cout<<"]\n";
		}
	}
};
}


#endif /* QUERYGRAPH_H_ */
