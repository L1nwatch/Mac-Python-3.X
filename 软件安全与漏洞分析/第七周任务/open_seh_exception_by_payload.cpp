// 编译器通过一个头文件stdafx.h来使用预编译头文件。stdafx.h这个头文件名是可以在project的编译设置里指定的。
//编译器认为，所有在指令#include "stdafx.h"前的代码都是预编译的，它跳过#include "stdafx. h"指令，使用projectname.pch编译这条指令之后的所有代码。
#include <stdio.h>
#include <WINSOCK2.H>
#include <excpt.h>
#pragma comment(lib, "ws2_32.lib")  //加载 ws2_32.dll

#define BUF_SIZE 64

unsigned char shellcode[] = {0x33,0xC0,0x50,0xB8,0x2E,0x65,0x78,0x65,0x50,0xB8,0x63,0x61,0x6C,0x63,0x50,0x8D,0x04,0x24,0x50,0xB9,0xC7,0x93,0xBF,0x77,0xFF,0xD1};
typedef void (*MYPROC)(LPTSTR); 

int ExceptionHandler(void){
	printf("Something Wrong!\n");
	return 0;
}

void client_deal(SOCKET sock, sockaddr_in servAddr,sockaddr fromAddr, int * res){
	__try{
		char buffer[BUF_SIZE] = {0};	
		printf("Input a string: ");
		gets(buffer);
		sendto(sock, buffer, strlen(buffer), 0, (struct sockaddr*)&servAddr, sizeof(servAddr));

		int addrLen = sizeof(fromAddr);
		int strLen = recvfrom(sock, buffer, 512, 0, &fromAddr, &addrLen);
		buffer[strLen] = '\0';

		printf("Received: %s\n",buffer);

		*res = 0;
	}__except(ExceptionHandler()){
		printf("Exception ! \n");
	}
}

int main(void){
	//初始化DLL
	WSADATA wsaData;
	WSAStartup(MAKEWORD(2, 2), &wsaData);

	//创建套接字
	SOCKET sock = socket(PF_INET, SOCK_DGRAM, 0);

	//服务器地址信息
	sockaddr_in servAddr;
	memset(&servAddr, 0, sizeof(servAddr));  //每个字节都用0填充
	servAddr.sin_family = PF_INET;
	servAddr.sin_addr.s_addr = inet_addr("192.168.117.1");
	servAddr.sin_port = htons(9999);

	//不断获取用户输入并发送给服务器，然后接受服务器数据
	sockaddr fromAddr;
	int addrLen = sizeof(fromAddr);
	int res = 1;
	memset((char*)&fromAddr,0,addrLen);	// 初始化
	while(1){
		client_deal(sock, servAddr, fromAddr, &res);
	}

	closesocket(sock);
	WSACleanup();
	return 0;
}