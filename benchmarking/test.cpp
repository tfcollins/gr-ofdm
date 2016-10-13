#include <iostream>
#include <functional>

class Paulo {

	public:
		static int add_numbers(int a, int b)
		{
			return a+b;
		}

		std::function<int(int,int)> fptr;

		Paulo()
		{
			fptr = Paulo::add_numbers;
		}




};


int main()
{

	Paulo p = Paulo();
	std::cout<<"Adder: "<<p.add_numbers(1,2)<<"\n";
	std::cout<<"Adder: "<<p.fptr(1,2)<<"\n";

	return 0;
}

