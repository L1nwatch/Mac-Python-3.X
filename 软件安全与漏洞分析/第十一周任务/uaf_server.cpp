#include "winsock2.h"
#pragma comment(lib, "ws2_32.lib")

#include <fcntl.h>
#include <iostream> 
#include <cstring>
#include <cstdlib>
// #include <unistd.h>
#include <string>

using namespace std;

const int BUF_SIZE = 64;

class Human{
private:
	virtual void give_shell(){
		//system("/bin/sh");
		cout << "Success give shell!" << endl;
		system("pause");
	}
protected:
	int age;
	string name;
public:
	virtual void introduce(){
		cout << "My name is " << name << endl;
		cout << "I am " << age << " years old" << endl;
	}
};

class Man: public Human{
public:
	Man(string name, int age){
		this->name = name;
		this->age = age;
	}
	virtual void introduce(){
		Human::introduce();
		cout << "I am a nice guy!" << endl;
	}
};

class Woman: public Human{
public:
	Woman(string name, int age){
		this->name = name;
		this->age = age;
	}
	virtual void introduce(){
		Human::introduce();
		cout << "I am a cute girl!" << endl;
	}
};

void client_deal(SOCKET sServer, SOCKET sClient, int addrClientlen) {
	Human* m = new Man("Jack", 25);
	Human* w = new Woman("Jill", 21);

	char buf[BUF_SIZE];
	size_t len;
	char* data;
	unsigned int op;
	while(1){
		send(sClient, "1. use\n2. after\n3. free\n", strlen("1. use\n2. after\n3. free\n"), 0);
		recv(sClient, buf, 1, 0);
		op = atoi(buf);;

		switch(op){
		case 1:
			m->introduce();
			w->introduce();
			break;
		case 2:		
			// 接收长度
			recv(sClient, buf, 2, 0); // 这里接收长度为 2，发送长度也要为 2 才行
			len = atoi(buf);

			// 接收数据
			data = new char[len];
			recv(sClient, buf, BUF_SIZE, 0);
			memcpy(data, buf, len);

			send(sClient, "your data is allocated", strlen("your data is allocated"), 0);
			break;
		case 3:
			delete m;
			delete w;
			break;
		default:
			break;
		}
	}
}

int main(int argc, char* argv[])
{
	WSADATA wsd; //WSADATA变量
	SOCKET sServer; //服务器套接字
	SOCKET sClient; //客户端套接字
	SOCKADDR_IN addrServ;; //服务器地址
	int retVal; //返回值

	//初始化套结字动态库
	if (WSAStartup(MAKEWORD(2,2), &wsd) != 0)
	{
		cout << "WSAStartup failed!" << endl;
		return 1;
	}
	//创建套接字
	sServer = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
	if(INVALID_SOCKET == sServer)
	{
		cout << "socket failed!" << endl;
		WSACleanup();//释放套接字资源;
		return  -1;
	}
	//服务器套接字地址 
	addrServ.sin_family = AF_INET;
	addrServ.sin_port = htons(9999);
	addrServ.sin_addr.s_addr = inet_addr("192.168.117.131");
	//绑定套接字
	retVal = bind(sServer, (LPSOCKADDR)&addrServ, sizeof(SOCKADDR_IN));

	if(SOCKET_ERROR == retVal)
	{
		cout << "bind failed!" << endl;
		closesocket(sServer); //关闭套接字
		WSACleanup(); //释放套接字资源;
		return -1;
	}
	//开始监听 
	retVal = listen(sServer, 1);
	if(SOCKET_ERROR == retVal)
	{
		cout << "listen failed!" << endl;
		closesocket(sServer); //关闭套接字
		WSACleanup(); //释放套接字资源;
		return -1;
	}
	//接受客户端请求
	sockaddr_in addrClient;
	int addrClientlen = sizeof(addrClient);
	sClient = accept(sServer,(sockaddr FAR*)&addrClient, &addrClientlen);
	if(INVALID_SOCKET == sClient)
	{
		cout << "accept failed!" << endl;
		closesocket(sServer); //关闭套接字
		WSACleanup(); //释放套接字资源;
		return -1;
	}

	client_deal(sServer, sClient, addrClientlen);

	//退出
	closesocket(sServer); //关闭套接字
	closesocket(sClient); //关闭套接字
	WSACleanup(); //释放套接字资源;

	return 0;
}