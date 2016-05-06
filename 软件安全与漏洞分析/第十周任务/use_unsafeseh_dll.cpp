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

class Client{
public:
	void client_deal(SOCKET sock, sockaddr_in servAddr,sockaddr fromAddr, int * res){
		__try{
			HINSTANCE hInst = LoadLibrary(L"no_safeseh_dll_build.dll");

			char buffer[BUF_SIZE] = {0};	
			printf("Input a string: ");
			gets(buffer);
			sendto(sock, buffer, strlen(buffer), 0, (struct sockaddr*)&servAddr, sizeof(servAddr));

			int addrLen = sizeof(fromAddr);
			int strLen = recvfrom(sock, buffer, 512, 0, &fromAddr, &addrLen);
			buffer[strLen] = '\0';

			// SafeSEH 绕过时需要的复制 ShellCode 到堆的语句
			char * heap_buf = (char * )malloc(512);
			memcpy(heap_buf, buffer, 512);

			printf("Received: %s\n",buffer);
			
			*res = 4 / *res;	// 利用 SEH 绕过时需要的触发异常语句
		}__except(ExceptionHandler()){
			printf("Exception ! \n");
		}
	}
	virtual void virtual_func()
	{
		printf("利用虚表指针绕过失败了！\n");
	}
};


int main(void){
	// 	// 测试 shellcode
	// 	void (*fun)();
	// 	*(int *)&fun=(int)shellcode;
	// 	fun();
	// 	return 0;



	//int * ret;
	//HINSTANCE LibHandle;
	//MYPROC ProcAdd;
	//char sysbuf[7] = "system";
	//char cmdbuf[16] = "calc.exe";
	//LibHandle = LoadLibrary("msvcrt.dll");
	//ProcAdd = (MYPROC)GetProcAddress(LibHandle,sysbuf); // 0x77bf93c7
	//(ProcAdd)(cmdbuf);
	//return 0;


	//测试 Done
	// 	__asm{
	// 		xor eax,eax			// "\0"
	// 		push eax
	// 		mov eax,0x6578652e 	// "exe." <- ".exe"
	// 		push eax
	// 		mov eax,0x636c6163 	// "clac" <- "calc"
	// 		push eax
	// 		lea eax,[esp]		// 字符串 "calc.exe" 的地址
	// 		push eax
	// 		mov ecx,0x77bf93c7	// system 调用
	// 		call ecx
	// 	}
	// 	return 0;

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
		Client user;
		user.client_deal(sock, servAddr, fromAddr, &res);
	}

	closesocket(sock);
	WSACleanup();
	return 0;
}