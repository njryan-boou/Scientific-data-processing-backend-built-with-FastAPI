#include <iostream>

using namespace std;

int add(int a, int b) {
    return a + b;
}

int main() {
    int x;
    float y;
    double z;
    long n;

    cin >> x;
    cin >> y;
    cin >> z;
    cin >> n;
    cout << x << y << z << n << endl; // all varibles

    cout << "Sum\n";
    cout << x + y + z + n; // addition of all 3 varibles;

    int i = 0;
    while ( i < 3) {
        cout << x;
        i++;
    }
    return 0;

    // function

    int v =  add(x, y);
    cout << v;
    for (int i = 0; i < 3; i++) {
        cout << x;
    }
}