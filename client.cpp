#include "Socket.h"

#include <iostream>
#include <string>

using namespace std;

int main() {

  try {
    SocketClient s("www.google.com", 80);

    s.SendLine("GET / HTTP/1.0");
    s.SendLine("Host: www.google.com");
    s.SendLine("");

    while (1) {
      string l = s.ReceiveLine();
      if (l.empty()) break;
      cout << l;
      cout.flush();
    }

  } 
  catch (const char* s) {
    cerr << s << endl;
  } 
  catch (string s) {
    cerr << s << endl;
  } 
  catch (...) {
    cerr << "unhandled exception\n";
  }

  return 0;
}