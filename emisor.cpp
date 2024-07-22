#include <iostream>
#include <string>
// codigo en C++ para el emisor
// Arturo Argueta
// Diego Alonzo
//emplea el uso de bit de paridad
using namespace std;
int main(){
cout << "Ingrese una cadena de bits, ejemplo : 10001 " << endl;
string x;
cin >> x;
int paridad = 0;
for(int i = 0; i < x.length(); i++){
    if (x[i] == '1'){
        paridad++;
    }
}
if(paridad%2==0){
  cout << x << '0' << endl;  
}else{
    cout << x << '1' << endl;
}
}
